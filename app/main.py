from fastmcp import FastMCP, Context
import logging
from typing import Optional, Dict, Any, List, Union
from .core.config import settings, logger
from .api.models.property import PropertyDetail
from .api.models.area import Area, Boundary, AreaHierarchy
from .api.models.poi import POI, POICategory
from .api.models.community import Community
from .api.models.school import School, SchoolDistrict


# Mock data for demonstration purposes
MOCK_PROPERTY = {
    "attomId": "145423726",
    "property_id": "145423726",
    "address": {
        "street_address": "7804 N MILTON ST",
        "city": "SPOKANE",
        "state": "WA",
        "zip_code": "99208",
        "county": "SPOKANE"
    },
    "property_type": "SINGLE FAMILY RESIDENCE",
    "year_built": 1994,
    "beds": 3,
    "baths": 2.5,
    "universal_size": 1800,
    "lot_size": 0.25,
    "legal_description": "LOT 1 BLK 2 MILTON HEIGHTS 1ST ADD",
    "owner_name": "JOHN DOE",
    "owner_occupied": True,
    "tax_id": "12345",
    "apn": "26252.2605",
    "fips": "53063",
    "assessments": [
        {
            "year": 2022,
            "land_value": 80000,
            "improvement_value": 220000,
            "total_value": 300000
        }
    ],
    "sales_history": [
        {
            "sale_date": "2020-06-15",
            "sale_price": 275000,
            "sale_type": "RESALE",
            "buyer_name": "JOHN DOE",
            "seller_name": "JANE SMITH"
        }
    ],
    "avm": {
        "value": 310000,
        "high_value": 325000,
        "low_value": 295000,
        "confidence_score": 85
    }
}

MOCK_AREA = {
    "geo_id": "CO06059",
    "geo_id_v4": "baa5d7de09afdefd0ffcd66b581991de",
    "name": "ORANGE COUNTY",
    "type": "CO",
    "centroid": {
        "latitude": 33.7175,
        "longitude": -117.8311
    }
}

# Create FastMCP app instance
app = FastMCP(
    name=settings.API_TITLE,
    instructions=settings.API_DESCRIPTION,
)


# Authentication helper
def validate_api_key(context: Context) -> Optional[Dict[str, Any]]:
    """
    Validate API key from request context
    
    Args:
        context: The FastMCP context
        
    Returns:
        Error response if authentication fails, None if successful
    """
    # Get API key from headers
    api_key = context.request.headers.get(settings.API_KEY_HEADER)
    
    # Validate API key
    if not api_key:
        logger.warning(f"Missing API key in request")
        return {
            "status": "error",
            "code": 401,
            "message": f"Missing API key. Please provide the '{settings.API_KEY_HEADER}' header."
        }
    
    if api_key not in settings.API_KEYS:
        logger.warning(f"Invalid API key used")
        return {
            "status": "error",
            "code": 403,
            "message": "Invalid API key. Please provide a valid API key."
        }
    
    return None


