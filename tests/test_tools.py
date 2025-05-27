import pytest
from fastmcp import Context
from app.main import (
    property_detail,
    property_snapshot,
    property_search,
    boundary_detail,
    hierarchy_lookup,
    validate_api_key
)
import json
from unittest.mock import AsyncMock, MagicMock


class MockRequest:
    """Mock request object for testing"""
    def __init__(self, headers=None):
        self.headers = headers or {}


class MockContext:
    """Mock Context for testing FastMCP tools"""
    def __init__(self, headers=None):
        self.request = MockRequest(headers)


@pytest.mark.asyncio
async def test_property_detail_without_api_key():
    """Test property detail tool with missing API key"""
    # Create context without API key
    context = MockContext()
    
    # Call the tool
    result = await property_detail(context, attom_id="145423726")
    
    # Check that authentication failed
    assert result["status"] == "error"
    assert result["code"] == 401
    assert "Missing API key" in result["message"]


@pytest.mark.asyncio
async def test_property_detail_with_invalid_api_key():
    """Test property detail tool with invalid API key"""
    # Create context with invalid API key
    context = MockContext(headers={"apikey": "invalid_key"})
    
    # Call the tool
    result = await property_detail(context, attom_id="145423726")
    
    # Check that authentication failed
    assert result["status"] == "error"
    assert result["code"] == 403
    assert "Invalid API key" in result["message"]


@pytest.mark.asyncio
async def test_property_detail_missing_parameters():
    """Test property detail tool with missing property identifiers"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool without any property identifier
    result = await property_detail(context)
    
    # Check that validation failed
    assert result["status"] == "error"
    assert result["code"] == 400
    assert "At least one property identifier" in result["message"]


@pytest.mark.asyncio
async def test_property_detail_success():
    """Test property detail tool with valid parameters"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with a valid AttomID
    result = await property_detail(context, attom_id="145423726")
    
    # Check that the request succeeded
    assert result["status"] == "success"
    assert "property" in result
    assert result["property"]["attomId"] == "145423726"


@pytest.mark.asyncio
async def test_property_detail_not_found():
    """Test property detail tool with non-existent AttomID"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with a non-existent AttomID
    result = await property_detail(context, attom_id="999999")
    
    # Check that the property was not found
    assert result["status"] == "error"
    assert result["code"] == 404
    assert "not found" in result["message"]


@pytest.mark.asyncio
async def test_property_snapshot_success():
    """Test property snapshot tool with valid parameters"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with a valid address
    result = await property_snapshot(context, address="7804 N MILTON ST, SPOKANE, WA 99208")
    
    # Check that the request succeeded
    assert result["status"] == "success"
    assert "property" in result
    assert "address" in result["property"]
    assert "beds" in result["property"]
    assert "baths" in result["property"]


@pytest.mark.asyncio
async def test_property_search_success():
    """Test property search tool with valid parameters"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with a postal code
    result = await property_search(context, postal_code="99208")
    
    # Check that the request succeeded
    assert result["status"] == "success"
    assert "properties" in result
    assert "total_matches" in result
    assert "page" in result
    assert "page_size" in result


@pytest.mark.asyncio
async def test_boundary_detail_success():
    """Test boundary detail tool with valid parameters"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with a valid geo_id_v4
    result = await boundary_detail(context, geo_id_v4="baa5d7de09afdefd0ffcd66b581991de")
    
    # Check that the request succeeded
    assert result["status"] == "success"
    assert "boundary" in result
    assert result["boundary"]["format"] == "geojson"
    assert "data" in result["boundary"]


@pytest.mark.asyncio
async def test_hierarchy_lookup_success():
    """Test hierarchy lookup tool with valid parameters"""
    # Create context with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    
    # Call the tool with latitude and longitude
    result = await hierarchy_lookup(context, latitude=33.8239, longitude=-117.7842)
    
    # Check that the request succeeded
    assert result["status"] == "success"
    assert "hierarchy" in result
    assert "state" in result["hierarchy"]
    assert "county" in result["hierarchy"]
    assert "city" in result["hierarchy"]