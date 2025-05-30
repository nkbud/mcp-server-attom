"""MCP tools for the ATTOM Assessment API.

This module provides MCP tools for accessing the Assessment API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier

# Configure logging
logger = structlog.get_logger(__name__)


# Assessment Models
class AssessmentParams(PropertyIdentifier):
    """Parameters for assessment endpoints."""

    pass


class AssessmentResponse(AttomResponse):
    """Response model for assessment endpoints."""

    pass


# Assessment Detail Tool
@mcp.tool()
async def assessment_detail(params: AssessmentParams) -> AssessmentResponse:
    """Get detailed assessment information for a property.

    Returns detailed assessment information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Detailed assessment information
    """
    log = logger.bind(tool="assessment_detail", params=params.model_dump())

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
        return AssessmentResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching assessment detail")

    try:
        response = await client.get("assessment/detail", request_params)
        return AssessmentResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching assessment detail", error=str(e))
        return AssessmentResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Assessment Snapshot Tool
@mcp.tool()
async def assessment_snapshot(params: AssessmentParams) -> AssessmentResponse:
    """Get assessment snapshot for a property.

    Returns a snapshot of assessment information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Assessment snapshot information
    """
    log = logger.bind(tool="assessment_snapshot", params=params.model_dump())

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
        return AssessmentResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching assessment snapshot")

    try:
        response = await client.get("assessment/snapshot", request_params)
        return AssessmentResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching assessment snapshot", error=str(e))
        return AssessmentResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Assessment History Detail Tool
@mcp.tool()
async def assessment_history_detail(params: AssessmentParams) -> AssessmentResponse:
    """Get assessment history for a property.

    Returns detailed assessment history information for a specific property.

    Args:
        params: Parameters to identify the property

    Returns:
        Assessment history information
    """
    log = logger.bind(tool="assessment_history_detail", params=params.model_dump())

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
        return AssessmentResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info("Fetching assessment history detail")

    try:
        response = await client.get("assessmenthistory/detail", request_params)
        return AssessmentResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching assessment history detail", error=str(e))
        return AssessmentResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
