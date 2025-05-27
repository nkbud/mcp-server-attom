from fastmcp import FastMCP
from .property import register_property_routes
from .area import register_area_routes
from .poi import register_poi_routes
from .community import register_community_routes
from .school import register_school_routes


def register_all_routes(app: FastMCP):
    """Register all API routes with the FastMCP application"""
    
    # Register routes for each API category
    register_property_routes(app)
    register_area_routes(app)
    register_poi_routes(app)
    register_community_routes(app)
    register_school_routes(app)