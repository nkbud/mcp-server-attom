"""MCP tools for the ATTOM Property API.

This module provides MCP tools for accessing the Property API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Property Detail Models
class PropertyDetailParams(PropertyIdentifier):
    """Parameters for property detail endpoints."""

    pass


class PropertyDetailResponse(AttomResponse):
    """Response model for property detail endpoints."""

    pass


# Property Address Tool
async def property_address(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get property address information.

    Returns address information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Property address information
    """
    log = logger.bind(tool="property_address", params=params.model_dump())

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
        return PropertyDetailResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching property address")

    try:
        response = await client.get("property/address", request_params)
        return PropertyDetailResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching property address", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Property Detail Tool
async def property_detail(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get detailed property information.

    Returns comprehensive information about a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Detailed property information
    """
    log = logger.bind(tool="property_detail", params=params.model_dump())

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
        return PropertyDetailResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching property detail")

    try:
        response = await client.get("property/detail", request_params)
        return PropertyDetailResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching property detail", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Property Basic Profile Tool
async def property_basic_profile(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get basic property profile information.

    Returns basic profile information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Basic property profile information
    """
    log = logger.bind(tool="property_basic_profile", params=params.model_dump())

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
        return PropertyDetailResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching property basic profile")

    try:
        response = await client.get("property/basicprofile", request_params)
        return PropertyDetailResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching property basic profile", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Property Expanded Profile Tool
async def property_expanded_profile(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get expanded property profile information.

    Returns expanded profile information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Expanded property profile information
    """
    log = logger.bind(tool="property_expanded_profile", params=params.model_dump())

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
        return PropertyDetailResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching property expanded profile")

    try:
        response = await client.get("property/expandedprofile", request_params)
        return PropertyDetailResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching property expanded profile", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Property Detail With Schools Tool
async def property_detail_with_schools(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get property details including school information.

    Returns detailed property information including nearby schools.

    Args:
        params: Parameters to identify the property

    Returns:
        Property details with school information
    """
    log = logger.bind(tool="property_detail_with_schools", params=params.model_dump())

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
        return PropertyDetailResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching property detail with schools")

    try:
        response = await client.get("property/detailwithschools", request_params)
        return PropertyDetailResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching property detail with schools", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


async def property_basic_history(params: PropertyIdentifier) -> AttomResponse:
    """Get propertybasichistory information.

    Returns propertybasichistory information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertybasichistory information
    """
    log = logger.bind(tool="property_basic_history", params=params.model_dump())

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

    log.info("Fetching propertybasichistory")

    try:
        response = await client.get("saleshistory/basichistory", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertybasichistory", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_building_permits(params: PropertyIdentifier) -> AttomResponse:
    """Get propertybuildingpermits information.

    Returns propertybuildingpermits information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertybuildingpermits information
    """
    log = logger.bind(tool="property_building_permits", params=params.model_dump())

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

    log.info("Fetching propertybuildingpermits")

    try:
        response = await client.get("property/buildingpermits", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertybuildingpermits", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_detail_mortgage(params: PropertyIdentifier) -> AttomResponse:
    """Get propertydetailmortgage information.

    Returns propertydetailmortgage information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertydetailmortgage information
    """
    log = logger.bind(tool="property_detail_mortgage", params=params.model_dump())

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

    log.info("Fetching propertydetailmortgage")

    try:
        response = await client.get("property/detailmortgage", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertydetailmortgage", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_detail_owner(params: PropertyIdentifier) -> AttomResponse:
    """Get propertydetailowner information.

    Returns propertydetailowner information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertydetailowner information
    """
    log = logger.bind(tool="property_detail_owner", params=params.model_dump())

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

    log.info("Fetching propertydetailowner")

    try:
        response = await client.get("property/detailowner", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertydetailowner", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_detail_mortgage_owner(params: PropertyIdentifier) -> AttomResponse:
    """Get propertydetailmortgageowner information.

    Returns propertydetailmortgageowner information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertydetailmortgageowner information
    """
    log = logger.bind(tool="property_detail_mortgage_owner", params=params.model_dump())

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

    log.info("Fetching propertydetailmortgageowner")

    try:
        response = await client.get("property/detailmortgageowner", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertydetailmortgageowner", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_expanded_history(params: PropertyIdentifier) -> AttomResponse:
    """Get propertyexpandedhistory information.

    Returns propertyexpandedhistory information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Propertyexpandedhistory information
    """
    log = logger.bind(tool="property_expanded_history", params=params.model_dump())

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

    log.info("Fetching propertyexpandedhistory")

    try:
        response = await client.get("saleshistory/expandedhistory", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertyexpandedhistory", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def building_permits(params: PropertyIdentifier) -> AttomResponse:
    """Get building permits information.

    Returns building permits information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Building Permits information
    """
    log = logger.bind(tool="building_permits", params=params.model_dump())

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

    log.info("Fetching building permits")

    try:
        response = await client.get("property/BuildingPermits", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching building permits", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def property_id_search_sort(params: PropertyIdentifier) -> AttomResponse:
    """Get property ID search and sort examples.

    Returns property ID search and sort examples for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Property ID search and sort information
    """
    log = logger.bind(tool="property_id_search_sort", params=params.model_dump())

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

    log.info("Fetching propertyid - with search & sort examples")

    try:
        response = await client.get("property/id", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching propertyid - with search & sort examples", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


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
