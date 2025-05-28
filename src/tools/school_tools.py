"""MCP tools for the ATTOM API School endpoints.

This module provides MCP tools for accessing the School API endpoints.
"""

import structlog

from src.client import client
from src.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Define parameter and response models
class SchoolParams(PropertyIdentifier):
    """Parameters for school endpoints."""

    pass


class SchoolResponse(AttomResponse):
    """Response model for school endpoints."""

    pass


async def school(params: PropertyIdentifier) -> AttomResponse:
    """Get school information.

    Returns school information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        School information
    """
    log = logger.bind(tool="school", params=params.model_dump())

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

    log.info("Fetching school")

    try:
        response = await client.get("school", request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching school", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
