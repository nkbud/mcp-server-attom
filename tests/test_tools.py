"""Tests for the ATTOM API MCP tools."""

import httpx
import pytest
import respx

from src.tools import property_tools


@pytest.fixture
def mock_api():
    """Fixture to mock ATTOM API responses."""
    with respx.mock(
        base_url="https://api.gateway.attomdata.com", assert_all_called=False
    ) as respx_mock:
        # Mock property address endpoint
        respx_mock.get("/propertyapi/v1.0.0/property/address").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": {"version": "1.0.0", "code": 0, "msg": "SuccessWithResult"},
                    "property": [
                        {
                            "identifier": {
                                "attomId": 145423726,
                                "fips": "53063",
                                "apn": "26252.2605",
                            },
                            "address": {
                                "line1": "7804 N MILTON ST",
                                "line2": "SPOKANE, WA 99208",
                                "unitDesignator": "",
                                "unitValue": "",
                            },
                            "location": {"latitude": "47.734118", "longitude": "-117.426547"},
                        }
                    ],
                },
            )
        )

        # Mock property detail endpoint
        respx_mock.get("/propertyapi/v1.0.0/property/detail").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": {"version": "1.0.0", "code": 0, "msg": "SuccessWithResult"},
                    "property": [
                        {
                            "identifier": {
                                "attomId": 145423726,
                                "fips": "53063",
                                "apn": "26252.2605",
                            },
                            "address": {
                                "line1": "7804 N MILTON ST",
                                "line2": "SPOKANE, WA 99208",
                            },
                            "summary": {
                                "propclass": "Single Family Residence / Townhouse",
                                "propsubtype": "RESIDENTIAL",
                                "proptype": "SFR",
                                "yearbuilt": 2004,
                                "propLandUse": "SFR",
                                "beds": 3,
                                "baths": 2,
                            },
                        }
                    ],
                },
            )
        )

        yield respx_mock


@pytest.mark.asyncio
async def test_property_address(mock_api):
    """Test property_address tool."""
    result = await property_tools.property_address(
        property_tools.PropertyDetailParams(attom_id="145423726")
    )

    assert result.status_code == 200
    assert result.status_message == "Success"
    assert "property" in result.data
    assert len(result.data["property"]) > 0
    assert result.data["property"][0]["identifier"]["attomId"] == 145423726


@pytest.mark.asyncio
async def test_property_detail(mock_api):
    """Test property_detail tool."""
    result = await property_tools.property_detail(
        property_tools.PropertyDetailParams(attom_id="145423726")
    )

    assert result.status_code == 200
    assert result.status_message == "Success"
    assert "property" in result.data
    assert len(result.data["property"]) > 0
    assert result.data["property"][0]["identifier"]["attomId"] == 145423726
    assert result.data["property"][0]["summary"]["beds"] == 3
    assert result.data["property"][0]["summary"]["baths"] == 2
