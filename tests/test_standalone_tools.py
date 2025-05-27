import pytest
import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import directly from main module to avoid loading app
from app.main import (
    validate_api_key,
    property_detail,
    property_snapshot,
    property_search,
    boundary_detail,
    hierarchy_lookup,
)

# Mock context
class MockRequest:
    """Mock request object for testing"""
    def __init__(self, headers=None):
        self.headers = headers or {}


class MockContext:
    """Mock Context for testing FastMCP tools"""
    def __init__(self, headers=None):
        self.request = MockRequest(headers)


@pytest.mark.asyncio
async def test_validate_api_key():
    """Test API key validation"""
    # Test with missing API key
    context = MockContext()
    error = validate_api_key(context)
    assert error is not None
    assert error["code"] == 401
    
    # Test with invalid API key
    context = MockContext(headers={"apikey": "invalid_key"})
    error = validate_api_key(context)
    assert error is not None
    assert error["code"] == 403
    
    # Test with valid API key
    context = MockContext(headers={"apikey": "test_api_key"})
    error = validate_api_key(context)
    assert error is None


@pytest.mark.asyncio
async def test_property_detail():
    """Test property detail tool"""
    # Test with valid API key and AttomID
    context = MockContext(headers={"apikey": "test_api_key"})
    result = await property_detail(context, attom_id="145423726")
    assert result["status"] == "success"
    assert result["property"]["attomId"] == "145423726"
    
    # Test with invalid AttomID
    result = await property_detail(context, attom_id="999999")
    assert result["status"] == "error"
    assert result["code"] == 404


@pytest.mark.asyncio
async def test_property_snapshot():
    """Test property snapshot tool"""
    context = MockContext(headers={"apikey": "test_api_key"})
    result = await property_snapshot(context, address="123 Main St")
    assert result["status"] == "success"
    assert "property" in result


@pytest.mark.asyncio
async def test_property_search():
    """Test property search tool"""
    context = MockContext(headers={"apikey": "test_api_key"})
    result = await property_search(context, postal_code="99208")
    assert result["status"] == "success"
    assert "properties" in result or "property" in result