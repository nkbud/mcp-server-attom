"""ATTOM API MCP Server.

This module provides a MCP server for the ATTOM API.
"""

import json
import logging
import sys

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mcp_server import config
from mcp_server.tools import property_tools
from mcp_server.tools.property_tools import PropertyDetailParams, PropertyDetailResponse

# Configure logging
log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer() if config.LOG_FORMAT.lower() == "json" else structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=log_level,
)

# Create FastAPI app
app = FastAPI(
    title="ATTOM API MCP Server",
    description="An MCP server for the ATTOM real estate data API",
    version="0.0.1",
    docs_url="/",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add MCP routes
@app.post("/tools/property_address")
async def api_property_address(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get property address information."""
    return await property_tools.property_address(params)


@app.post("/tools/property_detail")
async def api_property_detail(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get detailed property information."""
    return await property_tools.property_detail(params)


@app.post("/tools/property_basic_profile")
async def api_property_basic_profile(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get basic property profile information."""
    return await property_tools.property_basic_profile(params)


@app.post("/tools/property_expanded_profile")
async def api_property_expanded_profile(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get expanded property profile information."""
    return await property_tools.property_expanded_profile(params)


@app.post("/tools/property_detail_with_schools")
async def api_property_detail_with_schools(params: PropertyDetailParams) -> PropertyDetailResponse:
    """Get property details including school information."""
    return await property_tools.property_detail_with_schools(params)


# OpenAPI specification endpoint for UVX/MCP tooling integration
@app.get("/.well-known/mcp.json")
async def get_mcp_spec():
    """Return the MCP spec for this server."""
    spec = {
        "mcp_server_info": {
            "title": "ATTOM API MCP Server",
            "description": "An MCP server for the ATTOM real estate data API",
            "version": "0.0.1",
        },
        "tools": [
            {
                "name": "property_address",
                "description": property_tools.property_address.__doc__,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                        "address": {"type": "string", "description": "Full address of the property"},
                        "address1": {"type": "string", "description": "First line of address (e.g., street address)"},
                        "address2": {"type": "string", "description": "Second line of address (e.g., city, state, ZIP)"},
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
            {
                "name": "property_detail",
                "description": property_tools.property_detail.__doc__,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                        "address": {"type": "string", "description": "Full address of the property"},
                        "address1": {"type": "string", "description": "First line of address (e.g., street address)"},
                        "address2": {"type": "string", "description": "Second line of address (e.g., city, state, ZIP)"},
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
            {
                "name": "property_basic_profile",
                "description": property_tools.property_basic_profile.__doc__,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                        "address": {"type": "string", "description": "Full address of the property"},
                        "address1": {"type": "string", "description": "First line of address (e.g., street address)"},
                        "address2": {"type": "string", "description": "Second line of address (e.g., city, state, ZIP)"},
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
            {
                "name": "property_expanded_profile",
                "description": property_tools.property_expanded_profile.__doc__,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                        "address": {"type": "string", "description": "Full address of the property"},
                        "address1": {"type": "string", "description": "First line of address (e.g., street address)"},
                        "address2": {"type": "string", "description": "Second line of address (e.g., city, state, ZIP)"},
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
            {
                "name": "property_detail_with_schools",
                "description": property_tools.property_detail_with_schools.__doc__,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                        "address": {"type": "string", "description": "Full address of the property"},
                        "address1": {"type": "string", "description": "First line of address (e.g., street address)"},
                        "address2": {"type": "string", "description": "Second line of address (e.g., city, state, ZIP)"},
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
        ]
    }
    return spec


# MCP instance to export for UVX
mcp = app


def main() -> None:
    """Run the MCP server."""
    import uvicorn
    
    logger = structlog.get_logger(__name__)
    logger.info("Starting ATTOM API MCP Server")
    
    # Check if API key is set
    if not config.ATTOM_API_KEY:
        logger.error("ATTOM_API_KEY environment variable is required")
        sys.exit(1)

    # Start the server
    uvicorn.run(
        "mcp_server.server:app",
        host="0.0.0.0",
        port=8000,
        log_level=config.LOG_LEVEL.lower(),
        reload=False,
    )


if __name__ == "__main__":
    main()