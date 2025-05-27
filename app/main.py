from fastmcp import FastMCP, Context
import logging
from typing import Optional, Dict, Any, List, Union
from .core.config import settings, logger
from .api.models.property import PropertyDetail
from .api.models.area import Area, Boundary, AreaHierarchy
from .api.models.poi import POI, POICategory
from .api.models.community import Community
from .api.models.school import School, SchoolDistrict, SchoolType


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

# Mock POI data
MOCK_POIS = [
    {
        "poi_id": "12345",
        "name": "Starbucks Coffee",
        "address": "123 Main St",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92802",
        "latitude": 33.8150,
        "longitude": -117.9265,
        "category": {
            "category_id": "9996",
            "category_name": "RESTAURANT",
            "line_of_business": "FOOD & BEVERAGE",
            "industry_name": "COFFEE SHOP"
        },
        "distance": 0.5,
        "phone": "714-555-1234",
        "website": "https://www.starbucks.com",
        "description": "Coffee shop offering a variety of drinks and snacks."
    },
    {
        "poi_id": "67890",
        "name": "Target",
        "address": "456 Orange Ave",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92802",
        "latitude": 33.8200,
        "longitude": -117.9150,
        "category": {
            "category_id": "9997",
            "category_name": "RETAIL",
            "line_of_business": "DEPARTMENT STORE",
            "industry_name": "GENERAL MERCHANDISE"
        },
        "distance": 0.8,
        "phone": "714-555-5678",
        "website": "https://www.target.com",
        "description": "Department store offering a wide range of products."
    }
]

MOCK_POI_CATEGORIES = [
    {
        "category_id": "9996",
        "category_name": "RESTAURANT",
        "line_of_business": "FOOD & BEVERAGE",
        "industry_name": "COFFEE SHOP"
    },
    {
        "category_id": "9997",
        "category_name": "RETAIL",
        "line_of_business": "DEPARTMENT STORE",
        "industry_name": "GENERAL MERCHANDISE"
    },
    {
        "category_id": "9998",
        "category_name": "PERSONAL SERVICES",
        "line_of_business": "MISC SERVICES",
        "industry_name": "BEAUTY SALON"
    },
    {
        "category_id": "9999",
        "category_name": "FINANCIAL",
        "line_of_business": "BANKING",
        "industry_name": "BANK BRANCH"
    }
]

# Mock Community data
MOCK_COMMUNITY = {
    "geo_id": "NB060591401",
    "geo_id_v4": "08f3762070941bf29ff66a3927612f05",
    "name": "ANAHEIM RESORT",
    "city": "ANAHEIM",
    "state": "CA",
    "zip_code": "92802",
    "demographics": {
        "population": 12500,
        "population_density": 5620.5,
        "median_age": 34.2,
        "median_household_income": 68500,
        "median_home_value": 550000,
        "owner_occupied_percent": 45.5,
        "renter_occupied_percent": 48.2,
        "vacant_percent": 6.3
    },
    "amenities": {
        "poi_count": 250,
        "restaurant_count": 45,
        "shopping_count": 35,
        "nightlife_count": 15,
        "grocery_count": 8,
        "school_count": 5,
        "park_count": 3,
        "transit_count": 12
    },
    "description": "The Anaheim Resort is a popular tourist destination known for its proximity to Disneyland and other attractions."
}

# Mock School data
MOCK_SCHOOLS = [
    {
        "school_id": "12345",
        "geo_id_v4": "9c6bded31fd0e089485f276acb947875",
        "name": "Anaheim High School",
        "address": "811 W Lincoln Ave",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92805",
        "latitude": 33.8320,
        "longitude": -117.9265,
        "school_type": "High",
        "grades": "9-12",
        "student_count": 2500,
        "student_teacher_ratio": 24.5,
        "rating": {
            "rating": 8,
            "year": 2022,
            "source": "GreatSchools"
        },
        "district_name": "Anaheim Union High School District",
        "district_id": "12345",
        "phone": "714-555-9876",
        "website": "https://ahs.auhsd.us",
        "distance": 1.2
    },
    {
        "school_id": "67890",
        "geo_id_v4": "8370d93a17ba7fb07f115392bd1225d9",
        "name": "Anaheim Elementary School",
        "address": "123 School St",
        "city": "Anaheim",
        "state": "CA",
        "zip_code": "92805",
        "latitude": 33.8350,
        "longitude": -117.9240,
        "school_type": "Elementary",
        "grades": "K-6",
        "student_count": 850,
        "student_teacher_ratio": 22.0,
        "rating": {
            "rating": 7,
            "year": 2022,
            "source": "GreatSchools"
        },
        "district_name": "Anaheim Elementary School District",
        "district_id": "67890",
        "phone": "714-555-4321",
        "website": "https://aes.aesd.org",
        "distance": 0.9
    }
]

