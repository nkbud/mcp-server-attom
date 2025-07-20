"""Utility functions shared across MCP tools."""

import structlog
from src.client import client
from src.models import AttomResponse, PropertyIdentifier

logger = structlog.get_logger(__name__)


def build_property_params(params: PropertyIdentifier) -> dict:
    """Build request parameters from PropertyIdentifier."""
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
    return request_params


async def make_api_call(endpoint: str, params: PropertyIdentifier, tool_name: str) -> AttomResponse:
    """Make an API call with standardized error handling."""
    log = logger.bind(tool=tool_name, params=params.model_dump())
    
    request_params = build_property_params(params)
    if not request_params:
        log.error("Invalid property identifier")
        return AttomResponse(
            status_code=400,
            status_message="Invalid property identifier. Please provide attom_id, address, address1+address2, or fips+apn.",
        )

    log.info(f"Fetching {tool_name}")

    try:
        response = await client.get(endpoint, request_params)
        return AttomResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error(f"Error fetching {tool_name}", error=str(e))
        return AttomResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )