#!/usr/bin/env python3
"""
bump_version.py – replace __VERSION__ placeholders with the next Git tag version.

Usage
-----

# bump patch and update pyproject.toml in place
python bump_version.py patch

# bump minor and update two files
python bump_version.py minor --files pyproject.toml src/myapp/__init__.py

The script prints VERSION=<new-version> at the end so that
  new_version=$(python bump_version.py patch)      # Bash
can capture it.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List


SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def latest_git_version() -> str:
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
        raise ValueError(f"Tag {tag!r} is not a valid semantic version")
    except (subprocess.CalledProcessError, ValueError):
        # First tag in the repo
        return "0.0.0"


def bump(version: str, kind: str) -> str:
    major, minor, patch = map(int, version.split("."))
    if kind == "major":
        major, minor, patch = major + 1, 0, 0
    elif kind == "minor":
        minor, patch = minor + 1, 0
    elif kind == "patch":
        patch += 1
    else:
        sys.exit(f"Invalid bump type: {kind}")
    return f"{major}.{minor}.{patch}"


def substitute_version(files: List[Path], new_version: str) -> None:
    """Replace __VERSION__ with new_version everywhere in *files* (in place)."""
    placeholder_found = False
    for fp in files:
        text = fp.read_text()
        if "__VERSION__" in text:
            placeholder_found = True
            fp.write_text(text.replace("__VERSION__", new_version))
            print(f"• Updated {fp}")
    if not placeholder_found:
        print("Warning: No __VERSION__ placeholders were found in the given files.")


# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump the latest git tag and substitute __VERSION__ placeholders."
    )
    parser.add_argument(
        "bump_type", choices=["major", "minor", "patch"], help="Version part to bump"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=["pyproject.toml"],
        metavar="PATH",
        help="Files to rewrite (space-separated list)",
    )
    args = parser.parse_args()

    current = latest_git_version()
    next_ver = bump(current, args.bump_type)

    print(f"Bumping {args.bump_type}: {current}  →  {next_ver}")

    # Write files
    files = [Path(p) for p in args.files]
    substitute_version(files, next_ver)

    # Emit for CI
    print(f"VERSION={next_ver}")


if __name__ == "__main__":
    main()
