from fastmcp import FastMCP, Request, Response, Path, Query
from typing import Optional, List, Dict, Any
import logging
from ...core.config import settings
from ..models.school import SchoolType, School, SchoolDistrict, SchoolRating

logger = logging.getLogger(__name__)

# Mock data for demonstration purposes
MOCK_SCHOOLS = [
    {
        "school_id": "12345",
        "geo_id_v4": "9c6bded31fd0e089485f276acb947875",
        "name": "Anaheim High School",
        "address": "811 W Lincoln Ave",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92805",
        "latitude": 33.8324,
        "longitude": -117.9241,
        "school_type": "High",
        "grades": "9-12",
        "student_count": 2450,
        "student_teacher_ratio": 23.5,
        "rating": {
            "rating": 7,
            "year": 2022,
            "source": "GreatSchools"
        },
        "district_name": "Anaheim Union High School District",
        "district_id": "0606720",
        "phone": "714-555-1234",
        "website": "https://ahs.auhsd.us",
        "distance": 2.1
    },
    {
        "school_id": "67890",
        "geo_id_v4": "54dfabc123fd0e089485f276a987654",
        "name": "South Junior High School",
        "address": "2320 E South St",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92806",
        "latitude": 33.8192,
        "longitude": -117.8826,
        "school_type": "Middle",
        "grades": "7-8",
        "student_count": 1250,
        "student_teacher_ratio": 22.0,
        "rating": {
            "rating": 6,
            "year": 2022,
            "source": "GreatSchools"
        },
        "district_name": "Anaheim Elementary School District",
        "district_id": "0606710",
        "phone": "714-555-5678",
        "website": "https://sjhs.auesd.us",
        "distance": 1.5
    }
]

MOCK_SCHOOL_DISTRICT = {
    "district_id": "0606720",
    "geo_id_v4": "8370d93a17ba7fb07f115392bd1225d9",
    "name": "Anaheim Union High School District",
    "state": "CA",
    "student_count": 30000,
    "school_count": 19,
    "rating": {
        "rating": 7,
        "year": 2022,
        "source": "GreatSchools"
    }
}


def register_school_routes(app: FastMCP):
    """Register all school API routes"""
    
    @app.get("/v4/school/profile")
    async def school_profile(
        request: Request,
        geo_id_v4: str = Query(..., alias="geoIdv4")
    ) -> Response:
        """
        Get school profile information
        
        Args:
            geo_id_v4: Geographic ID v4 for the school
            
        Returns:
            Detailed school information
        """
        logger.info(f"School profile request: geoIdv4={geo_id_v4}")
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll find a matching school in our mock data or return 404
        school = next((s for s in MOCK_SCHOOLS if s["geo_id_v4"] == geo_id_v4), None)
        
        if not school:
            return Response(
                status_code=404,
                content={
                    "status": "error",
                    "code": 404,
                    "message": f"School with geoIdv4 {geo_id_v4} not found."
                }
            )
        
        # Return mock data
        response_data = {
            "status": "success",
            "school": school
        }
        
        return Response(
            content=response_data
        )
    
    @app.get("/v4/school/district")
    async def school_district(
        request: Request,
        geo_id_v4: str = Query(..., alias="geoIdv4")
    ) -> Response:
        """
        Get school district information
        
        Args:
            geo_id_v4: Geographic ID v4 for the school district
            
        Returns:
            Detailed school district information
        """
        logger.info(f"School district request: geoIdv4={geo_id_v4}")
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll check if the geo_id_v4 matches our mock district
        if geo_id_v4 == MOCK_SCHOOL_DISTRICT["geo_id_v4"]:
            district_data = MOCK_SCHOOL_DISTRICT.copy()
        else:
            return Response(
                status_code=404,
                content={
                    "status": "error",
                    "code": 404,
                    "message": f"School district with geoIdv4 {geo_id_v4} not found."
                }
            )
        
        # Return mock data
        response_data = {
            "status": "success",
            "district": district_data
        }
        
        return Response(
            content=response_data
        )
    
    @app.get("/v4/school/search")
    async def school_search(
        request: Request,
        radius: float = Query(5.0, gt=0),
        geo_id_v4: Optional[str] = Query(None, alias="geoIdv4"),
        latitude: Optional[float] = Query(None),
        longitude: Optional[float] = Query(None),
        school_type: Optional[SchoolType] = Query(None, alias="schoolType"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize")
    ) -> Response:
        """
        Search for schools
        
        Args:
            radius: Search radius in miles
            geo_id_v4: Geographic ID v4 to search around
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            school_type: Type of school (Elementary, Middle, High, etc.)
            page: Page number for pagination
            page_size: Number of results per page
            
        Returns:
            Schools matching the search criteria
        """
        logger.info(f"School search request: geo_id_v4={geo_id_v4}, lat/lon={latitude}/{longitude}, radius={radius}")
        
        # Validate that at least geo_id_v4 or lat/lon is provided
        if not geo_id_v4 and (latitude is None or longitude is None):
            return Response(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "message": "Either geoIdv4 or latitude+longitude is required for school search."
                }
            )
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll filter the mock schools based on school_type if provided
        filtered_schools = MOCK_SCHOOLS
        
        if school_type:
            filtered_schools = [s for s in filtered_schools if s["school_type"] == school_type]
        
        # Return mock data
        response_data = {
            "status": "success",
            "schools": filtered_schools,
            "total_records": len(filtered_schools),
            "page": page,
            "page_size": page_size
        }
        
        return Response(
            content=response_data
        )