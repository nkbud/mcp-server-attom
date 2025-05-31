"""MCP tools for the ATTOM Community API.

This module provides MCP tools for accessing the Community API endpoints
including crime, population, education, weather stats, and commuter data.
"""

import structlog
from src.mcp_server import mcp
from typing import Optional

from src.client import client
from src.models import AttomResponse
from pydantic import BaseModel

# Configure logging
logger = structlog.get_logger(__name__)


# Community Models
class CommunityParams(BaseModel):
    """Parameters for community endpoints."""
    geoid_v4: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class CommunityResponse(AttomResponse):
    """Response model for community endpoints."""
    pass


# Neighborhood Community Tool
@mcp.tool()
async def neighborhood_community(params: CommunityParams) -> CommunityResponse:
    """Get comprehensive neighborhood community information.

    Returns detailed community data including crime statistics, population 
    demographics, education metrics, weather stats and averages, and 
    commuter information for a specified geographic area.

    Args:
        params: Parameters including geoIdv4 for the neighborhood

    Returns:
        Comprehensive community data including:
        - Crime statistics and safety metrics
        - Population demographics and statistics  
        - Education data and school information
        - Weather statistics and historical averages
        - Commuter times and transportation data
    """
    log = logger.bind(tool="neighborhood_community", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdv4"] = params.geoid_v4
    else:
        log.error("Missing required parameter")
        return CommunityResponse(
            status_code=400,
            status_message="geoIdv4 is required.",
        )

    log.info("Fetching neighborhood community data")

    try:
        response = await client.get("v4.0.0/neighborhood/community", request_params)
        return CommunityResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching neighborhood community data", error=str(e))
        return CommunityResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )