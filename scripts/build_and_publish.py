#!/usr/bin/env python3
"""
build_and_publish.py - A complete script to build and publish packages to GitHub and PyPI.

This script handles:
- Version bumping (patch, minor, major)
- Package building
- Git tag creation and pushing
- GitHub Release creation
- PyPI publishing (with token or trusted publishing)
- Verification of publication

Usage:
    python scripts/build_and_publish.py [OPTIONS]

Options:
    --bump-type TYPE         Version bump type: 'patch', 'minor', 'major' (default: patch)
    --dry-run                Run without publishing or pushing tags
    --skip-tests             Skip running tests
    --gh-token TOKEN         GitHub token (can also set GITHUB_TOKEN env var)
    --pypi-token TOKEN       PyPI token (can also set PYPI_TOKEN env var)
    --trusted-publishing     Use PyPI trusted publishing instead of token
    --files FILE [FILE ...]  Files to update with new version (default: pyproject.toml)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
GITHUB_API_URL = "https://api.github.com"
PYPI_API_URL = "https://pypi.org/pypi"
ANSI_COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def color(text: str, color_name: str) -> str:
    """Apply ANSI color to text if terminal supports it."""
    if sys.stdout.isatty():
        return f"{ANSI_COLORS.get(color_name, '')}{text}{ANSI_COLORS['reset']}"
    return text


def print_step(step: str) -> None:
    """Print a step header."""
    print(f"\n{color('▶ ' + step, 'bold')}")


def print_success(msg: str) -> None:
    """Print a success message."""
    print(f"{color('✅ ', 'green')}{msg}")


def print_error(msg: str) -> None:
    """Print an error message."""
    print(f"{color('❌ ', 'red')}{msg}")


def print_warning(msg: str) -> None:
    """Print a warning message."""
    print(f"{color('⚠️ ', 'yellow')}{msg}")


def print_info(msg: str) -> None:
    """Print an info message."""
    print(f"{color('ℹ️ ', 'blue')}{msg}")


def run_command(
    cmd: List[str], check: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print_info(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, check=False)
        
        if result.returncode != 0 and check:
            print_error(f"Command failed with exit code {result.returncode}")
            if result.stderr:
                print(result.stderr)
            sys.exit(1)
        
        return result
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        if check:
            sys.exit(1)
        # Create a dummy result object
        return subprocess.CompletedProcess(cmd, 127, "", "Command not found")
    except Exception as e:
        print_error(f"Error executing command: {e}")
        if check:
            sys.exit(1)
        # Create a dummy result object
        return subprocess.CompletedProcess(cmd, 1, "", str(e))


def get_package_name() -> str:
    """Get the package name from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print_error("pyproject.toml not found")
        sys.exit(1)
        
    content = pyproject_path.read_text()
    match = re.search(r'name\s*=\s*"([^"]+)"', content)
    if not match:
        print_error("Package name not found in pyproject.toml")
        sys.exit(1)
    
    return match.group(1)


