"""MCP tools for the ATTOM API.

This module registers all tools for the MCP server.
"""

from src.tools import property_tools

# Define tool specs
TOOL_SPECS = [
    {
        "name": "property_address",
        "description": property_tools.property_address.__doc__,
        "function": property_tools.property_address,
        "parameters": {
            "type": "object",
            "properties": {
                "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                "address": {"type": "string", "description": "Full address of the property"},
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
        "function": property_tools.property_detail,
        "parameters": {
            "type": "object",
            "properties": {
                "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                "address": {"type": "string", "description": "Full address of the property"},
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
        "function": property_tools.property_basic_profile,
        "parameters": {
            "type": "object",
            "properties": {
                "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                "address": {"type": "string", "description": "Full address of the property"},
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
        "function": property_tools.property_expanded_profile,
        "parameters": {
            "type": "object",
            "properties": {
                "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                "address": {"type": "string", "description": "Full address of the property"},
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
        "function": property_tools.property_detail_with_schools,
        "parameters": {
            "type": "object",
            "properties": {
                "attom_id": {"type": "string", "description": "ATTOM ID for the property"},
                "address": {"type": "string", "description": "Full address of the property"},
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