MOCK_SCHOOL_DISTRICT = {
    "district_id": "12345",
    "geo_id_v4": "8370d93a17ba7fb07f115392bd1225d9",
    "name": "Anaheim Union High School District",
    "state": "CA",
    "student_count": 30000,
    "school_count": 20,
    "rating": {
        "rating": 8,
        "year": 2022,
        "source": "GreatSchools"
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

# POI API tools
@app.tool(
    name="poi_search",
    description="Search for points of interest near a location"
)
async def poi_search(
    context: Context,
    point: Optional[str] = None,  # WKT point format: "POINT(lon lat)"
    address: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: float = 1.0,
    zipcode: Optional[str] = None,
    category_name: Optional[str] = None,
    line_of_business_name: Optional[str] = None,
    industry_name: Optional[str] = None,
    category_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Search for points of interest near a location
    
    Args:
        context: The FastMCP context
        point: WKT string representation of a point (e.g., "POINT(-117.9265 33.8150)")
        address: Address to search near
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Radius in miles to search (default: 1.0)
        zipcode: ZIP/Postal code to search within
        category_name: Filter by category name
        line_of_business_name: Filter by line of business
        industry_name: Filter by industry name
        category_id: Filter by category ID
        page: Page number for pagination
        page_size: Number of results per page
        
    Returns:
        List of points of interest near the specified location
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"POI search request: point={point}, address={address}, lat={latitude}, lon={longitude}, radius={radius}")
    
    # Validate that at least one location identifier is provided
    if not any([point, address, (latitude is not None and longitude is not None), zipcode]):
        return {
            "status": "error",
            "code": 400,
            "message": "Location information is required. Please provide point, address, latitude+longitude, or zipcode."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, we'll return mock data
    pois = MOCK_POIS
    
    # Apply category filtering if provided
    if category_name or line_of_business_name or industry_name or category_id:
        filtered_pois = []
        for poi in pois:
            category = poi.get("category", {})
            
            # Check if POI matches any of the filter criteria
            if (not category_name or category.get("category_name") == category_name) and \
               (not line_of_business_name or category.get("line_of_business") == line_of_business_name) and \
               (not industry_name or category.get("industry_name") == industry_name) and \
               (not category_id or category.get("category_id") == category_id):
                filtered_pois.append(poi)
        
        pois = filtered_pois
    
    # Apply pagination
    total_records = len(pois)
    total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    
    pois = pois[start_idx:end_idx]
    
    # Return mock data
    return {
        "status": "success",
        "pois": pois,
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@app.tool(
    name="poi_category_lookup",
    description="Look up POI categories"
)
async def poi_category_lookup(
    context: Context,
    category: Optional[str] = None,
    lineofbusiness: Optional[str] = None,
    industry: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Look up point of interest categories
    
    Args:
        context: The FastMCP context
        category: Filter by category name
        lineofbusiness: Filter by line of business
        industry: Filter by industry name
        page: Page number for pagination
        page_size: Number of results per page
        
    Returns:
        List of POI categories matching criteria
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"POI category lookup request: category={category}, lineofbusiness={lineofbusiness}, industry={industry}")
    
    # Get mock categories
    categories = MOCK_POI_CATEGORIES
    
    # Apply filtering if provided
    if category or lineofbusiness or industry:
        filtered_categories = []
        for cat in categories:
            # Check if category matches any of the filter criteria
            if (not category or cat.get("category_name") == category) and \
               (not lineofbusiness or cat.get("line_of_business") == lineofbusiness) and \
               (not industry or cat.get("industry_name") == industry):
                filtered_categories.append(cat)
        
        categories = filtered_categories
    
    # Apply pagination
    total_records = len(categories)
    total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    
    categories = categories[start_idx:end_idx]
    
    # Return mock data
    return {
        "status": "success",
        "categories": categories,
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


# Community API tools
@app.tool(
    name="neighborhood_community",
    description="Get neighborhood community information"
)
async def neighborhood_community(
    context: Context,
    geo_id_v4: str
) -> Dict[str, Any]:
    """
    Get neighborhood community information
    
    Args:
        context: The FastMCP context
        geo_id_v4: Geographic ID v4 of the neighborhood
        
    Returns:
        Detailed information about the neighborhood community
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Neighborhood community request: geoIdv4={geo_id_v4}")
    
    # In a real implementation, you would query the database or an external API
    # For now, return mock data
    community_data = MOCK_COMMUNITY.copy()
    
    # If geoIdv4 doesn't match our mock, simulate not found
    if geo_id_v4 != MOCK_COMMUNITY["geo_id_v4"]:
        return {
            "status": "error",
            "code": 404,
            "message": f"Community with geoIdv4 {geo_id_v4} not found."
        }
    
    # Return mock data
    return {
        "status": "success",
        "community": community_data
    }


@app.tool(
    name="location_lookup",
    description="Look up locations by various criteria"
)
async def location_lookup(
    context: Context,
    geo_id_v4: Optional[str] = None,
    name: Optional[str] = None,
    geography_type_abbreviation: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Look up locations by various criteria
    
    Args:
        context: The FastMCP context
        geo_id_v4: Geographic ID v4
        name: Location name
        geography_type_abbreviation: Geography type abbreviation
        page: Page number for pagination
        page_size: Number of results per page
        
    Returns:
        List of locations matching criteria
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"Location lookup request: geoIdv4={geo_id_v4}, name={name}, geographyTypeAbbreviation={geography_type_abbreviation}")
    
    # Validate that at least one search criterion is provided
    if not any([geo_id_v4, name, geography_type_abbreviation]):
        return {
            "status": "error",
            "code": 400,
            "message": "At least one search criterion is required. Please provide geoIdv4, name, or geographyTypeAbbreviation."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, we'll return mock data
    locations = [
        {
            "geo_id": "ZI92802",
            "geo_id_v4": "d87a509d9fc19bbafc4cee730988a18e",
            "name": "92802",
            "type": "ZI",
            "city": "ANAHEIM",
            "state": "CA",
            "county": "ORANGE COUNTY"
        },
        {
            "geo_id": "NB060591401",
            "geo_id_v4": "08f3762070941bf29ff66a3927612f05",
            "name": "ANAHEIM RESORT",
            "type": "NB",
            "city": "ANAHEIM",
            "state": "CA",
            "county": "ORANGE COUNTY"
        }
    ]
    
    # Apply filtering if specific geo_id_v4 is provided
    if geo_id_v4:
        filtered_locations = [loc for loc in locations if loc.get("geo_id_v4") == geo_id_v4]
        locations = filtered_locations
    
    # Apply filtering if name is provided
    if name:
        filtered_locations = [loc for loc in locations if name.upper() in loc.get("name", "").upper()]
        locations = filtered_locations
    
    # Apply filtering if geography_type_abbreviation is provided
    if geography_type_abbreviation:
        filtered_locations = [loc for loc in locations if loc.get("type") == geography_type_abbreviation]
        locations = filtered_locations
    
    # Apply pagination
    total_records = len(locations)
    total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    
    locations = locations[start_idx:end_idx]
    
    # Return mock data
    return {
        "status": "success",
        "locations": locations,
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


# School API tools
@app.tool(
    name="school_profile",
    description="Get school profile information"
)
async def school_profile(
    context: Context,
    geo_id_v4: str
) -> Dict[str, Any]:
    """
    Get school profile information
    
    Args:
        context: The FastMCP context
        geo_id_v4: Geographic ID v4 of the school
        
    Returns:
        Detailed information about the school
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"School profile request: geoIdv4={geo_id_v4}")
    
    # In a real implementation, you would query the database or an external API
    # For now, return mock data for a matching school
    school = None
    for s in MOCK_SCHOOLS:
        if s["geo_id_v4"] == geo_id_v4:
            school = s.copy()
            break
    
    if not school:
        return {
            "status": "error",
            "code": 404,
            "message": f"School with geoIdv4 {geo_id_v4} not found."
        }
    
    # Return mock data
    return {
        "status": "success",
        "school": school
    }


@app.tool(
    name="school_district",
    description="Get school district information"
)
async def school_district(
    context: Context,
    geo_id_v4: str
) -> Dict[str, Any]:
    """
    Get school district information
    
    Args:
        context: The FastMCP context
        geo_id_v4: Geographic ID v4 of the school district
        
    Returns:
        Detailed information about the school district
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"School district request: geoIdv4={geo_id_v4}")
    
    # In a real implementation, you would query the database or an external API
    # For now, return mock data
    district_data = MOCK_SCHOOL_DISTRICT.copy()
    
    # If geoIdv4 doesn't match our mock, simulate not found
    if geo_id_v4 != MOCK_SCHOOL_DISTRICT["geo_id_v4"]:
        return {
            "status": "error",
            "code": 404,
            "message": f"School district with geoIdv4 {geo_id_v4} not found."
        }
    
    # Return mock data
    return {
        "status": "success",
        "district": district_data
    }


@app.tool(
    name="school_search",
    description="Search for schools by various criteria"
)
async def school_search(
    context: Context,
    radius: float = 5.0,
    geo_id_v4: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    school_type: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Search for schools by location and type
    
    Args:
        context: The FastMCP context
        radius: Radius in miles to search (default: 5.0)
        geo_id_v4: Geographic ID v4 of the area to search within
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        school_type: Filter by school type (Elementary, Middle, High, Charter, Private, Public)
        page: Page number for pagination
        page_size: Number of results per page
        
    Returns:
        List of schools matching criteria
    """
    # Validate API key
    auth_error = validate_api_key(context)
    if auth_error:
        return auth_error
    
    logger.info(f"School search request: geoIdv4={geo_id_v4}, lat={latitude}, lon={longitude}, radius={radius}, type={school_type}")
    
    # Validate that location information is provided
    if not any([geo_id_v4, (latitude is not None and longitude is not None)]):
        return {
            "status": "error",
            "code": 400,
            "message": "Location information is required. Please provide geoIdv4 or latitude+longitude."
        }
    
    # In a real implementation, you would query the database or an external API
    # For now, return mock data
    schools = MOCK_SCHOOLS
    
    # Apply filtering by school type if provided
    if school_type:
        filtered_schools = [s for s in schools if s.get("school_type") == school_type]
        schools = filtered_schools
    
    # Apply pagination
    total_records = len(schools)
    total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    
    schools = schools[start_idx:end_idx]
    
    # Return mock data
    return {
        "status": "success",
        "schools": schools,
        "total_records": total_records,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


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