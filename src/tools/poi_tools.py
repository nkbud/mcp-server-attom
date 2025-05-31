"""MCP tools for the ATTOM POI (Points of Interest) API.

This module provides MCP tools for accessing the POI API endpoints
including restaurant, bank, shopping, and other business location data.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse

# Configure logging
logger = structlog.get_logger(__name__)


# POI Models
class POIParams:
    """Parameters for POI endpoints."""
    def __init__(
        self,
        address: str = None,
        point: str = None,
        latitude: float = None,
        longitude: float = None,
        radius: float = None,
        category_name: str = None,
        line_of_business_name: str = None,
        industry_name: str = None,
        category_id: str = None,
        zipcode: str = None,
        page: int = None,
        page_size: int = None,
        category: str = None,
        lineofbusiness: str = None,
        industry: str = None,
    ):
        self.address = address
        self.point = point
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.category_name = category_name
        self.line_of_business_name = line_of_business_name
        self.industry_name = industry_name
        self.category_id = category_id
        self.zipcode = zipcode
        self.page = page
        self.page_size = page_size
        self.category = category
        self.lineofbusiness = lineofbusiness
        self.industry = industry


class POIResponse(AttomResponse):
    """Response model for POI endpoints."""
    pass


# POI Search Tool
@mcp.tool()
async def poi_search(params: POIParams) -> POIResponse:
    """Search for Points of Interest by location.

    Returns POI data including restaurants, banks, shopping centers and other
    businesses within a specified radius of an address or geographic point.
    Supports filtering by business category, line of business, and industry.

    Args:
        params: Parameters including address/point/coordinates, radius, and filters

    Returns:
        POI search results with business information
    """
    log = logger.bind(tool="poi_search", params=params.__dict__)

    # Build request parameters
    request_params = {}
    
    # Location parameters (address, point, or lat/lon)
    if params.address:
        request_params["address"] = params.address
    elif params.point:
        request_params["point"] = params.point
    elif params.latitude is not None and params.longitude is not None:
        request_params["latitude"] = params.latitude
        request_params["longitude"] = params.longitude
    elif params.zipcode:
        request_params["zipcode"] = params.zipcode
    else:
        log.error("Missing required location parameter")
        return POIResponse(
            status_code=400,
            status_message="One of address, point, latitude/longitude, or zipcode is required.",
        )

    # Optional filter parameters
    if params.radius is not None:
        request_params["radius"] = params.radius
    if params.category_name:
        request_params["categoryName"] = params.category_name
    if params.line_of_business_name:
        request_params["LineOfBusinessName"] = params.line_of_business_name
    if params.industry_name:
        request_params["IndustryName"] = params.industry_name
    if params.category_id:
        request_params["CategoryId"] = params.category_id
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching POI search results")

    try:
        response = await client.get("v4/neighborhood/poi", request_params)
        return POIResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching POI search results", error=str(e))
        return POIResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# POI Category Lookup Tool
@mcp.tool()
async def poi_category_lookup(params: POIParams) -> POIResponse:
    """Get POI category, line of business, and industry information.

    Returns reference data about business categories, lines of business,
    and industry classifications available for POI filtering.

    Args:
        params: Parameters for filtering category lookups

    Returns:
        POI category and classification information
    """
    log = logger.bind(tool="poi_category_lookup", params=params.__dict__)

    # Build request parameters
    request_params = {}
    if params.category:
        request_params["category"] = params.category
    if params.lineofbusiness:
        request_params["lineofbusiness"] = params.lineofbusiness
    if params.industry:
        request_params["industry"] = params.industry
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pagesize"] = params.page_size

    log.info("Fetching POI category lookup")

    try:
        response = await client.get("v4/neighborhood/poi/categorylookup", request_params)
        return POIResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching POI category lookup", error=str(e))
        return POIResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )