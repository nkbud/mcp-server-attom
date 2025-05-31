"""ATTOM API MCP Server.

This module provides a MCP server for the ATTOM API.
"""

import logging
import sys

import structlog
from src import config
from src.mcp_server import mcp

# Import all tool modules to register the @mcp.tool decorators
from src.tools import (
    assessment_tools,
    event_tools,
    misc_tools,
    property_tools,
    sale_tools,
    school_tools,
    valuation_tools,
)

# Configure logging
log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    format="%(message)s",
    stream=sys.stderr,
    level=log_level,
)

# Configure structlog to also use stderr
structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(log_level),
    logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
    cache_logger_on_first_use=True,
)


def main() -> None:
    """Run the MCP server.
    
    This function is used as the entry point for the CLI tool.
    When using uvx, this function will be called directly.
    """
    import argparse

    logger = structlog.get_logger(__name__)
    logger.info("Starting ATTOM API MCP Server")

    # Parse command line arguments for flexible configuration
    parser = argparse.ArgumentParser(description="ATTOM API MCP Server")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to"
    )
    parser.add_argument(
        "--log-level", default=config.LOG_LEVEL.lower(), help="Logging level (debug, info, warning, error)"
    )
    
    # Parse arguments but allow for direct invocation without arguments
    try:
        args, _ = parser.parse_known_args()
    except SystemExit:
        # If parsing fails, use defaults
        class DefaultArgs:
            port = 8000
            log_level = config.LOG_LEVEL.lower()
        args = DefaultArgs()

    # Check if API key is set
    if not config.ATTOM_API_KEY:
        logger.error("ATTOM_API_KEY environment variable is required")
        sys.exit(1)

    # Run the MCP server
    logger.info("Running MCP server with STDIO transport")
    mcp.run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()
