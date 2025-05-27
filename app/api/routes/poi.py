from fastmcp import FastMCP, Request, Response, Path, Query
from typing import Optional, List, Dict, Any
import logging
from ...core.config import settings
from ..models.poi import POICategory, POI

logger = logging.getLogger(__name__)

# Mock data for demonstration purposes
MOCK_POIS = [
    {
        "poi_id": "12345",
        "name": "Starbucks",
        "address": "123 Main St",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92802",
        "latitude": 33.8239,
        "longitude": -117.7842,
        "category": {
            "category_id": "5812",
            "category_name": "RESTAURANT",
            "line_of_business": "FOOD SERVICES",
            "industry_name": "RETAIL TRADE"
        },
        "distance": 0.2,
        "phone": "555-1234",
        "website": "https://www.starbucks.com"
    },
    {
        "poi_id": "67890",
        "name": "Target",
        "address": "456 Broadway Ave",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92802",
        "latitude": 33.8304,
        "longitude": -117.7901,
        "category": {
            "category_id": "5311",
            "category_name": "DEPARTMENT STORE",
            "line_of_business": "SHOPPING",
            "industry_name": "RETAIL TRADE"
        },
        "distance": 0.5,
        "phone": "555-5678",
        "website": "https://www.target.com"
    }
]

MOCK_CATEGORIES = [
    {
        "category_id": "5812",
        "category_name": "RESTAURANT",
        "line_of_business": "FOOD SERVICES",
        "industry_name": "RETAIL TRADE"
    },
    {
        "category_id": "5311",
        "category_name": "DEPARTMENT STORE",
        "line_of_business": "SHOPPING",
        "industry_name": "RETAIL TRADE"
    },
    {
        "category_id": "6512",
        "category_name": "REAL ESTATE",
        "line_of_business": "REAL ESTATE",
        "industry_name": "FINANCE"
    },
    {
        "category_id": "8211",
        "category_name": "SCHOOL",
        "line_of_business": "EDUCATION",
        "industry_name": "SERVICES"
    },
    {
        "category_id": "7992",
        "category_name": "PARK",
        "line_of_business": "RECREATION",
        "industry_name": "SERVICES"
    }
]


def register_poi_routes(app: FastMCP):
    """Register all POI API routes"""
    
    @app.get("/v4/neighborhood/poi")
    async def poi_search(
        request: Request,
        point: Optional[str] = Query(None),
        address: Optional[str] = Query(None),
        latitude: Optional[float] = Query(None),
        longitude: Optional[float] = Query(None),
        radius: float = Query(1.0, gt=0),
        zipcode: Optional[str] = Query(None),
        category_name: Optional[str] = Query(None, alias="categoryName"),
        line_of_business_name: Optional[str] = Query(None, alias="LineOfBusinessName"),
        industry_name: Optional[str] = Query(None, alias="IndustryName"),
        category_id: Optional[str] = Query(None, alias="CategoryId"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=500, alias="pageSize")
    ) -> Response:
        """
        Search for points of interest
        
        Args:
            point: WKT point string (e.g., "POINT(-74.019215 40.706554)")
            address: Address to search near
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in miles
            zipcode: ZIP code to search within
            category_name: POI category name
            line_of_business_name: Line of business name
            industry_name: Industry name
            category_id: POI category ID
            page: Page number for pagination
            page_size: Number of results per page
            
        Returns:
            Points of interest matching the search criteria
        """
        logger.info(f"POI search request: point={point}, address={address}, lat/lon={latitude}/{longitude}, radius={radius}")
        
        # Validate that at least one location parameter is provided
        if not any([point, address, (latitude is not None and longitude is not None), zipcode]):
            return Response(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "message": "At least one location parameter is required. Please provide point, address, latitude+longitude, or zipcode."
                }
            )
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll filter the mock data based on provided parameters
        filtered_pois = MOCK_POIS
        
        # Apply filtering based on category parameters if provided
        if category_name:
            filtered_pois = [poi for poi in filtered_pois if poi["category"]["category_name"] == category_name]
        
        if line_of_business_name:
            filtered_pois = [poi for poi in filtered_pois if poi["category"]["line_of_business"] == line_of_business_name]
        
        if industry_name:
            filtered_pois = [poi for poi in filtered_pois if poi["category"]["industry_name"] == industry_name]
        
        if category_id:
            filtered_pois = [poi for poi in filtered_pois if poi["category"]["category_id"] == category_id]
        
        # Return mock data
        response_data = {
            "status": "success",
            "pois": filtered_pois,
            "total_records": len(filtered_pois),
            "page": page,
            "page_size": page_size
        }
        
        return Response(
            content=response_data
        )
    
    @app.get("/v4/neighborhood/poi/categorylookup")
    async def poi_category_lookup(
        request: Request,
        category: Optional[str] = Query(None),
        lineofbusiness: Optional[str] = Query(None),
        industry: Optional[str] = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pagesize")
    ) -> Response:
        """
        Look up POI categories
        
        Args:
            category: Category name to filter by
            lineofbusiness: Line of business to filter by
            industry: Industry to filter by
            page: Page number for pagination
            page_size: Number of results per page
            
        Returns:
            POI categories matching the filter criteria
        """
        logger.info(f"POI category lookup request: category={category}, lineofbusiness={lineofbusiness}, industry={industry}")
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll filter the mock data based on provided parameters
        filtered_categories = MOCK_CATEGORIES
        
        if category:
            filtered_categories = [cat for cat in filtered_categories if cat["category_name"] == category]
        
        if lineofbusiness:
            filtered_categories = [cat for cat in filtered_categories if cat["line_of_business"] == lineofbusiness]
        
        if industry:
            filtered_categories = [cat for cat in filtered_categories if cat["industry_name"] == industry]
        
        # Return mock data
        response_data = {
            "status": "success",
            "categories": filtered_categories,
            "total_records": len(filtered_categories),
            "page": page,
            "page_size": page_size
        }
        
        return Response(
            content=response_data
        )