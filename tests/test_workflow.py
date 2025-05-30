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
    pypi_step = None
    for step in release_steps:
        if step.get("name") == "Publish to PyPI":
            pypi_step = step
            break
    
    assert pypi_step is not None, "PyPI publishing step should exist"
    assert "if" in pypi_step, "PyPI step should have a conditional"
    
    # The conditional should check for secrets.PYPI_TOKEN, not use != '' syntax
    conditional = pypi_step["if"]
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
    
    # Should not have unnecessary permissions
    assert "packages" not in workflow["permissions"], "packages permission not needed for this workflow"