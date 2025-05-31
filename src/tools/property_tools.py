"""MCP tools for the ATTOM Property API.

This module provides MCP tools for accessing the Property API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier
from src.tools.utils import make_api_call

# Configure logging
logger = structlog.get_logger(__name__)


# Property Address Tool
@mcp.tool()
async def property_address(params: PropertyIdentifier) -> AttomResponse:
    """Get property address information."""
    return await make_api_call("property/address", params, "property_address")


# Property Detail Tool
@mcp.tool()
async def property_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get property detail information."""
    return await make_api_call("property/detail", params, "property_detail")

# Property Basic Profile Tool
@mcp.tool()
async def property_basic_profile(params: PropertyIdentifier) -> AttomResponse:
    """Get property basic profile information."""
    return await make_api_call("property/basicprofile", params, "property_basic_profile")

# Property Expanded Profile Tool
@mcp.tool()
async def property_expanded_profile(params: PropertyIdentifier) -> AttomResponse:
    """Get property expanded profile information."""
    return await make_api_call("property/expandedprofile", params, "property_expanded_profile")

# Property Detail With Schools Tool
@mcp.tool()
async def property_detail_with_schools(params: PropertyIdentifier) -> AttomResponse:
    """Get property detail with schools information."""
    return await make_api_call("property/detailwithschools", params, "property_detail_with_schools")

@mcp.tool()
async def property_basic_history(params: PropertyIdentifier) -> AttomResponse:
    """Get property basic history information."""
    return await make_api_call("saleshistory/basichistory", params, "property_basic_history")

@mcp.tool()
async def property_building_permits(params: PropertyIdentifier) -> AttomResponse:
    """Get property building permits information."""
    return await make_api_call("property/buildingpermits", params, "property_building_permits")

@mcp.tool()
async def property_detail_mortgage(params: PropertyIdentifier) -> AttomResponse:
    """Get property detail mortgage information."""
    return await make_api_call("property/detailmortgage", params, "property_detail_mortgage")

@mcp.tool()
async def property_detail_owner(params: PropertyIdentifier) -> AttomResponse:
    """Get property detail owner information."""
    return await make_api_call("property/detailowner", params, "property_detail_owner")

@mcp.tool()
async def property_detail_mortgage_owner(params: PropertyIdentifier) -> AttomResponse:
    """Get property detail mortgage owner information."""
    return await make_api_call("property/detailmortgageowner", params, "property_detail_mortgage_owner")

@mcp.tool()
async def property_expanded_history(params: PropertyIdentifier) -> AttomResponse:
    """Get property expanded history information."""
    return await make_api_call("saleshistory/expandedhistory", params, "property_expanded_history")

@mcp.tool()
async def building_permits(params: PropertyIdentifier) -> AttomResponse:
    """Get building permits information."""
    return await make_api_call("property/BuildingPermits", params, "building_permits")

@mcp.tool()
async def property_id_search_sort(params: PropertyIdentifier) -> AttomResponse:
    """Get property id search sort information."""
    return await make_api_call("property/id", params, "property_id_search_sort")

@mcp.tool()
async def property_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get propertysnapshot information.

    Returns propertysnapshot information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertysnapshot information
    """
    log = logger.bind(tool="property_snapshot", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.attom_id:
        request_params["AttomID"] = params.attom_id
    elif params.address:
        request_params["address"] = params.address
    elif params.address1 and params.address2:
        request_params["address1"] = params.address1
        request_params["address2"] = params.address2
    elif params.fips and params.apn:
        request_params["fips"] = params.fips
        request_params["apn"] = params.apn
    else:
        log.error("Invalid property identifier")
        return AttomResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching propertysnapshot")

    try:
        response = await client.get("property/snapshot", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertysnapshot", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