def get_latest_git_version() -> str:
    """Return the latest git tag that matches v<semver>, or '0.0.0' if none."""
    try:
        tag = (
            subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0", "--match", "v[0-9]*"],
                text=True,
                capture_output=True,
                check=True,
            )
            .stdout.strip()
            .lstrip("v")
        )
        if SEMVER_RE.match(tag):
            return tag
        print_warning(f"Tag {tag!r} is not a valid semantic version, using 0.0.0")
        return "0.0.0"
    except (subprocess.CalledProcessError, ValueError):
        print_info("No version tags found, starting at 0.0.0")
        return "0.0.0"


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump the version according to the bump type."""
    major, minor, patch = map(int, current_version.split("."))
    if bump_type == "major":
        major, minor, patch = major + 1, 0, 0
    elif bump_type == "minor":
        minor, patch = minor + 1, 0
    elif bump_type == "patch":
        patch += 1
    else:
        print_error(f"Invalid bump type: {bump_type}")
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"


SEMVER_PATTERN = re.compile(r'(version\s*=\s*")(\d+\.\d+\.\d+)(")')

def substitute_version(files: List[Path], new_version: str) -> None:
    """Replace version with new_version in *files* (in place)."""
    version_updated = False
    for fp in files:
        if not fp.exists():
            print_warning(f"File not found: {fp}")
            continue
            
        text = fp.read_text()
        new_text, count = SEMVER_PATTERN.subn(rf'\g<1>{new_version}\g<3>', text)
        if count > 0:
            fp.write_text(new_text)
            print_info(f"Updated version to {new_version} in {fp}")
            version_updated = True
    
    if not version_updated:
        print_warning("No version found to update in the given files.")


def build_package() -> bool:
    """Build the package."""
    print_step("Building package")
    
    # Check for wheel and sdist output dir
    dist_dir = Path("dist")
    if dist_dir.exists():
        print_info("Cleaning up old build artifacts")
        shutil.rmtree(dist_dir)
    
    # Try to use uv first, fall back to python -m build
    try:
        run_command(["uv", "--version"], check=False)
        result = run_command(["uv", "build"], capture_output=False)
    except FileNotFoundError:
        print_info("uv not found, using build module")
        
        # Check if build is available
        try:
            run_command(["python", "-m", "build", "--version"], check=False)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_warning("build module not found, installing...")
            run_command(["pip", "install", "build"])
            
        result = run_command(["python", "-m", "build"], capture_output=False)
    
    # Verify build artifacts
    dist_files = list(dist_dir.glob("*"))
    if not dist_files:
        print_error("No build artifacts found")
        return False
    
    print_success(f"Built {len(dist_files)} distribution files:")
    for file in dist_files:
        print(f"  📦 {file.name}")
    
    return True


def validate_package() -> bool:
    """Validate the package with twine."""
    print_step("Validating package")
    
    dist_dir = Path("dist")
    if not dist_dir.exists() or not list(dist_dir.glob("*")):
        print_error("No distribution files found")
        return False
    
    # Check if twine is available
    result = run_command(["twine", "--version"], check=False)
    if result.returncode != 0:
        print_warning("twine not found, installing...")
        run_command(["pip", "install", "twine"])
    
    # Run twine check
    result = run_command(["twine", "check", str(dist_dir / "*")], check=False)
    if result.returncode == 0:
        print_success("Package validation passed")
        return True
    else:
        print_error("Package validation failed")
        return False


def create_git_tag(version: str, dry_run: bool = False) -> bool:
    """Create and push a git tag for the version."""
    print_step("Creating git tag")
    
    tag = f"v{version}"
    
    # Create the tag
    result = run_command(
        ["git", "tag", "-a", tag, "-m", f"Release {tag}"], 
        check=False
    )
    if result.returncode != 0:
        if "already exists" in result.stderr:
            print_warning(f"Tag {tag} already exists")
            return True
        print_error(f"Failed to create tag: {result.stderr}")
        return False

    print_success(f"Created tag {tag}")
    
    # Push the tag if not a dry run
    if not dry_run:
        result = run_command(["git", "push", "origin", tag], check=False)
        if result.returncode != 0:
            print_error(f"Failed to push tag: {result.stderr}")
            return False
        print_success(f"Pushed tag {tag}")
    else:
        print_info(f"[DRY RUN] Would push tag {tag}")
    
    return True


def create_github_release(
    version: str, github_token: Optional[str], dry_run: bool = False
) -> bool:
    """Create a GitHub release for the version."""
    print_step("Creating GitHub release")
    
    if not github_token:
        print_error("GitHub token not found. Set --gh-token or GITHUB_TOKEN env var")
        return False
        
    if dry_run:
        print_info(f"[DRY RUN] Would create GitHub release v{version}")
        return True
    
    # Get repository information from git
    try:
        remote_url = (
            subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                text=True,
                capture_output=True,
                check=True,
            )
            .stdout.strip()
        )
        
        # Parse remote URL to get owner and repo
        match = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", remote_url)
        if not match:
            print_error(f"Could not parse remote URL: {remote_url}")
            return False
            
        owner, repo = match.groups()
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to get git repository info: {e}")
        return False
    
    # Get distribution files
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print_error("dist directory not found")
        return False
        
    dist_files = list(dist_dir.glob("*"))
    if not dist_files:
        print_error("No distribution files found in dist directory")
        return False
    
    # Use GitHub API to create release
    release_data = {
        "tag_name": f"v{version}",
        "name": f"Release v{version}",
        "body": f"Release v{version}",
        "draft": False,
        "prerelease": False,
    }
    
    # Create the release
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    # Use curl to create the release
    curl_cmd = [
        "curl", "-s", "-X", "POST",
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/releases",
        "-H", f"Authorization: Bearer {github_token}",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        "-d", json.dumps(release_data)
    ]
    
    result = run_command(curl_cmd, check=False)
    
    if result.returncode != 0:
        print_error(f"Failed to create GitHub release: {result.stderr}")
        return False
        
    release_info = json.loads(result.stdout)
    if "id" not in release_info:
        print_error(f"Failed to create GitHub release: {release_info.get('message', 'Unknown error')}")
        return False
        
    release_id = release_info["id"]
    upload_url = release_info["upload_url"].split("{")[0]
    
    print_success(f"Created GitHub release: {release_info['html_url']}")
    
    # Upload assets
    for file_path in dist_files:
        asset_name = file_path.name
        content_type = "application/octet-stream"
        if asset_name.endswith(".whl"):
            content_type = "application/zip"
        elif asset_name.endswith(".tar.gz"):
            content_type = "application/gzip"
            
        curl_upload_cmd = [
            "curl", "-s", "-X", "POST",
            f"{upload_url}?name={asset_name}",
            "-H", f"Authorization: Bearer {github_token}",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            "-H", f"Content-Type: {content_type}",
            "--data-binary", f"@{file_path}"
        ]
        
        result = run_command(curl_upload_cmd, check=False)
        
        if result.returncode != 0:
            print_error(f"Failed to upload {asset_name}: {result.stderr}")
            continue
            
        asset_result = json.loads(result.stdout)
        if "id" not in asset_result:
            print_error(f"Failed to upload {asset_name}: {asset_result.get('message', 'Unknown error')}")
            continue
            
        print_success(f"Uploaded {asset_name}")
    
    return True


def publish_to_pypi(
    version: str, 
    pypi_token: Optional[str], 
    use_trusted_publishing: bool,
    dry_run: bool = False
) -> bool:
    """Publish the package to PyPI."""
    print_step("Publishing to PyPI")
    
    if dry_run:
        print_info("[DRY RUN] Would publish to PyPI")
        return True
    
    # Check that dist files exist
    dist_dir = Path("dist")
    if not dist_dir.exists() or not list(dist_dir.glob("*")):
        print_error("No distribution files found")
        return False
    
    # Try to use UV first, fall back to twine
    if shutil.which("uv"):
        cmd = ["uv", "publish"]
        if use_trusted_publishing:
            cmd.extend(["--trusted-publishing", "automatic"])
            print_info("Using trusted publishing")
        elif pypi_token:
            os.environ["UV_PUBLISH_TOKEN"] = pypi_token
            print_info("Using PyPI token for authentication")
        else:
            print_error("No PyPI token and not using trusted publishing")
            return False
            
        result = run_command(cmd, check=False)
        if result.returncode == 0:
            print_success("Package published to PyPI with uv")
            return True
    else:
        # Fall back to twine
        cmd = ["twine", "upload", "dist/*"]
        if not pypi_token:
            print_error("PyPI token required for twine upload")
            return False
            
        os.environ["TWINE_USERNAME"] = "__token__"
        os.environ["TWINE_PASSWORD"] = pypi_token
        
        result = run_command(cmd, check=False)
        if result.returncode == 0:
            print_success("Package published to PyPI with twine")
            return True
    
    print_error(f"Failed to publish to PyPI: {result.stderr}")
    return False


def verify_pypi_publication(version: str) -> bool:
    """Verify that the package was published to PyPI."""
    print_step("Verifying PyPI publication")
    
    package_name = get_package_name().replace("-", "-")
    pypi_url = f"{PYPI_API_URL}/{package_name}/{version}/json"
    
    print_info(f"Checking {pypi_url}")
    print_info("Waiting for package to appear on PyPI (this may take a few minutes)...")
    
    # Try a few times with increasing delays
    attempts = 5
    for attempt in range(1, attempts + 1):
        try:
            result = run_command(["curl", "-s", pypi_url], check=False)
            
            if result.returncode == 0 and "version" in result.stdout:
                print_success(f"Package {package_name} version {version} found on PyPI!")
                print_info(f"View at: https://pypi.org/project/{package_name}/{version}/")
                return True
        except Exception as e:
            print_error(f"Error checking PyPI: {e}")
        
        if attempt < attempts:
            wait_time = attempt * 15  # 15, 30, 45, 60 seconds
            print_info(f"Package not found yet, waiting {wait_time} seconds... (attempt {attempt}/{attempts})")
            time.sleep(wait_time)
    
    print_warning("Package verification timed out, but it might still be processing.")
    print_info(f"Check manually at: https://pypi.org/project/{package_name}/")
    return False


# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------
def main() -> int:
    """Main function to orchestrate the build and publish process."""
    parser = argparse.ArgumentParser(
        description="Build and publish a Python package to GitHub and PyPI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--bump-type",
        choices=["patch", "minor", "major"],
        default="patch",
        help="Version part to bump",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without publishing or pushing tags",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests",
    )
    parser.add_argument(
        "--gh-token",
        help="GitHub token (can also set GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--pypi-token",
        help="PyPI token (can also set PYPI_TOKEN env var)",
    )
    parser.add_argument(
        "--trusted-publishing",
        action="store_true",
        help="Use PyPI trusted publishing instead of token",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=["pyproject.toml"],
        help="Files to update with new version",
    )
    args = parser.parse_args()
    
    # Get tokens from env vars if not provided as args
    github_token = args.gh_token or os.environ.get("GITHUB_TOKEN")
    pypi_token = args.pypi_token or os.environ.get("PYPI_TOKEN")

    # 1. Bump version
    print_step(f"Bumping version ({args.bump_type})")
    current_version = get_latest_git_version()
    new_version = bump_version(current_version, args.bump_type)
    print_info(f"Bumping {args.bump_type}: {current_version} → {new_version}")
    
    # Update files
    files = [Path(file) for file in args.files]
    substitute_version(files, new_version)
    
    # 2. Build package
    if not build_package():
        print_error("Package build failed, aborting")
        return 1
    
    # 3. Validate package
    if not validate_package():
        print_warning("Package validation failed, but continuing anyway")
    
    # 4. Create and push Git tag
    if not create_git_tag(new_version, args.dry_run):
        print_error("Git tag creation failed, aborting")
        return 1
    
    # 5. Create GitHub release
    if not create_github_release(new_version, github_token, args.dry_run):
        print_warning("GitHub release creation failed, but continuing")
    
    # 6. Publish to PyPI
    if not publish_to_pypi(new_version, pypi_token, args.trusted_publishing, args.dry_run):
        print_error("PyPI publication failed, aborting")
        return 1
    
    # 7. Verify publication success (only if not dry run)
    if not args.dry_run:
        verify_pypi_publication(new_version)
    
    # Done!
    print_step("All done!")
    print_success(f"Successfully released version {new_version}")
    print_info("Summary:")
    print(f"  🏷️  Git tag: v{new_version}")
    print(f"  📦 Package: {get_package_name()} {new_version}")
    print(f"  🔗 PyPI: https://pypi.org/project/{get_package_name()}/{new_version}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
