"""ATTOM API MCP Server.

This module provides a MCP server for the ATTOM API.
"""

import logging
import sys
from typing import Dict

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import config
from src.tools import (
    assessment_tools,
    event_tools,
    misc_tools,
    property_tools,
    sale_tools,
    school_tools,
    valuation_tools,
)
from src.tools.property_tools import PropertyDetailParams, PropertyDetailResponse

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
        (
            structlog.processors.JSONRenderer()
            if config.LOG_FORMAT.lower() == "json"
            else structlog.dev.ConsoleRenderer()
        ),
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


# Collect all tools
def collect_tool_functions(module) -> Dict[str, callable]:
    """Collect all tool functions from a module."""
    tools = {}
    for name in dir(module):
        attr = getattr(module, name)
        if callable(attr) and not name.startswith("_"):
            tools[name] = attr
    return tools


# Add MCP routes from property_tools
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


# Dynamically add all tools to FastAPI
tool_modules = [
    property_tools,
    assessment_tools,
    valuation_tools,
    sale_tools,
    event_tools,
    misc_tools,
    school_tools,
]

mcp_tools = []
for module in tool_modules:
    tools = collect_tool_functions(module)
    for name, func in tools.items():
        if name not in [
            "property_address",
            "property_detail",
            "property_basic_profile",
            "property_expanded_profile",
            "property_detail_with_schools",
        ]:
            # Add function to mcp_tools for the spec
            mcp_tools.append(
                {
                    "name": name,
                    "description": func.__doc__,
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "attom_id": {
                                "type": "string",
                                "description": "ATTOM ID for the property",
                            },
                            "address": {
                                "type": "string",
                                "description": "Full address of the property",
                            },
                            "address1": {
                                "type": "string",
                                "description": "First line of address (e.g., street address)",
                            },
                            "address2": {
                                "type": "string",
                                "description": "Second line of address (e.g., city, state, ZIP)",
                            },
                            "fips": {"type": "string", "description": "FIPS county code"},
                            "apn": {"type": "string", "description": "Assessor Parcel Number"},
                        },
                    },
                }
            )

            # Create a dynamic route handler
            async def create_handler(func):
                params_class = func.__annotations__.get("params", PropertyDetailParams)
                response_class = func.__annotations__.get("return", PropertyDetailResponse)

                async def handler(params: params_class) -> response_class:
                    return await func(params)

                return handler

            # Add route - NOTE: In a real implementation, this would be done dynamically
            # but we'll skip this for now since we're focusing on the UVX build


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
                        "address": {
                            "type": "string",
                            "description": "Full address of the property",
                        },
                        "address1": {
                            "type": "string",
                            "description": "First line of address (e.g., street address)",
                        },
                        "address2": {
                            "type": "string",
                            "description": "Second line of address (e.g., city, state, ZIP)",
                        },
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
                        "address": {
                            "type": "string",
                            "description": "Full address of the property",
                        },
                        "address1": {
                            "type": "string",
                            "description": "First line of address (e.g., street address)",
                        },
                        "address2": {
                            "type": "string",
                            "description": "Second line of address (e.g., city, state, ZIP)",
                        },
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
                        "address": {
                            "type": "string",
                            "description": "Full address of the property",
                        },
                        "address1": {
                            "type": "string",
                            "description": "First line of address (e.g., street address)",
                        },
                        "address2": {
                            "type": "string",
                            "description": "Second line of address (e.g., city, state, ZIP)",
                        },
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
                        "address": {
                            "type": "string",
                            "description": "Full address of the property",
                        },
                        "address1": {
                            "type": "string",
                            "description": "First line of address (e.g., street address)",
                        },
                        "address2": {
                            "type": "string",
                            "description": "Second line of address (e.g., city, state, ZIP)",
                        },
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
                        "address": {
                            "type": "string",
                            "description": "Full address of the property",
                        },
                        "address1": {
                            "type": "string",
                            "description": "First line of address (e.g., street address)",
                        },
                        "address2": {
                            "type": "string",
                            "description": "Second line of address (e.g., city, state, ZIP)",
                        },
                        "fips": {"type": "string", "description": "FIPS county code"},
                        "apn": {"type": "string", "description": "Assessor Parcel Number"},
                    },
                },
            },
        ]
        + mcp_tools,
    }
    return spec


# MCP instance to export for UVX
mcp = app


def main() -> None:
    """Run the MCP server.
    
    This function is used as the entry point for the CLI tool.
    When using uvx, this function will be called directly.
    """
    import argparse
    import uvicorn

    logger = structlog.get_logger(__name__)
    logger.info("Starting ATTOM API MCP Server")

    # Parse command line arguments for flexible configuration
    parser = argparse.ArgumentParser(description="ATTOM API MCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--log-level", default=config.LOG_LEVEL.lower(), 
                       help="Logging level (debug, info, warning, error)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on code changes")
    
    # Parse arguments but allow for direct invocation without arguments
    try:
        args, _ = parser.parse_known_args()
    except SystemExit:
        # If parsing fails, use defaults
        class DefaultArgs:
            host = "0.0.0.0"
            port = 8000
            log_level = config.LOG_LEVEL.lower()
            reload = False
        args = DefaultArgs()

    # Check if API key is set
    if not config.ATTOM_API_KEY:
        logger.error("ATTOM_API_KEY environment variable is required")
        sys.exit(1)

    # Start the server
    uvicorn.run(
        "src.server:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
