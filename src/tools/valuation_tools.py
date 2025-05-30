"""MCP tools for the ATTOM Valuation API.

This module provides MCP tools for accessing the Valuation API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Valuation Models
class ValuationParams(PropertyIdentifier):
    """Parameters for valuation endpoints."""

    pass


class ValuationResponse(AttomResponse):
    """Response model for valuation endpoints."""

    pass


# AVM Detail Tool
@mcp.tool()
async def avm_detail(params: ValuationParams) -> ValuationResponse:
    """Get detailed AVM (Automated Valuation Model) information.

    Returns detailed AVM data for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Detailed AVM information
    """
    log = logger.bind(tool="avm_detail", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching AVM detail")

    try:
        response = await client.get("avm/detail", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching AVM detail", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# AVM Snapshot Tool
@mcp.tool()
async def avm_snapshot(params: ValuationParams) -> ValuationResponse:
    """Get AVM (Automated Valuation Model) snapshot.

    Returns a snapshot of AVM data for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        AVM snapshot information
    """
    log = logger.bind(tool="avm_snapshot", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching AVM snapshot")

    try:
        response = await client.get("avm/snapshot", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching AVM snapshot", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# AVM History Detail Tool
@mcp.tool()
async def avm_history_detail(params: ValuationParams) -> ValuationResponse:
    """Get AVM (Automated Valuation Model) history.

    Returns historical AVM data for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        AVM history information
    """
    log = logger.bind(tool="avm_history_detail", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching AVM history detail")

    try:
        response = await client.get("avmhistory/detail", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching AVM history detail", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# ATTOM AVM Tool
@mcp.tool()
async def attom_avm_detail(params: ValuationParams) -> ValuationResponse:
    """Get ATTOM AVM (Automated Valuation Model) information.

    Returns ATTOM's proprietary AVM data for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        ATTOM AVM information
    """
    log = logger.bind(tool="attom_avm_detail", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching ATTOM AVM detail")

    try:
        response = await client.get("attomavm/detail", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching ATTOM AVM detail", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Home Equity Tool
@mcp.tool()
async def home_equity(params: ValuationParams) -> ValuationResponse:
    """Get home equity information.

    Returns home equity data for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Home equity information
    """
    log = logger.bind(tool="home_equity", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching home equity information")

    try:
        response = await client.get("valuation/homeequity", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching home equity information", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Rental AVM Tool
@mcp.tool()
async def rental_avm(params: ValuationParams) -> ValuationResponse:
    """Get rental AVM (Automated Valuation Model) information.

    Returns rental value estimation for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Rental AVM information
    """
    log = logger.bind(tool="rental_avm", params=params.model_dump())

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
        return ValuationResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching rental AVM information")

    try:
        response = await client.get("valuation/rentalavm", request_params)
        return ValuationResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching rental AVM information", error=str(e))
        return ValuationResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
