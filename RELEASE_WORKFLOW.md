# Release Process Documentation

This document describes the release process for this project, including both automated and manual methods.

## Release Options

There are two ways to release this project:

1. **Manual Build & Publish Script** (Recommended): Run locally to build, tag, and publish
2. **GitHub Actions Workflow**: Automatically triggers on pushes to the `main` branch

## Manual Build and Publish

For direct control over the release process, use the provided script:

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

### Example Usage

```bash
# Bump patch version and publish
python scripts/build_and_publish.py --gh-token your_github_token --pypi-token your_pypi_token

# Bump minor version with trusted publishing
python scripts/build_and_publish.py --bump-type minor --trusted-publishing --gh-token your_github_token
```

See `scripts/README.md` for more detailed examples and options.

## GitHub Actions Workflow

The workflow in `.github/workflows/release.yml` automatically processes releases.

### Required Repository Configuration

#### 1. Repository Permissions
The workflow requires these permissions (already configured in the workflow file):
- `contents: write` - Required for creating tags and releases
- `id-token: write` - Required for trusted publishing to PyPI

#### 2. Branch Protection (Recommended)
Configure branch protection rules for the `main` branch:
- Require pull request reviews before merging
- Require status checks to pass before merging
- Include the CI job in required status checks

#### 3. PyPI Publishing Configuration

The workflow supports two methods for PyPI publishing:

##### Option A: API Token (Traditional)
1. Generate a PyPI API token at https://pypi.org/manage/account/token/
2. Add the token as a repository secret named `PYPI_TOKEN`
3. The workflow will use this token for publishing

##### Option B: Trusted Publishing (Recommended)
1. Configure trusted publishing on PyPI:
   - Go to your project's settings on PyPI
   - Add a trusted publisher for GitHub Actions
   - Set the repository to: `nkbud/mcp-server-attom`
   - Set the workflow filename to: `release.yml`
2. No secrets needed - the workflow will automatically use trusted publishing

If neither option is configured, the publish steps will fail but won't prevent the release creation.

### Automatic Release Triggers
- **Patch Release**: Any commit to `main` that doesn't start with "feat:" or "feature:"
- **Minor Release**: Commits to `main` that start with "feat:" or "feature:"

### Manual Testing
You can test the release components with these scripts:
```bash
# Test the publishing workflow components
python scripts/test_pypi_publishing.py

# Test the build and publish script with dry run
python scripts/build_and_publish.py --dry-run
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
- `scripts/build_and_publish.py` - Manual build and publish script
- `pyproject.toml` - Must contain `version = "__VERSION__"` placeholder