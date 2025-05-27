from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum


class PropertyIdentifier(BaseModel):
    """Model for property identification methods"""
    attom_id: Optional[str] = Field(None, alias="AttomID")
    address: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    fips: Optional[str] = None
    apn: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PropertyType(str, Enum):
    """Property types supported by ATTOM API"""
    SINGLE_FAMILY = "SINGLE FAMILY RESIDENCE"
    CONDOMINIUM = "CONDOMINIUM"
    TOWNHOUSE = "TOWNHOUSE"
    COMMERCIAL = "COMMERCIAL"
    MULTI_FAMILY = "MULTI FAMILY DWELLING"
    DUPLEX = "DUPLEX"
    TRIPLEX = "TRIPLEX"
    QUADRUPLEX = "QUADRUPLEX"


class ResponseFormat(str, Enum):
    """Response format options"""
    JSON = "application/json"
    XML = "application/xml"


class ApiError(BaseModel):
    """API error response model"""
    status: str = "error"
    code: int
    message: str
    detail: Optional[Dict[str, Any]] = None


class ApiResponse(BaseModel):
    """Base API response model"""
    status: str = "success"
    data: Optional[Dict[str, Any]] = None


class PaginationParams(BaseModel):
    """Common pagination parameters"""
    page: Optional[int] = Field(1, ge=1)
    page_size: Optional[int] = Field(10, ge=1, le=100, alias="pageSize")


class GeoParams(BaseModel):
    """Geographic parameters"""
    geo_id_v4: Optional[str] = Field(None, alias="geoIdv4")
    geo_id: Optional[str] = Field(None, alias="geoId")
    geo_type: Optional[str] = None