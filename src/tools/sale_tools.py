"""MCP tools for the ATTOM Sales API.

This module provides MCP tools for accessing the Sales API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier
from src.tools.utils import make_api_call

# Configure logging
logger = structlog.get_logger(__name__)


@mcp.tool()
async def sale_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get detailed sales information for a property."""
    return await make_api_call("sale/detail", params, "sale_detail")


@mcp.tool()
async def sale_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get sales snapshot information."""
    return await make_api_call("sale/snapshot", params, "sale_snapshot")


@mcp.tool()
async def sales_history_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get sales history detail information."""
    return await make_api_call("saleshistory/detail", params, "sales_history_detail")


@mcp.tool()
async def sales_history_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get sales history snapshot information."""
    return await make_api_call("saleshistory/snapshot", params, "sales_history_snapshot")


@mcp.tool()
async def sales_comparables(params: PropertyIdentifier) -> AttomResponse:
    """Get sales comparables information."""
    return await make_api_call("salescomparables/", params, "sales_comparables")
