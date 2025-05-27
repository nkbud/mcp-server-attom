"""MCP tools for the ATTOM Property API.

This module provides MCP tools for accessing the Property API endpoints.
"""

from typing import Any, Dict, Optional

import structlog
from pydantic import BaseModel, Field

from mcp_server.client import client
from mcp_server.models import AttomResponse, PropertyIdentifier

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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching property address")
    
    try:
        response = await client.get("property/address", request_params)
        return PropertyDetailResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching property detail")
    
    try:
        response = await client.get("property/detail", request_params)
        return PropertyDetailResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching property basic profile")
    
    try:
        response = await client.get("property/basicprofile", request_params)
        return PropertyDetailResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching property expanded profile")
    
    try:
        response = await client.get("property/expandedprofile", request_params)
        return PropertyDetailResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
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
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching property detail with schools")
    
    try:
        response = await client.get("property/detailwithschools", request_params)
        return PropertyDetailResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching property detail with schools", error=str(e))
        return PropertyDetailResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )