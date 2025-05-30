# Build and Publish Script

This directory contains scripts for building and publishing the package to GitHub Releases and PyPI.

## `build_and_publish.py`

A comprehensive script that handles:
- Version bumping (patch, minor, major)
- Package building
- Git tag creation and pushing
- GitHub Release creation
- PyPI publishing (with token or trusted publishing)
- Verification of publication

### Usage

```bash
python scripts/build_and_publish.py [OPTIONS]
```

### Options

- `--bump-type TYPE`: Version bump type: 'patch', 'minor', 'major' (default: patch)
- `--dry-run`: Run without publishing or pushing tags
- `--skip-tests`: Skip running tests
- `--gh-token TOKEN`: GitHub token (can also set GITHUB_TOKEN env var)
- `--pypi-token TOKEN`: PyPI token (can also set PYPI_TOKEN env var)
- `--trusted-publishing`: Use PyPI trusted publishing instead of token
- `--files FILE [FILE ...]`: Files to update with new version (default: pyproject.toml)

### Examples

```bash
# Bump patch version (0.1.0 -> 0.1.1) and publish
python scripts/build_and_publish.py --gh-token your_github_token --pypi-token your_pypi_token

# Bump minor version (0.1.1 -> 0.2.0) and publish
python scripts/build_and_publish.py --bump-type minor --gh-token your_github_token --pypi-token your_pypi_token

# Dry run (no publishing)
python scripts/build_and_publish.py --dry-run

# Use PyPI trusted publishing instead of token
python scripts/build_and_publish.py --trusted-publishing --gh-token your_github_token
```

### Environment Variables

Instead of passing tokens directly, you can use environment variables:

```bash
export GITHUB_TOKEN=your_github_token
export PYPI_TOKEN=your_pypi_token
python scripts/build_and_publish.py
```

## `bump_version.py`

A utility script to replace `__VERSION__` placeholders with the next Git tag version.

### Usage

```bash
# Bump patch and update pyproject.toml in place
python scripts/bump_version.py patch

# Bump minor and update two files
python scripts/bump_version.py minor --files pyproject.toml src/myapp/__init__.py
```

The script will print `VERSION=<new-version>` at the end, which can be captured in a shell script:

```bash
new_version=$(python scripts/bump_version.py patch)
```

## `test_pypi_publishing.py`

A test script to verify PyPI publishing workflow functionality. It validates that the package can be built and is ready for PyPI.

### Usage

```bash
python scripts/test_pypi_publishing.py
```