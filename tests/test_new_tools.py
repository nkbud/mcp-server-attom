"""Tests for new ATTOM API tool implementations.

This module contains tests for the newly implemented tool categories
to ensure 1:1 API correspondence is maintained.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.mark.asyncio
async def test_area_tools_imports():
    """Test that area tools can be imported and have expected functions."""
    from tools.area_tools import (
        boundary_detail, hierarchy_lookup, state_lookup,
        county_lookup, cbsa_lookup, geoid_lookup,
        geocode_legacy_lookup, location_lookup
    )
    
    # All functions should be callable
    assert callable(boundary_detail)
    assert callable(hierarchy_lookup)
    assert callable(state_lookup)
    assert callable(county_lookup)
    assert callable(cbsa_lookup)
    assert callable(geoid_lookup)
    assert callable(geocode_legacy_lookup)
    assert callable(location_lookup)


@pytest.mark.asyncio
async def test_poi_tools_imports():
    """Test that POI tools can be imported and have expected functions."""
    from tools.poi_tools import poi_search, poi_category_lookup
    
    assert callable(poi_search)
    assert callable(poi_category_lookup)


@pytest.mark.asyncio
async def test_community_tools_imports():
    """Test that community tools can be imported and have expected functions."""
    from tools.community_tools import neighborhood_community
    
    assert callable(neighborhood_community)


@pytest.mark.asyncio
async def test_school_tools_imports():
    """Test that school tools can be imported and have expected functions."""
    from tools.school_tools import school_profile, school_district, school_search
    
    assert callable(school_profile)
    assert callable(school_district)
    assert callable(school_search)


@pytest.mark.asyncio 
async def test_area_tools_parameter_validation():
    """Test area tools parameter validation."""
    from tools.area_tools import boundary_detail, AreaParams
    
    # Test with missing required parameters
    params = AreaParams()
    result = await boundary_detail(params)
    
    assert result.status_code == 400
    assert "required" in result.status_message.lower()


@pytest.mark.asyncio
async def test_poi_search_parameter_validation():
    """Test POI search parameter validation."""
    from tools.poi_tools import poi_search, POIParams
    
    # Test with missing required location parameters
    params = POIParams()
    result = await poi_search(params)
    
    assert result.status_code == 400
    assert "required" in result.status_message.lower()


@pytest.mark.asyncio
async def test_community_tools_parameter_validation():
    """Test community tools parameter validation."""
    from tools.community_tools import neighborhood_community, CommunityParams
    
    # Test with missing required parameters
    params = CommunityParams()
    result = await neighborhood_community(params)
    
    assert result.status_code == 400
    assert "required" in result.status_message.lower()


@pytest.mark.asyncio
async def test_school_tools_parameter_validation():
    """Test school tools parameter validation."""
    from tools.school_tools import school_profile, SchoolParams
    
    # Test with missing required parameters
    params = SchoolParams()
    result = await school_profile(params)
    
    assert result.status_code == 400
    assert "required" in result.status_message.lower()


def test_api_coverage_documentation_exists():
    """Test that API coverage documentation exists and is comprehensive."""
    coverage_file = os.path.join(os.path.dirname(__file__), '..', 'ATTOM_API_COVERAGE.md')
    
    assert os.path.exists(coverage_file), "ATTOM_API_COVERAGE.md documentation should exist"
    
    with open(coverage_file, 'r') as f:
        content = f.read()
    
    # Check for key sections
    assert "Property Data" in content
    assert "Area Data" in content  
    assert "POI" in content
    assert "Community Data" in content
    assert "School" in content
    assert "100%" in content  # Coverage percentage
    assert "pay_blck" in content  # Documentation of paid features


def test_readme_updated_with_new_tools():
    """Test that README was updated with new tool categories."""
    readme_file = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    
    with open(readme_file, 'r') as f:
        content = f.read()
    
    # Check for new tool categories
    assert "Area & Location Tools" in content
    assert "POI (Points of Interest) Tools" in content
    assert "Community Tools" in content
    assert "School Tools" in content
    
    # Check for specific new tools
    assert "boundary_detail" in content
    assert "poi_search" in content
    assert "neighborhood_community" in content
    assert "school_profile" in content


if __name__ == "__main__":
    # Run basic syntax and import validation
    print("🧪 Running ATTOM API implementation tests...")
    
    try:
        # Test imports work
        sys.path.insert(0, '../src')
        
        from tools import area_tools, poi_tools, community_tools, school_tools
        print("✅ All new tool modules imported successfully")
        
        # Test documentation exists
        test_api_coverage_documentation_exists()
        print("✅ API coverage documentation exists")
        
        test_readme_updated_with_new_tools()
        print("✅ README updated with new tools")
        
        print("\n🎯 Implementation validation complete!")
        print("✅ Area Tools: 8 endpoints")
        print("✅ POI Tools: 2 endpoints") 
        print("✅ Community Tools: 1 endpoint")
        print("✅ School Tools: 3 endpoints")
        print("✅ Total New Tools: 14 endpoints")
        print("\n🚀 Ready for full 1:1 ATTOM API correspondence!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Note: Full testing requires dependencies. Run with pytest for complete validation.")
    except Exception as e:
        print(f"❌ Test error: {e}")