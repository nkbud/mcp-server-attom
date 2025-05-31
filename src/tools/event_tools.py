"""MCP tools for the ATTOM API Event endpoints.

This module provides MCP tools for accessing the Event API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier
from src.tools.utils import make_api_call

# Configure logging
logger = structlog.get_logger(__name__)


@mcp.tool()
async def all_events_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get all events detail information."""
    return await make_api_call("allevents/detail", params, "all_events_detail")


@mcp.tool()
async def all_events_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get all events snapshot information."""
    return await make_api_call("allevents/snapshot", params, "all_events_snapshot")
