"""MCP tools for the ATTOM Valuation API.

This module provides MCP tools for accessing the Valuation API endpoints.
"""

import structlog
from src.mcp_server import mcp

from src.client import client
from src.models import AttomResponse, PropertyIdentifier
from src.tools.utils import make_api_call

# Configure logging
logger = structlog.get_logger(__name__)


@mcp.tool()
async def avm_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get detailed AVM (Automated Valuation Model) information."""
    return await make_api_call("avm/detail", params, "avm_detail")


@mcp.tool()
async def avm_snapshot(params: PropertyIdentifier) -> AttomResponse:
    """Get AVM snapshot information."""
    return await make_api_call("avm/snapshot", params, "avm_snapshot")


@mcp.tool()
async def avm_history_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get AVM history detail information."""
    return await make_api_call("avmhistory/detail", params, "avm_history_detail")


@mcp.tool()
async def attom_avm_detail(params: PropertyIdentifier) -> AttomResponse:
    """Get ATTOM AVM detail information."""
    return await make_api_call("attomavm/detail", params, "attom_avm_detail")


@mcp.tool()
async def home_equity(params: PropertyIdentifier) -> AttomResponse:
    """Get home equity valuation information."""
    return await make_api_call("valuation/homeequity", params, "home_equity")


@mcp.tool()
async def rental_avm(params: PropertyIdentifier) -> AttomResponse:
    """Get rental AVM information."""
    return await make_api_call("valuation/rentalavm", params, "rental_avm")
