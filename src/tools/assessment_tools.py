"""MCP tools for the ATTOM Assessment API.

This module provides MCP tools for accessing the Assessment API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier
from src.tools.utils import make_api_call

# Configure logging
logger = structlog.get_logger(__name__)


@mcp.tool()
async def assessment_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get detailed assessment information for a property."""
    return await make_api_call("assessment/detail", params, "assessment_detail")


@mcp.tool()
async def assessment_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get assessment snapshot information."""
    return await make_api_call("assessment/snapshot", params, "assessment_snapshot")


@mcp.tool()
async def assessment_history_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get assessment history detail information."""
    return await make_api_call("assessmenthistory/detail", params, "assessment_history_detail")