# Property API tools
@app.tool(
    name="property_detail",
    description="Get detailed information about a property by various identifiers"
)
async def property_detail(
    context: Context,
    attom_id: Optional[str] = None,
    address: Optional[str] = None,
    address1: Optional[str] = None,
    address2: Optional[str] = None,
    fips: Optional[str] = None,
    apn: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get detailed property information
    
    Args:
        context: The FastMCP context
        attom_id: ATTOM ID of the property
        address: Full property address
        address1: First line of property address
        address2: Second line of property address (city, state, zip)
        fips: FIPS code
        apn: Assessor's Parcel Number
        
    Returns:
        Property detail information
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Property detail request: AttomID={attom_id}, address={address}")
    
    # Validate that at least one identifier is provided
    if not any([attom_id, address, (address1 and address2), (fips and apn)]):
        return {
            "status": "error",
            "code": 400,
            "message": "At least one property identifier is required. Please provide AttomID, address, address1+address2, or fips+apn."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, we'll return mock data
    property_data = MOCK_PROPERTY.copy()
    
    # If attomID is provided and doesn't match our mock, simulate not found
    if attom_id and attom_id != MOCK_PROPERTY["attomId"]:
        return {
            "status": "error",
            "code": 404,
            "message": f"Property with AttomID {attom_id} not found."
        }
    
    # Return mock data
    return {
        "status": "success",
        "property": property_data
    }


@app.tool(
    name="property_snapshot",
    description="Get basic property information snapshot"
)
async def property_snapshot(
    context: Context,
    attom_id: Optional[str] = None,
    address: Optional[str] = None,
    address1: Optional[str] = None,
    address2: Optional[str] = None,
    fips: Optional[str] = None,
    apn: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get basic property information snapshot
    
    Args:
        context: The FastMCP context
        attom_id: ATTOM ID of the property
        address: Full property address
        address1: First line of property address
        address2: Second line of property address (city, state, zip)
        fips: FIPS code
        apn: Assessor's Parcel Number
        
    Returns:
        Property snapshot information
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Property snapshot request: AttomID={attom_id}, address={address}")
    
    # Validate that at least one identifier is provided
    if not any([attom_id, address, (address1 and address2), (fips and apn)]):
        return {
            "status": "error",
            "code": 400,
            "message": "At least one property identifier is required. Please provide AttomID, address, address1+address2, or fips+apn."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, return a simplified version of the mock data
    property_data = {
        "property_id": MOCK_PROPERTY["property_id"],
        "address": MOCK_PROPERTY["address"],
        "property_type": MOCK_PROPERTY["property_type"],
        "year_built": MOCK_PROPERTY["year_built"],
        "beds": MOCK_PROPERTY["beds"],
        "baths": MOCK_PROPERTY["baths"],
        "universal_size": MOCK_PROPERTY["universal_size"],
        "lot_size": MOCK_PROPERTY["lot_size"],
    }
    
    # Return mock data
    return {
        "status": "success",
        "property": property_data
    }


@app.tool(
    name="property_search",
    description="Search for properties by various criteria"
)
async def property_search(
    context: Context,
    attom_id: Optional[str] = None,
    address: Optional[str] = None,
    address1: Optional[str] = None,
    address2: Optional[str] = None,
    fips: Optional[str] = None,
    apn: Optional[str] = None,
    property_type: Optional[str] = None,
    postal_code: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    """
    Search for properties by identifier or criteria
    
    Args:
        context: The FastMCP context
        attom_id: ATTOM ID of the property
        address: Full property address
        address1: First line of property address
        address2: Second line of property address (city, state, zip)
        fips: FIPS code
        apn: Assessor's Parcel Number
        property_type: Type of property
        postal_code: ZIP/Postal code
        page: Page number for pagination
        page_size: Number of results per page
        
    Returns:
        List of properties matching criteria
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Property search request: AttomID={attom_id}, address={address}, postalcode={postal_code}")
    
    # For search, if specific ID is provided, return single property
    if any([attom_id, address, (address1 and address2), (fips and apn)]):
        # Mock single property response
        property_data = {
            "property_id": MOCK_PROPERTY["property_id"],
            "address": MOCK_PROPERTY["address"],
            "property_type": MOCK_PROPERTY["property_type"],
            "year_built": MOCK_PROPERTY["year_built"],
            "beds": MOCK_PROPERTY["beds"],
            "baths": MOCK_PROPERTY["baths"],
            "universal_size": MOCK_PROPERTY["universal_size"],
            "lot_size": MOCK_PROPERTY["lot_size"],
        }
        
        return {
            "status": "success",
            "property": [property_data],
            "total_matches": 1,
            "page": 1,
            "page_size": 1,
            "total_pages": 1
        }
    else:
        # Mock search response with multiple properties
        properties = [
            {
                "property_id": MOCK_PROPERTY["property_id"],
                "address": MOCK_PROPERTY["address"],
                "property_type": MOCK_PROPERTY["property_type"],
                "year_built": MOCK_PROPERTY["year_built"],
                "beds": MOCK_PROPERTY["beds"],
                "baths": MOCK_PROPERTY["baths"],
                "universal_size": MOCK_PROPERTY["universal_size"],
                "lot_size": MOCK_PROPERTY["lot_size"],
            },
            {
                "property_id": "158832785",
                "address": {
                    "street_address": "15530 N TATUM BLVD",
                    "city": "PHOENIX",
                    "state": "AZ",
                    "zip_code": "85032",
                    "county": "MARICOPA"
                },
                "property_type": "CONDOMINIUM",
                "year_built": 2005,
                "beds": 2,
                "baths": 2.0,
                "universal_size": 1200,
                "lot_size": 0.1,
            }
        ]
        
        return {
            "status": "success",
            "properties": properties,
            "total_matches": 2,
            "page": page,
            "page_size": page_size,
            "total_pages": 1
        }


# Area API tools
@app.tool(
    name="boundary_detail",
    description="Get boundary details for a geographic area"
)
async def boundary_detail(
    context: Context,
    geo_id_v4: Optional[str] = None,
    area_id: Optional[str] = None,
    format: str = "geojson"
) -> Dict[str, Any]:
    """
    Get boundary detail for a geographic area
    
    Args:
        context: The FastMCP context
        geo_id_v4: Geographic ID v4
        area_id: Legacy area ID
        format: Boundary format (geojson or wkt)
        
    Returns:
        Boundary detail for the specified area
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Boundary detail request: geoIdV4={geo_id_v4}, areaId={area_id}")
    
    # Validate that at least one identifier is provided
    if not any([geo_id_v4, area_id]):
        return {
            "status": "error",
            "code": 400,
            "message": "At least one area identifier is required. Please provide geoIdV4 or areaId."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, we'll return mock data
    boundary_data = {
        "format": format,
        "data": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-117.9781, 33.6602],
                    [-117.7836, 33.6602],
                    [-117.7836, 33.7748],
                    [-117.9781, 33.7748],
                    [-117.9781, 33.6602]
                ]
            ]
        }
    }
    
    # Return mock data
    return {
        "status": "success",
        "boundary": boundary_data
    }


@app.tool(
    name="hierarchy_lookup",
    description="Look up geographic hierarchy for a location"
)
async def hierarchy_lookup(
    context: Context,
    wkt_string: Optional[str] = None,
    geo_type: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> Dict[str, Any]:
    """
    Look up the geographic hierarchy for a point
    
    Args:
        context: The FastMCP context
        wkt_string: WKT string representation of a point
        geo_type: Geography type filter
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Geographic hierarchy for the specified point
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Hierarchy lookup request: lat={latitude}, lon={longitude}")
    
    # Validate that either wkt_string or lat/lon is provided
    if not any([wkt_string, (latitude is not None and longitude is not None)]):
        return {
            "status": "error",
            "code": 400,
            "message": "Location information is required. Please provide wktstring or latitude+longitude."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, we'll return mock data
    hierarchy_data = {
        "state": {
            "geo_id": "ST06",
            "geo_id_v4": "e48f70f22d03db973e32c92ca268f891",
            "name": "CALIFORNIA",
            "type": "ST"
        },
        "county": {
            "geo_id": "CO06059",
            "geo_id_v4": "baa5d7de09afdefd0ffcd66b581991de",
            "name": "ORANGE COUNTY",
            "type": "CO"
        },
        "city": {
            "geo_id": "CI0603526",
            "geo_id_v4": "07991e1ba28ff61117434d9a073c4360",
            "name": "ANAHEIM",
            "type": "CI"
        },
        "zip_code": {
            "geo_id": "ZI92802",
            "geo_id_v4": "d87a509d9fc19bbafc4cee730988a18e",
            "name": "92802",
            "type": "ZI"
        },
        "neighborhood": {
            "geo_id": "NB060591401",
            "geo_id_v4": "08f3762070941bf29ff66a3927612f05",
            "name": "ANAHEIM RESORT",
            "type": "NB"
        }
    }
    
    # Return mock data
    return {
        "status": "success",
        "hierarchy": hierarchy_data
    }


# Define more tools for other API categories...
# POI API, Community API, School API, etc.


if __name__ == "__main__":
    # Run the app
    import uvicorn
    
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )