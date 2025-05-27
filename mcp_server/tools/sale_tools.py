"""MCP tools for the ATTOM Sales API.

This module provides MCP tools for accessing the Sales API endpoints.
"""

from typing import Any, Dict, Optional

import structlog
from fastmcp import mcp
from pydantic import BaseModel, Field

from mcp_server.client import client
from mcp_server.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Sales Models
class SaleParams(PropertyIdentifier):
    """Parameters for sale endpoints."""
    pass


class SaleResponse(AttomResponse):
    """Response model for sale endpoints."""
    pass


# Sale Detail Tool
@mcp.tool
async def sale_detail(params: SaleParams) -> SaleResponse:
    """Get detailed sales information for a property.
    
    Returns detailed sales information for a specific property.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Detailed sales information
    """
    log = logger.bind(tool="sale_detail", params=params.model_dump())
    
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
        return SaleResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching sale detail")
    
    try:
        response = await client.get("sale/detail", request_params)
        return SaleResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching sale detail", error=str(e))
        return SaleResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Sale Snapshot Tool
@mcp.tool
async def sale_snapshot(params: SaleParams) -> SaleResponse:
    """Get sales snapshot for a property.
    
    Returns a snapshot of sales information for a specific property.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Sales snapshot information
    """
    log = logger.bind(tool="sale_snapshot", params=params.model_dump())
    
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
        return SaleResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching sale snapshot")
    
    try:
        response = await client.get("sale/snapshot", request_params)
        return SaleResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching sale snapshot", error=str(e))
        return SaleResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Sales History Detail Tool
@mcp.tool
async def sales_history_detail(params: SaleParams) -> SaleResponse:
    """Get sales history for a property.
    
    Returns detailed sales history information for a specific property.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Sales history information
    """
    log = logger.bind(tool="sales_history_detail", params=params.model_dump())
    
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
        return SaleResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching sales history detail")
    
    try:
        response = await client.get("saleshistory/detail", request_params)
        return SaleResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching sales history detail", error=str(e))
        return SaleResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Sales History Snapshot Tool
@mcp.tool
async def sales_history_snapshot(params: SaleParams) -> SaleResponse:
    """Get sales history snapshot for a property.
    
    Returns a snapshot of sales history for a specific property.
    
    Args:
        params: Parameters to identify the property
        
    Returns:
        Sales history snapshot information
    """
    log = logger.bind(tool="sales_history_snapshot", params=params.model_dump())
    
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
        return SaleResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn."
        )
    
    log.info("Fetching sales history snapshot")
    
    try:
        response = await client.get("saleshistory/snapshot", request_params)
        return SaleResponse(
            status_code=200,
            status_message="Success",
            data=response
        )
    except Exception as e:
        log.error("Error fetching sales history snapshot", error=str(e))
        return SaleResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )