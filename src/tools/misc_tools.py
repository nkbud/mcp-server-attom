"""MCP tools for the ATTOM API Misc endpoints.

This module provides MCP tools for accessing the Misc API endpoints.
"""

from typing import Any, Dict, Optional

import structlog
from pydantic import BaseModel, Field
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Define parameter and response models
class MiscParams(PropertyIdentifier):
    """Parameters for misc endpoints."""
    pass


class MiscResponse(AttomResponse):
    """Response model for misc endpoints."""
    pass


@mcp.tool()
async def enumerations_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get enumerations detail information.
    
    Returns enumerations detail information including field definitions
    and valid values for various property data fields.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Enumerations detail information
    """
    log = logger.bind(tool="enumerations_detail", params=params.model_dump())
    
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching enumerations detail")
    
    try:
        response = await client.get("enumerations/Detail", request_params)
        return AttomResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching enumerations detail", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def transportation_noise(params: PropertyIdentifier) -> AttomResponse:
    """Get transportation noise information.
    
    Returns transportation noise information for a specific property
    including noise levels from airports, highways, and railways.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Transportation noise information
    """
    log = logger.bind(tool="transportation_noise", params=params.model_dump())
    
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching transportation noise")
    
    try:
        response = await client.get("transportationnoise", request_params)
        return AttomResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching transportation noise", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


@mcp.tool()
async def preforeclosure_details(params: PropertyIdentifier) -> AttomResponse:
    """Get preforeclosure details information.
    
    Returns preforeclosure details information for a specific property
    including foreclosure status, timeline, and related data.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Preforeclosure details information
    """
    log = logger.bind(tool="preforeclosure_details", params=params.model_dump())
    
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching preforeclosure details")
    
    try:
        response = await client.get("preforeclosuredetails", request_params)
        return AttomResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching preforeclosure details", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
