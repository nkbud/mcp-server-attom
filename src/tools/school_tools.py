"""MCP tools for the ATTOM School API.

This module provides MCP tools for accessing the School API endpoints
including school profiles, district information, and school search.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse

# Configure logging
logger = structlog.get_logger(__name__)


# School Models
class SchoolParams:
    """Parameters for school endpoints."""
    def __init__(
        self,
        geoid_v4: str = None,
        radius: float = None,
        latitude: float = None,
        longitude: float = None,
        page: int = None,
        page_size: int = None,
    ):
        self.geoid_v4 = geoid_v4
        self.radius = radius
        self.latitude = latitude
        self.longitude = longitude
        self.page = page
        self.page_size = page_size


class SchoolResponse(AttomResponse):
    """Response model for school endpoints."""
    pass


# School Profile Tool
@mcp.tool()
async def school_profile(params: SchoolParams) -> SchoolResponse:
    """Get detailed school profile information.

    Returns comprehensive school information including ratings, test scores,
    enrollment data, teacher-student ratios, and other educational metrics.

    Args:
        params: Parameters including geoIdv4 for the school

    Returns:
        Detailed school profile information
    """
    log = logger.bind(tool="school_profile", params=params.__dict__)

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdv4"] = params.geoid_v4
    else:
        log.error("Missing required parameter")
        return SchoolResponse(
            status_code=400,
            status_message="geoIdv4 is required.",
        )

    log.info("Fetching school profile")

    try:
        response = await client.get("v4/school/profile", request_params)
        return SchoolResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching school profile", error=str(e))
        return SchoolResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# School District Tool
@mcp.tool()
async def school_district(params: SchoolParams) -> SchoolResponse:
    """Get school district information.

    Returns information about a school district including boundaries,
    performance metrics, and administrative data.

    Args:
        params: Parameters including geoIdv4 for the school district

    Returns:
        School district information
    """
    log = logger.bind(tool="school_district", params=params.__dict__)

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdv4"] = params.geoid_v4
    else:
        log.error("Missing required parameter")
        return SchoolResponse(
            status_code=400,
            status_message="geoIdv4 is required.",
        )

    log.info("Fetching school district")

    try:
        response = await client.get("v4/school/district", request_params)
        return SchoolResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching school district", error=str(e))
        return SchoolResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# School Search Tool
@mcp.tool()
async def school_search(params: SchoolParams) -> SchoolResponse:
    """Search for schools by location.

    Returns schools within a specified radius of a geographic area or coordinates.
    Supports searching by geoIdv4 (zip code, etc.) or latitude/longitude.

    Args:
        params: Parameters including location (geoIdv4 or lat/lon), radius, pagination

    Returns:
        School search results
    """
    log = logger.bind(tool="school_search", params=params.__dict__)

    # Build request parameters
    request_params = {}
    
    # Location parameters (geoIdv4 or lat/lon)
    if params.geoid_v4:
        request_params["geoIdv4"] = params.geoid_v4
    elif params.latitude is not None and params.longitude is not None:
        request_params["latitude"] = params.latitude
        request_params["longitude"] = params.longitude
    else:
        log.error("Missing required location parameter")
        return SchoolResponse(
            status_code=400,
            status_message="Either geoIdv4 or latitude/longitude is required.",
        )

    # Optional parameters
    if params.radius is not None:
        request_params["radius"] = params.radius
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching school search results")

    try:
        response = await client.get("v4/school/search", request_params)
        return SchoolResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching school search results", error=str(e))
        return SchoolResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )
