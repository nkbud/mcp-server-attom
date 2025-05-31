"""MCP tools for the ATTOM Area and Location API.

This module provides MCP tools for accessing the Area API endpoints
including boundary details, hierarchy lookups, and geographic data.
"""

import structlog
from src.mcp_server import mcp
from typing import Optional

from src.client import client
from src.models import AttomResponse
from pydantic import BaseModel

# Configure logging
logger = structlog.get_logger(__name__)


# Area Models
class AreaParams(BaseModel):
    """Parameters for area endpoints."""
    geoid_v4: Optional[str] = None
    area_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    wkt_string: Optional[str] = None
    geo_type: Optional[str] = None
    state_id: Optional[str] = None
    format: Optional[str] = None
    mime: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class AreaResponse(AttomResponse):
    """Response model for area endpoints."""
    pass


# Boundary Detail Tool
@mcp.tool()
async def boundary_detail(params: AreaParams) -> AreaResponse:
    """Get boundary detail information for a geographic area.

    Returns boundary information including geographic shapes and details
    for counties, cities, neighborhoods, etc.

    Args:
        params: Parameters including geoIdV4, areaId, format (geojson), mime (json)

    Returns:
        Boundary detail information
    """
    log = logger.bind(tool="boundary_detail", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.area_id:
        request_params["areaId"] = params.area_id
    if params.format:
        request_params["format"] = params.format
    if params.mime:
        request_params["mime"] = params.mime

    if not any(request_params.get(key) for key in ["geoIdV4", "areaId"]):
        log.error("Missing required parameter")
        return AreaResponse(
            status_code=400,
            status_message="Either geoIdV4 or areaId is required.",
        )

    log.info("Fetching boundary detail")

    try:
        response = await client.get("areaapi/area/boundary/detail", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching boundary detail", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Hierarchy Lookup Tool
@mcp.tool()
async def hierarchy_lookup(params: AreaParams) -> AreaResponse:
    """Get area hierarchy information for a geographic location.

    Returns all geographic areas that contain the specified location
    (county, city, neighborhood, etc.)

    Args:
        params: Parameters including latitude, longitude, wktstring, geoType

    Returns:
        Area hierarchy information
    """
    log = logger.bind(tool="hierarchy_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.latitude is not None and params.longitude is not None:
        request_params["latitude"] = params.latitude
        request_params["longitude"] = params.longitude
    elif params.wkt_string:
        request_params["wktstring"] = params.wkt_string
    
    if params.geo_type:
        request_params["geoType"] = params.geo_type
    if params.mime:
        request_params["mime"] = params.mime

    if not any([params.latitude is not None and params.longitude is not None, params.wkt_string]):
        log.error("Missing required location parameter")
        return AreaResponse(
            status_code=400,
            status_message="Either latitude/longitude or wktstring is required.",
        )

    log.info("Fetching hierarchy lookup")

    try:
        response = await client.get("areaapi/area/hierarchy/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching hierarchy lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# State Lookup Tool
@mcp.tool()
async def state_lookup(params: AreaParams) -> AreaResponse:
    """Get state information for a geographic area.

    Args:
        params: Parameters including geoIdV4, areaId

    Returns:
        State information
    """
    log = logger.bind(tool="state_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.area_id:
        request_params["areaId"] = params.area_id
    if params.mime:
        request_params["mime"] = params.mime
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching state lookup")

    try:
        response = await client.get("areaapi/area/state/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching state lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# County Lookup Tool
@mcp.tool()
async def county_lookup(params: AreaParams) -> AreaResponse:
    """Get county information for a state.

    Args:
        params: Parameters including stateId, geoIdV4

    Returns:
        County information
    """
    log = logger.bind(tool="county_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.state_id:
        request_params["stateId"] = params.state_id
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.mime:
        request_params["mime"] = params.mime
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching county lookup")

    try:
        response = await client.get("areaapi/area/county/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching county lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# CBSA Lookup Tool
@mcp.tool()
async def cbsa_lookup(params: AreaParams) -> AreaResponse:
    """Get Core Based Statistical Area (CBSA) information.

    Args:
        params: Parameters including stateId, geoIdV4

    Returns:
        CBSA information
    """
    log = logger.bind(tool="cbsa_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.state_id:
        request_params["stateId"] = params.state_id
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.mime:
        request_params["mime"] = params.mime
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching CBSA lookup")

    try:
        response = await client.get("areaapi/area/cbsa/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching CBSA lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# GeoID Lookup Tool
@mcp.tool()
async def geoid_lookup(params: AreaParams) -> AreaResponse:
    """Get geographic ID lookup information.

    Args:
        params: Parameters including geoId, geoIdV4, geoType

    Returns:
        GeoID information
    """
    log = logger.bind(tool="geoid_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.area_id:  # Using area_id as geoId
        request_params["geoId"] = params.area_id
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.geo_type:
        request_params["geoType"] = params.geo_type
    if params.mime:
        request_params["mime"] = params.mime
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pageSize"] = params.page_size

    log.info("Fetching GeoID lookup")

    try:
        response = await client.get("areaapi/area/geoid/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching GeoID lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# GeoCode Legacy Lookup Tool
@mcp.tool()
async def geocode_legacy_lookup(params: AreaParams) -> AreaResponse:
    """Get legacy geocode lookup information.

    Args:
        params: Parameters including geoId, geoIdV4

    Returns:
        Legacy geocode information
    """
    log = logger.bind(tool="geocode_legacy_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.area_id:  # Using area_id as geoId
        request_params["geoId"] = params.area_id
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4

    log.info("Fetching legacy geocode lookup")

    try:
        response = await client.get("areaapi/area/geoId/legacyLookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching legacy geocode lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )


# Location Lookup Tool
@mcp.tool()
async def location_lookup(params: AreaParams) -> AreaResponse:
    """Get location lookup information.

    Args:
        params: Parameters including geoIdV4, geographyTypeAbbreviation

    Returns:
        Location information
    """
    log = logger.bind(tool="location_lookup", params=params.model_dump())

    # Build request parameters
    request_params = {}
    if params.geoid_v4:
        request_params["geoIdV4"] = params.geoid_v4
    if params.geo_type:  # Using geo_type as geographyTypeAbbreviation
        request_params["geographyTypeAbbreviation"] = params.geo_type
    if params.page:
        request_params["page"] = params.page
    if params.page_size:
        request_params["pagesize"] = params.page_size

    log.info("Fetching location lookup")

    try:
        response = await client.get("v4/location/lookup", request_params)
        return AreaResponse(status_code=200, status_message="Success", data=response)
    except Exception as e:
        log.error("Error fetching location lookup", error=str(e))
        return AreaResponse(
            status_code=500,
            status_message=f"Error: {str(e)}",
        )