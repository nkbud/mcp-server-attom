#!/usr/bin/env python3
"""
Tests for the __VERSION__ placeholder versioning system.
"""

import os
import subprocess
import tempfile
import re
import pytest
from pathlib import Path


def test_pyproject_toml_has_version_placeholder():
    """Test that pyproject.toml contains __VERSION__ placeholder."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Check that both version entries use __VERSION__
    assert 'version = "__VERSION__"' in content, "pyproject.toml should contain __VERSION__ placeholder"
    
    # Count occurrences - should be exactly 2 (project and tool.uvx sections)
    version_count = content.count('version = "__VERSION__"')
    assert version_count == 2, f"Expected exactly 2 __VERSION__ placeholders, found {version_count}"


def test_increment_version_script_calculates_without_modifying():
    """Test that bump_version.py calculates version and modifies files correctly."""
    # Save original content
    pyproject_path = Path("pyproject.toml")
    original_content = pyproject_path.read_text()
    
    try:
        # Run the script
        result = subprocess.run(
            ["python", "scripts/bump_version.py", "patch"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check that output contains version calculation
        assert "VERSION=" in result.stdout
        assert "Updated pyproject.toml" in result.stdout
        
        # Verify pyproject.toml was modified (no longer contains placeholder)
        content = pyproject_path.read_text()
        assert '__VERSION__' not in content, "pyproject.toml should not contain __VERSION__ after script run"
        assert 'version = "0.0.1"' in content, "pyproject.toml should contain actual version"
        
    finally:
        # Restore original content
        pyproject_path.write_text(original_content)


def test_version_substitution():
    """Test that version substitution works correctly."""
    # Create a temporary copy of pyproject.toml
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.toml', delete=False) as temp_file:
        pyproject_path = Path("pyproject.toml")
        original_content = pyproject_path.read_text()
        temp_file.write(original_content)
        temp_file.flush()
        
        try:
            # Substitute the version
            test_version = "1.2.3"
            subprocess.run(
                ["sed", "-i", f"s/__VERSION__/{test_version}/g", temp_file.name],
                check=True
            )
            
            # Read the substituted content
            with open(temp_file.name, 'r') as f:
                substituted_content = f.read()
            
            # Verify substitution worked
            assert f'version = "{test_version}"' in substituted_content
            assert '__VERSION__' not in substituted_content
            
            # Count version occurrences - should be exactly 2
            version_count = substituted_content.count(f'version = "{test_version}"')
            assert version_count == 2, f"Expected exactly 2 version substitutions, found {version_count}"
            
        finally:
            # Clean up
            os.unlink(temp_file.name)


def test_version_script_output_format():
    """Test that the version script outputs in expected format."""
    result = subprocess.run(
        ["python", "scripts/bump_version.py", "minor"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    
    # Extract VERSION= line
    version_lines = [line for line in result.stdout.split('\n') if line.startswith('VERSION=')]
    assert len(version_lines) == 1, "Should output exactly one VERSION= line"
    
    version_line = version_lines[0]
    version = version_line.split('=')[1]
    
    # Verify version format (semantic versioning)
    assert re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', version), f"Invalid version format: {version}"


def test_different_bump_types():
    """Test that different bump types work correctly."""
    bump_types = ['patch', 'minor', 'major']
    
    # Save original content
    pyproject_path = Path("pyproject.toml")
    original_content = pyproject_path.read_text()
    
    try:
        for bump_type in bump_types:
            # Restore placeholder before each test
            pyproject_path.write_text(original_content)
            
            result = subprocess.run(
                ["python", "scripts/bump_version.py", bump_type],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0, f"Failed for bump type {bump_type}: {result.stderr}"
            assert f"Bumping {bump_type}:" in result.stdout
            assert "VERSION=" in result.stdout
            
    finally:
        # Restore original content
        pyproject_path.write_text(original_content)