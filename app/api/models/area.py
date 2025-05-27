from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from .common import GeoParams, ApiResponse


class GeographyType(str, Enum):
    """Geography type abbreviations"""
    STATE = "ST"
    COUNTY = "CO"
    CITY = "CI"
    ZIP = "ZI"
    NEIGHBORHOOD = "NB"
    SCHOOL_DISTRICT = "SD"


class BoundaryFormat(str, Enum):
    """Boundary format options"""
    GEOJSON = "geojson"
    WKT = "wkt"


class Location(BaseModel):
    """Geographic location"""
    latitude: float
    longitude: float


class Boundary(BaseModel):
    """Geographic boundary"""
    format: BoundaryFormat
    data: Any


class Area(BaseModel):
    """Geographic area details"""
    geo_id: str = Field(..., alias="geoId")
    geo_id_v4: str = Field(..., alias="geoIdV4")
    name: str
    type: GeographyType
    centroid: Optional[Location] = None
    boundary: Optional[Boundary] = None


class AreaHierarchy(BaseModel):
    """Hierarchical relationship between geographic areas"""
    state: Optional[Area] = None
    county: Optional[Area] = None
    city: Optional[Area] = None
    zip_code: Optional[Area] = Field(None, alias="zipCode")
    neighborhood: Optional[Area] = None
    school_district: Optional[Area] = Field(None, alias="schoolDistrict")
    congressional_district: Optional[Area] = Field(None, alias="congressionalDistrict")


class BoundaryDetailParams(GeoParams):
    """Parameters for boundary detail endpoint"""
    format: Optional[BoundaryFormat] = BoundaryFormat.GEOJSON
    mime: Optional[str] = "json"


class HierarchyLookupParams(BaseModel):
    """Parameters for hierarchy lookup endpoint"""
    wkt_string: Optional[str] = Field(None, alias="wktstring")
    geo_type: Optional[str] = Field(None, alias="geoType")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    mime: Optional[str] = "json"


class BoundaryDetailResponse(ApiResponse):
    """Response for boundary detail endpoint"""
    data: Dict[str, Boundary]


class HierarchyLookupResponse(ApiResponse):
    """Response for hierarchy lookup endpoint"""
    data: AreaHierarchy