from fastmcp import FastMCP, Request, Response, Path, Query, Body, Form
from typing import Optional, List, Dict, Any, Union
import logging
from ...core.config import settings
from ..models.property import (
    PropertyParams, 
    PropertyDetail, 
    PropertyDetailResponse,
    PropertySnapshotResponse,
    PropertySearchResponse,
    Address,
    Sale,
    Assessment,
    AVM
)

logger = logging.getLogger(__name__)

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


def register_property_routes(app: FastMCP):
    """Register all property API routes"""
    
    @app.get("/propertyapi/v1.0.0/property/detail")
    async def property_detail_get(
        request: Request,
        attom_id: Optional[str] = Query(None, alias="AttomID"),
        address: Optional[str] = Query(None),
        address1: Optional[str] = Query(None),
        address2: Optional[str] = Query(None),
        fips: Optional[str] = Query(None),
        apn: Optional[str] = Query(None),
    ) -> Response:
        """
        Get detailed property information
        
        Args:
            attom_id: ATTOM ID of the property
            address: Full property address
            address1: First line of property address
            address2: Second line of property address (city, state, zip)
            fips: FIPS code
            apn: Assessor's Parcel Number
            
        Returns:
            Property detail information
        """
        logger.info(f"Property detail request: AttomID={attom_id}, address={address}")
        
        # Validate that at least one identifier is provided
        if not any([attom_id, address, (address1 and address2), (fips and apn)]):
            return Response(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "message": "At least one property identifier is required. Please provide AttomID, address, address1+address2, or fips+apn."
                }
            )
        
        # In a real implementation, you would query the database or an external API
        # For now, we'll return mock data
        property_data = MOCK_PROPERTY.copy()
        
        # If attomID is provided and doesn't match our mock, simulate not found
        if attom_id and attom_id != MOCK_PROPERTY["attomId"]:
            return Response(
                status_code=404,
                content={
                    "status": "error",
                    "code": 404,
                    "message": f"Property with AttomID {attom_id} not found."
                }
            )
        
        # Return mock data
        response_data = {
            "status": "success",
            "property": property_data
        }
        
        return Response(
            content=response_data
        )
    
    @app.post("/propertyapi/v1.0.0/property/detail")
    async def property_detail_post(
        request: Request,
        attom_id: Optional[str] = Form(None, alias="AttomID"),
        address: Optional[str] = Form(None),
        address1: Optional[str] = Form(None),
        address2: Optional[str] = Form(None),
        fips: Optional[str] = Form(None),
        apn: Optional[str] = Form(None),
    ) -> Response:
        """
        Get detailed property information via POST
        
        Args:
            attom_id: ATTOM ID of the property
            address: Full property address
            address1: First line of property address
            address2: Second line of property address (city, state, zip)
            fips: FIPS code
            apn: Assessor's Parcel Number
            
        Returns:
            Property detail information
        """
        # POST handler can reuse the same logic as GET
        return await property_detail_get(
            request=request,
            attom_id=attom_id,
            address=address,
            address1=address1,
            address2=address2,
            fips=fips,
            apn=apn
        )
    
    @app.get("/propertyapi/v1.0.0/property/snapshot")
    async def property_snapshot_get(
        request: Request,
        attom_id: Optional[str] = Query(None, alias="AttomID"),
        address: Optional[str] = Query(None),
        address1: Optional[str] = Query(None),
        address2: Optional[str] = Query(None),
        fips: Optional[str] = Query(None),
        apn: Optional[str] = Query(None),
    ) -> Response:
        """
        Get basic property information snapshot
        
        Args:
            attom_id: ATTOM ID of the property
            address: Full property address
            address1: First line of property address
            address2: Second line of property address (city, state, zip)
            fips: FIPS code
            apn: Assessor's Parcel Number
            
        Returns:
            Property snapshot information
        """
        logger.info(f"Property snapshot request: AttomID={attom_id}, address={address}")
        
        # Validate that at least one identifier is provided
        if not any([attom_id, address, (address1 and address2), (fips and apn)]):
            return Response(
                status_code=400,
                content={
                    "status": "error",
                    "code": 400,
                    "message": "At least one property identifier is required. Please provide AttomID, address, address1+address2, or fips+apn."
                }
            )
        
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
        response_data = {
            "status": "success",
            "property": property_data
        }
        
        return Response(
            content=response_data
        )
    
    @app.post("/propertyapi/v1.0.0/property/snapshot")
    async def property_snapshot_post(
        request: Request,
        attom_id: Optional[str] = Form(None, alias="AttomID"),
        address: Optional[str] = Form(None),
        address1: Optional[str] = Form(None),
        address2: Optional[str] = Form(None),
        fips: Optional[str] = Form(None),
        apn: Optional[str] = Form(None),
    ) -> Response:
        """
        Get basic property information snapshot via POST
        
        Args:
            attom_id: ATTOM ID of the property
            address: Full property address
            address1: First line of property address
            address2: Second line of property address (city, state, zip)
            fips: FIPS code
            apn: Assessor's Parcel Number
            
        Returns:
            Property snapshot information
        """
        # POST handler can reuse the same logic as GET
        return await property_snapshot_get(
            request=request,
            attom_id=attom_id,
            address=address,
            address1=address1,
            address2=address2,
            fips=fips,
            apn=apn
        )
    
    @app.get("/propertyapi/v1.0.0/property/id")
    async def property_id_get(
        request: Request,
        attom_id: Optional[str] = Query(None, alias="AttomID"),
        address: Optional[str] = Query(None),
        address1: Optional[str] = Query(None),
        address2: Optional[str] = Query(None),
        fips: Optional[str] = Query(None),
        apn: Optional[str] = Query(None),
        property_type: Optional[str] = Query(None, alias="propertytype"),
        postal_code: Optional[str] = Query(None, alias="postalcode"),
        page: Optional[int] = Query(1, ge=1),
        page_size: Optional[int] = Query(10, ge=1, le=100, alias="pagesize"),
        order_by: Optional[str] = Query(None, alias="orderby"),
    ) -> Response:
        """
        Search for properties by identifier or criteria
        
        Args:
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
            order_by: Sort order specification
            
        Returns:
            List of properties matching criteria
        """
        logger.info(f"Property ID search request: AttomID={attom_id}, address={address}, postalcode={postal_code}")
        
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
            
            response_data = {
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
            
            response_data = {
                "status": "success",
                "properties": properties,
                "total_matches": 2,
                "page": page,
                "page_size": page_size,
                "total_pages": 1
            }
        
        return Response(
            content=response_data
        )
    
    @app.post("/propertyapi/v1.0.0/property/id")
    async def property_id_post(
        request: Request,
        attom_id: Optional[str] = Form(None, alias="AttomID"),
        address: Optional[str] = Form(None),
        address1: Optional[str] = Form(None),
        address2: Optional[str] = Form(None),
        fips: Optional[str] = Form(None),
        apn: Optional[str] = Form(None),
        property_type: Optional[str] = Form(None, alias="propertytype"),
        postal_code: Optional[str] = Form(None, alias="postalcode"),
        page: Optional[int] = Form(1, ge=1),
        page_size: Optional[int] = Form(10, ge=1, le=100, alias="pagesize"),
        order_by: Optional[str] = Form(None, alias="orderby"),
    ) -> Response:
        """
        Search for properties by identifier or criteria via POST
        """
        # POST handler can reuse the same logic as GET
        return await property_id_get(
            request=request,
            attom_id=attom_id,
            address=address,
            address1=address1,
            address2=address2,
            fips=fips,
            apn=apn,
            property_type=property_type,
            postal_code=postal_code,
            page=page,
            page_size=page_size,
            order_by=order_by
        )