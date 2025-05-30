# Release Workflow Configuration

This document describes the required repository configuration for the GitHub Actions release workflow to operate successfully.

## Workflow Overview

The release workflow in `.github/workflows/release.yml` automatically:
1. Runs CI tests on every push and pull request
2. Creates releases, tags, and publishes to PyPI on pushes to the `main` branch

## Required Repository Configuration

### 1. Repository Permissions
The workflow requires these permissions (already configured in the workflow file):
- `contents: write` - Required for creating tags and releases
- `id-token: write` - Required for trusted publishing to PyPI

### 2. Branch Protection (Recommended)
Configure branch protection rules for the `main` branch:
- Require pull request reviews before merging
- Require status checks to pass before merging
- Include the CI job in required status checks

### 3. PyPI Publishing Configuration

The workflow supports two methods for PyPI publishing:

#### Option A: API Token (Traditional)
1. Generate a PyPI API token at https://pypi.org/manage/account/token/
2. Add the token as a repository secret named `PYPI_TOKEN`
3. The workflow will use this token for publishing

#### Option B: Trusted Publishing (Recommended)
1. Configure trusted publishing on PyPI:
   - Go to your project's settings on PyPI
   - Add a trusted publisher for GitHub Actions
   - Set the repository to: `nkbud/mcp-server-attom`
   - Set the workflow filename to: `release.yml`
2. No secrets needed - the workflow will automatically use trusted publishing

If neither option is configured, the publish steps will fail but won't prevent the release creation.

## Release Process

### Automatic Release Triggers
- **Patch Release**: Any commit to `main` that doesn't start with "feat:" or "feature:"
- **Minor Release**: Commits to `main` that start with "feat:" or "feature:"

### Manual Testing
Run the manual test script to verify the workflow components:
```bash
python /path/to/test_workflow_manual.py
```

## Workflow Behavior

1. **On Pull Requests**: Only runs CI tests, does not create releases
2. **On Push to Main**: Runs CI tests, then creates release if CI passes
3. **Version Management**: Uses `__VERSION__` placeholder in `pyproject.toml` which gets replaced during the release process
4. **Git Tags**: Creates semantic version tags (e.g., `v1.2.3`)
5. **GitHub Releases**: Creates GitHub releases with built artifacts attached

## Troubleshooting

### Common Issues
1. **Release job doesn't run**: Check that the push was to the `main` branch
2. **PyPI publishing fails**: Verify PYPI_TOKEN secret or trusted publishing configuration
3. **Version bumping fails**: Ensure `pyproject.toml` contains `__VERSION__` placeholder
4. **Build fails**: Check that all dependencies are properly declared in `pyproject.toml`

### Required Files
- `.github/workflows/release.yml` - The workflow definition
- `scripts/bump_version.py` - Version bumping script
- `pyproject.toml` - Must contain `version = "__VERSION__"` placeholder