#!/usr/bin/env python3
"""
Test that the GitHub workflow files are valid.
"""

import yaml
from pathlib import Path


def test_release_workflow_valid():
    """Test that the release workflow YAML is valid."""
    workflow_path = Path(".github/workflows/release.yml")
    assert workflow_path.exists(), "Release workflow file should exist"
    
    with workflow_path.open() as f:
        workflow = yaml.safe_load(f)
    
    # Basic structure validation
    assert "name" in workflow
    assert True in workflow or "on" in workflow  # 'on' is parsed as boolean True in YAML
    assert "jobs" in workflow
    
    # Check that we have the expected jobs
    assert "ci" in workflow["jobs"]
    assert "release" in workflow["jobs"]
    
    # Check that release depends on CI
    assert workflow["jobs"]["release"]["needs"] == "ci"
    
    # Check that the conditional for PyPI publishing uses correct syntax
    release_steps = workflow["jobs"]["release"]["steps"]
    pypi_steps = []
    for step in release_steps:
        if "Publish to PyPI" in step.get("name", ""):
            pypi_steps.append(step)
    
    assert len(pypi_steps) >= 1, "At least one PyPI publishing step should exist"
    
    # All PyPI steps should have conditionals
    for step in pypi_steps:
        assert "if" in step, "PyPI step should have a conditional"
        conditional = step["if"]
        assert "secrets.PYPI_TOKEN" in conditional
        assert "!=" not in conditional, "Should not use != '' syntax in conditionals"


def test_workflow_permissions():
    """Test that workflow has appropriate permissions."""
    workflow_path = Path(".github/workflows/release.yml")
    
    with workflow_path.open() as f:
        workflow = yaml.safe_load(f)
    
    # Should have contents: write for tagging and releases
    assert "permissions" in workflow
    assert "contents" in workflow["permissions"]
    assert workflow["permissions"]["contents"] == "write"
    
    # Should have id-token: write for trusted publishing
    assert "id-token" in workflow["permissions"]
    assert workflow["permissions"]["id-token"] == "write"
    
    # Should not have unnecessary permissions
    assert "packages" not in workflow["permissions"], "packages permission not needed for this workflow"


def test_release_job_can_run_on_prs():
    """Test that the release job can run on PRs for testing purposes."""
    workflow_path = Path(".github/workflows/release.yml")
    
    with workflow_path.open() as f:
        workflow = yaml.safe_load(f)
    
    # Check that release job does not have a restrictive conditional
    release_job = workflow["jobs"]["release"]
    # The release job should be able to run on PRs for testing
    # If there's an "if" condition, it should not restrict to main pushes only
    if "if" in release_job:
        conditional = release_job["if"]
        # Should not restrict to only main pushes
        should_not_have_main_restriction = not ("refs/heads/main" in conditional and "push" in conditional)
        assert should_not_have_main_restriction, "Release job should be able to run on PRs for testing"


def test_pypi_publishing_steps():
    """Test that PyPI publishing steps are configured correctly."""
    workflow_path = Path(".github/workflows/release.yml")
    
    with workflow_path.open() as f:
        workflow = yaml.safe_load(f)
    
    release_steps = workflow["jobs"]["release"]["steps"]
    
    # Find PyPI publishing steps
    pypi_token_step = None
    trusted_publishing_step = None
    
    for step in release_steps:
        if step.get("name") == "Publish to PyPI (with token)":
            pypi_token_step = step
        elif step.get("name") == "Publish to PyPI (trusted publishing)":
            trusted_publishing_step = step
    
    # Both steps should exist
    assert pypi_token_step is not None, "PyPI token publishing step should exist"
    assert trusted_publishing_step is not None, "Trusted publishing step should exist"
    
    # Token step should check for token existence
    assert "if" in pypi_token_step, "PyPI token step should have conditional"
    assert "secrets.PYPI_TOKEN" in pypi_token_step["if"]
    
    # Trusted publishing step should run when no token
    assert "if" in trusted_publishing_step, "Trusted publishing step should have conditional"
    assert "!secrets.PYPI_TOKEN" in trusted_publishing_step["if"]