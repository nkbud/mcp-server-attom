#!/usr/bin/env python3
"""
Increment the version in pyproject.toml based on the specified bump type.
"""

import argparse
import re
import sys


def get_current_version(file_path):
    """Extract the current version from pyproject.toml."""
    with open(file_path, "r") as f:
        content = f.read()

    # First check for __VERSION__ placeholder and handle it
    if "__VERSION__" in content:
        print("Warning: Found __VERSION__ placeholder, replacing with 0.0.1")
        content = content.replace("__VERSION__", "0.0.1")
        # Write the fixed content back to the file
        with open(file_path, "w") as f:
            f.write(content)

    version_match = re.search(r'version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"', content)
    if not version_match:
        print(f"Error: Could not find version in {file_path}")
        sys.exit(1)

    return version_match.group(1)


def increment_version(version, bump_type):
    """Increment the version based on the bump type."""
    major, minor, patch = map(int, version.split("."))

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        print(f"Error: Invalid bump type '{bump_type}'")
        sys.exit(1)

    return f"{major}.{minor}.{patch}"


def update_pyproject_toml(file_path, new_version):
    """Update version in pyproject.toml with the new version."""
    with open(file_path, "r") as f:
        content = f.read()

    # Update the version in the [project] section
    updated_content = re.sub(
        r'(version\s*=\s*)"[0-9]+\.[0-9]+\.[0-9]+"', r'\1"' + new_version + '"', content
    )

    # Also update the version in the [tool.uvx] section if it exists
    updated_content = re.sub(
        r'(\[tool\.uvx\].*?version\s*=\s*)"[0-9]+\.[0-9]+\.[0-9]+"',
        r'\1"' + new_version + '"',
        updated_content,
        flags=re.DOTALL,
    )

    with open(file_path, "w") as f:
        f.write(updated_content)


def main():
    parser = argparse.ArgumentParser(description="Increment version in pyproject.toml")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="The type of version bump to perform",
    )
    parser.add_argument(
        "--file", default="pyproject.toml", help="Path to the pyproject.toml file"
    )

    args = parser.parse_args()

    current_version = get_current_version(args.file)
    new_version = increment_version(current_version, args.bump_type)

    print(f"Bumping {args.bump_type} version: {current_version} -> {new_version}")

    update_pyproject_toml(args.file, new_version)
    print(f"Updated {args.file} with new version: {new_version}")

    # Print the new version to stdout for the workflow to capture
    print(f"VERSION={new_version}")


if __name__ == "__main__":
    main()
