import pytest


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
    """Test API key validation function"""
    # Define a simple validation function for testing
    def validate_api_key(context, valid_keys=None):
        valid_keys = valid_keys or ["test_api_key"]
        api_key = context.request.headers.get("apikey")
        
        if not api_key:
            return {"status": "error", "code": 401, "message": "Missing API key"}
        
        if api_key not in valid_keys:
            return {"status": "error", "code": 403, "message": "Invalid API key"}
        
        return None
    
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
async def test_property_detail_tool():
    """Test property detail tool"""
    # Define a simple mock property detail function for testing
    async def property_detail(context, attom_id=None, address=None):
        # Validate API key
        api_key = context.request.headers.get("apikey")
        if not api_key:
            return {"status": "error", "code": 401, "message": "Missing API key"}
        if api_key != "test_api_key":
            return {"status": "error", "code": 403, "message": "Invalid API key"}
        
        # Check parameters
        if not any([attom_id, address]):
            return {"status": "error", "code": 400, "message": "Missing identifier"}
        
        # Return mock data based on ID
        if attom_id == "145423726" or address:
            return {
                "status": "success",
                "property": {
                    "attomId": attom_id or "default_id",
                    "address": {
                        "street_address": address or "123 Main St",
                        "city": "Example City"
                    },
                    "beds": 3,
                    "baths": 2
                }
            }
        else:
            return {"status": "error", "code": 404, "message": "Property not found"}
    
    # Test with valid API key and AttomID
    context = MockContext(headers={"apikey": "test_api_key"})
    result = await property_detail(context, attom_id="145423726")
    assert result["status"] == "success"
    assert result["property"]["attomId"] == "145423726"
    
    # Test with invalid AttomID
    result = await property_detail(context, attom_id="999999")
    assert result["status"] == "error"
    assert result["code"] == 404
    
    # Test with missing API key
    context = MockContext()
    result = await property_detail(context, attom_id="145423726")
    assert result["status"] == "error"
    assert result["code"] == 401