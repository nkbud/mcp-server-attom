"""Configuration settings for the ATTOM MCP Server.

This module loads environment variables and provides configuration settings
for the ATTOM API client and MCP server.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ATTOM API configuration
ATTOM_API_KEY: str = os.getenv("ATTOM_API_KEY", "")
ATTOM_HOST_URL: str = os.getenv("ATTOM_HOST_URL", "https://api.gateway.attomdata.com")
ATTOM_PROP_API_PREFIX: str = os.getenv("ATTOM_PROP_API_PREFIX", "/propertyapi/v1.0.0")
ATTOM_DLP_V2_PREFIX: str = os.getenv("ATTOM_DLP_V2_PREFIX", "/property/v2")
ATTOM_DLP_V3_PREFIX: str = os.getenv("ATTOM_DLP_V3_PREFIX", "/property/v3")

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")

# In server.py we'll check for the API key when actually running the server
# But we don't validate here to allow tests to run without an API key
