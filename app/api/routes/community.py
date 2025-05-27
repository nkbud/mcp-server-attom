from fastmcp import FastMCP, Request, Response, Path, Query
from typing import Optional, List, Dict, Any
import logging
from ...core.config import settings
from ..models.community import Community, Demographics, NeighborhoodAmenities

logger = logging.getLogger(__name__)

# Mock data for demonstration purposes
MOCK_COMMUNITY = {
    "geo_id": "NB060591401",
    "geo_id_v4": "08f3762070941bf29ff66a3927612f05",
    "name": "ANAHEIM RESORT",
    "city": "ANAHEIM",
    "state": "CA",
    "zip_code": "92802",
    "demographics": {
        "population": 15000,
        "population_density": 3500,
        "median_age": 35.2,
        "median_household_income": 65000,
        "median_home_value": 650000,
        "owner_occupied_percent": 45.5,
        "renter_occupied_percent": 48.3,
        "vacant_percent": 6.2
    },
    "amenities": {
        "poi_count": 237,
        "restaurant_count": 45,
        "shopping_count": 32,
        "nightlife_count": 18,
        "grocery_count": 6,
        "school_count": 8,
        "park_count": 4,
        "transit_count": 12
    },
    "description": "The Anaheim Resort is a tourism district located in Anaheim, California. It is home to the Disneyland Resort, the Anaheim Convention Center, and numerous hotels and restaurants."
}


def register_community_routes(app: FastMCP):
    """Register all community API routes"""
    
    @app.get("/v4.0.0/neighborhood/community")
    async def neighborhood_community(
        request: Request,
        geo_id_v4: str = Query(..., alias="geoIdv4")
    ) -> Response:
        """
        Get neighborhood community information
        
        Args:
            geo_id_v4: Geographic ID v4 for the neighborhood
            
        Returns:
            Neighborhood community information
        """
        logger.info(f"Neighborhood community request: geoIdv4={geo_id_v4}")
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll return mock data if the ID matches, or a 404 if not
        if geo_id_v4 == MOCK_COMMUNITY["geo_id_v4"]:
            community_data = MOCK_COMMUNITY.copy()
        else:
            return Response(
                status_code=404,
                content={
                    "status": "error",
                    "code": 404,
                    "message": f"Neighborhood with geoIdv4 {geo_id_v4} not found."
                }
            )
        
        # Return mock data
        response_data = {
            "status": "success",
            "community": community_data
        }
        
        return Response(
            content=response_data
        )
    
    @app.get("/v4/location/lookup")
    async def location_lookup(
        request: Request,
        geo_id_v4: Optional[str] = Query(None, alias="geoIdV4"),
        name: Optional[str] = Query(None),
        geography_type_abbreviation: Optional[str] = Query(None, alias="geographyTypeAbbreviation"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pagesize")
    ) -> Response:
        """
        Look up locations
        
        Args:
            geo_id_v4: Geographic ID v4
            name: Location name
            geography_type_abbreviation: Geography type abbreviation (e.g., ZI for ZIP code)
            page: Page number for pagination
            page_size: Number of results per page
            
        Returns:
            Locations matching the search criteria
        """
        logger.info(f"Location lookup request: geoIdV4={geo_id_v4}, name={name}, type={geography_type_abbreviation}")
        
        # Validate that at least one search parameter is provided
        if not any([geo_id_v4, name, geography_type_abbreviation]):
            return Response(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "message": "At least one search parameter is required. Please provide geoIdV4, name, or geographyTypeAbbreviation."
                }
            )
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll return mock community data
        communities = [
            {
                "geo_id": "NB060591401",
                "geo_id_v4": "08f3762070941bf29ff66a3927612f05",
                "name": "ANAHEIM RESORT",
                "city": "ANAHEIM",
                "state": "CA",
                "zip_code": "92802",
                "type": "NB",  # Neighborhood
            },
            {
                "geo_id": "CI0603526",
                "geo_id_v4": "07991e1ba28ff61117434d9a073c4360",
                "name": "ANAHEIM",
                "state": "CA",
                "type": "CI",  # City
            }
        ]
        
        # Filter the mock data based on the search parameters
        if geo_id_v4:
            communities = [c for c in communities if c["geo_id_v4"] == geo_id_v4]
        
        if name:
            communities = [c for c in communities if name.upper() in c["name"]]
        
        if geography_type_abbreviation:
            communities = [c for c in communities if c["type"] == geography_type_abbreviation]
        
        # Return mock data
        response_data = {
            "status": "success",
            "communities": communities,
            "total_records": len(communities),
            "page": page,
            "page_size": page_size
        }
        
        return Response(
            content=response_data
        )