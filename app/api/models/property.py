from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from .common import PropertyIdentifier, ApiResponse, PropertyType


class PropertyParams(PropertyIdentifier):
    """Parameters for property-based endpoints"""
    property_type: Optional[str] = Field(None, alias="propertytype")
    min_universal_size: Optional[int] = Field(None, alias="minUniversalSize", ge=0)
    max_universal_size: Optional[int] = Field(None, alias="maxUniversalSize", ge=0)
    min_sale_amt: Optional[float] = Field(None, alias="minSaleAmt", ge=0)
    max_sale_amt: Optional[float] = Field(None, alias="maxSaleAmt", ge=0)
    min_beds: Optional[int] = Field(None, alias="minBeds", ge=0)
    max_beds: Optional[int] = Field(None, alias="maxBeds", ge=0)
    min_baths_total: Optional[float] = Field(None, alias="minBathsTotal", ge=0)
    max_baths_total: Optional[float] = Field(None, alias="maxBathsTotal", ge=0)
    min_year_built: Optional[int] = Field(None, alias="minYearBuilt", ge=0)
    max_year_built: Optional[int] = Field(None, alias="maxYearBuilt", ge=0)
    postal_code: Optional[str] = Field(None, alias="postalcode")
    radius: Optional[float] = None
    order_by: Optional[str] = Field(None, alias="orderby")


class Address(BaseModel):
    """Address details"""
    street_address: Optional[str] = Field(None, alias="streetAddress")
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    county: Optional[str] = None
    country: Optional[str] = None


class Property(BaseModel):
    """Core property details"""
    property_id: str = Field(..., alias="propertyId")
    address: Address
    property_type: Optional[str] = Field(None, alias="propertyType")
    year_built: Optional[int] = Field(None, alias="yearBuilt")
    beds: Optional[int] = None
    baths: Optional[float] = None
    universal_size: Optional[int] = Field(None, alias="universalSize")
    lot_size: Optional[float] = Field(None, alias="lotSize")


class Assessment(BaseModel):
    """Property assessment details"""
    year: int
    land_value: Optional[float] = Field(None, alias="landValue")
    improvement_value: Optional[float] = Field(None, alias="improvementValue")
    total_value: Optional[float] = Field(None, alias="totalValue")


class Sale(BaseModel):
    """Property sale details"""
    sale_date: Optional[str] = Field(None, alias="saleDate")
    sale_price: Optional[float] = Field(None, alias="salePrice")
    sale_type: Optional[str] = Field(None, alias="saleType")
    buyer_name: Optional[str] = Field(None, alias="buyerName")
    seller_name: Optional[str] = Field(None, alias="sellerName")


class AVM(BaseModel):
    """Automated Valuation Model details"""
    value: float
    high_value: Optional[float] = Field(None, alias="highValue")
    low_value: Optional[float] = Field(None, alias="lowValue")
    confidence_score: Optional[int] = Field(None, alias="confidenceScore", ge=0, le=100)


class PropertyDetail(Property):
    """Extended property details"""
    attom_id: str = Field(..., alias="attomId")
    legal_description: Optional[str] = Field(None, alias="legalDescription")
    owner_name: Optional[str] = Field(None, alias="ownerName")
    owner_occupied: Optional[bool] = Field(None, alias="ownerOccupied")
    tax_id: Optional[str] = Field(None, alias="taxId")
    apn: Optional[str] = None
    fips: Optional[str] = None
    assessments: Optional[List[Assessment]] = None
    sales_history: Optional[List[Sale]] = Field(None, alias="salesHistory")
    avm: Optional[AVM] = None


class PropertyDetailResponse(ApiResponse):
    """Response for property detail endpoints"""
    data: Dict[str, PropertyDetail]


class PropertySnapshotResponse(ApiResponse):
    """Response for property snapshot endpoints"""
    data: Dict[str, Property]


class SaleDetailResponse(ApiResponse):
    """Response for sale detail endpoints"""
    data: Dict[str, Sale]


class AssessmentDetailResponse(ApiResponse):
    """Response for assessment detail endpoints"""
    data: Dict[str, Assessment]


class AVMDetailResponse(ApiResponse):
    """Response for AVM detail endpoints"""
    data: Dict[str, AVM]


class PropertySearchResponse(ApiResponse):
    """Response for property search endpoints"""
    data: Dict[str, List[Property]]
    total_matches: int = Field(..., alias="totalMatches")
    page: int
    page_size: int = Field(..., alias="pageSize")
    total_pages: int = Field(..., alias="totalPages")