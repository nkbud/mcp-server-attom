from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .common import ApiResponse, PaginationParams


class POICategory(BaseModel):
    """Point of interest category"""
    category_id: str = Field(..., alias="categoryId")
    category_name: str = Field(..., alias="categoryName")
    line_of_business: Optional[str] = Field(None, alias="lineOfBusiness")
    industry_name: Optional[str] = Field(None, alias="industryName")


class POI(BaseModel):
    """Point of interest details"""
    poi_id: str = Field(..., alias="poiId")
    name: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    latitude: float
    longitude: float
    category: POICategory
    distance: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class POISearchParams(PaginationParams):
    """Parameters for POI search endpoints"""
    point: Optional[str] = None  # WKT point format: "POINT(lon lat)"
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[float] = Field(1.0, gt=0)
    zipcode: Optional[str] = None
    category_name: Optional[str] = Field(None, alias="categoryName")
    line_of_business_name: Optional[str] = Field(None, alias="LineOfBusinessName")
    industry_name: Optional[str] = Field(None, alias="IndustryName")
    category_id: Optional[str] = Field(None, alias="CategoryId")


class POICategoryLookupParams(PaginationParams):
    """Parameters for POI category lookup"""
    category: Optional[str] = None
    lineofbusiness: Optional[str] = None
    industry: Optional[str] = None


class POISearchResponse(ApiResponse):
    """Response for POI search endpoints"""
    data: List[POI]
    total_records: int = Field(..., alias="totalRecords")
    page: int
    page_size: int = Field(..., alias="pageSize")


class POICategoryLookupResponse(ApiResponse):
    """Response for POI category lookup endpoint"""
    data: List[POICategory]
    total_records: int = Field(..., alias="totalRecords")