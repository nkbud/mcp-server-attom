#!/usr/bin/env python3
"""
Test script to verify PyPI publishing workflow functionality.
This script validates that the package can be built and is ready for PyPI.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import json
import tarfile
import os


def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result."""
    print(f"🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True, check=check)
    if result.stdout:
        print(f"📤 Output: {result.stdout.strip()}")
    if result.stderr and result.returncode != 0:
        print(f"❌ Error: {result.stderr.strip()}")
    return result


def test_package_building():
    """Test that the package can be built successfully."""
    print("\n🏗️  Testing package building...")
    
    # Create a temporary copy to avoid modifying the original
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Copy necessary files
        repo_root = Path(__file__).parent.parent
        project_files = ['pyproject.toml', 'src', 'README.md']
        
        for item in project_files:
            src = repo_root / item
            dst = tmpdir / item
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        # Set a test version
        pyproject_path = tmpdir / 'pyproject.toml'
        content = pyproject_path.read_text()
        content = content.replace('__VERSION__', '0.1.0')
        pyproject_path.write_text(content)
        
        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            
            # Build the package using uv (preferred method)
            try:
                run_command(['uv', 'build'])
            except FileNotFoundError:
                # Fallback to installing uv first
                run_command([sys.executable, '-m', 'pip', 'install', 'uv'])
                run_command(['uv', 'build'])
            
            # Check if dist files were created
            dist_dir = tmpdir / 'dist'
            if not dist_dir.exists():
                print("❌ Dist directory not created")
                return False
            
            # Filter out non-package files
            dist_files = [f for f in dist_dir.glob('*') if f.name.endswith(('.whl', '.tar.gz'))]
            if not dist_files:
                print("❌ No distribution files created")
                return False
            
            print(f"✅ Built {len(dist_files)} distribution files:")
            for file in dist_files:
                print(f"   📦 {file.name}")
            
            # Verify with twine if available
            try:
                run_command([sys.executable, '-m', 'pip', 'install', 'twine'])
                result = run_command(['twine', 'check'] + [str(f) for f in dist_files])
                if result.returncode == 0:
                    print("✅ Package validation with twine: PASSED")
                else:
                    print("⚠️ Package validation with twine: FAILED")
                    return False
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ Twine not available for validation")
            
            return True
            
        finally:
            os.chdir(original_cwd)


def test_metadata_extraction():
    """Test that package metadata can be extracted correctly."""
    print("\n📋 Testing metadata extraction...")
    
    repo_root = Path(__file__).parent.parent
    pyproject_path = repo_root / 'pyproject.toml'
    
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False
    
    content = pyproject_path.read_text()
    
    # Check required fields
    required_fields = ['name', 'version', 'description', 'authors']
    missing_fields = []
    
    for field in required_fields:
        if field not in content:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return False
    
    print("✅ All required metadata fields present")
    
    # Check for version placeholder
    if '__VERSION__' in content:
        print("✅ Version placeholder found (will be replaced during release)")
    else:
        print("⚠️ No version placeholder found")
    
    return True


def test_workflow_validation():
    """Test that the workflow file is valid."""
    print("\n🔄 Testing workflow validation...")
    
    repo_root = Path(__file__).parent.parent
    workflow_path = repo_root / '.github' / 'workflows' / 'release.yml'
    
    if not workflow_path.exists():
        print("❌ Release workflow file not found")
        return False
    
    content = workflow_path.read_text()
    
    # Check for required elements
    required_elements = [
        'uv publish',
        'trusted-publishing',
        'UV_PUBLISH_TOKEN',
        'contents: write',
        'id-token: write'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing workflow elements: {missing_elements}")
        return False
    
    print("✅ Workflow contains all required elements")
    return True


def main():
    """Main test function."""
    print("🚀 Testing PyPI Publishing Workflow")
    print("=" * 50)
    
    tests = [
        ("Package Building", test_package_building),
        ("Metadata Extraction", test_metadata_extraction),
        ("Workflow Validation", test_workflow_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! PyPI publishing workflow is ready.")
        return 0
    else:
        print("💥 Some tests failed. Please fix the issues before releasing.")
        return 1


if __name__ == '__main__':
    sys.exit(main())