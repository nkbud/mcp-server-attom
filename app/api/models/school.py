from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from .common import ApiResponse, GeoParams, PaginationParams


class SchoolType(str, Enum):
    """Types of schools"""
    ELEMENTARY = "Elementary"
    MIDDLE = "Middle"
    HIGH = "High"
    CHARTER = "Charter"
    PRIVATE = "Private"
    PUBLIC = "Public"


class SchoolRating(BaseModel):
    """School rating information"""
    rating: Optional[int] = Field(None, ge=1, le=10)
    year: Optional[int] = None
    source: Optional[str] = None


class School(BaseModel):
    """School information"""
    school_id: str = Field(..., alias="schoolId")
    geo_id_v4: str = Field(..., alias="geoIdV4")
    name: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    latitude: float
    longitude: float
    school_type: Optional[SchoolType] = Field(None, alias="schoolType")
    grades: Optional[str] = None
    student_count: Optional[int] = Field(None, alias="studentCount")
    student_teacher_ratio: Optional[float] = Field(None, alias="studentTeacherRatio")
    rating: Optional[SchoolRating] = None
    district_name: Optional[str] = Field(None, alias="districtName")
    district_id: Optional[str] = Field(None, alias="districtId")
    phone: Optional[str] = None
    website: Optional[str] = None
    distance: Optional[float] = None


class SchoolDistrict(BaseModel):
    """School district information"""
    district_id: str = Field(..., alias="districtId")
    geo_id_v4: str = Field(..., alias="geoIdV4")
    name: str
    state: Optional[str] = None
    student_count: Optional[int] = Field(None, alias="studentCount")
    school_count: Optional[int] = Field(None, alias="schoolCount")
    rating: Optional[SchoolRating] = None


class SchoolProfileParams(BaseModel):
    """Parameters for school profile endpoint"""
    geo_id_v4: str = Field(..., alias="geoIdv4")


class SchoolDistrictParams(BaseModel):
    """Parameters for school district endpoint"""
    geo_id_v4: str = Field(..., alias="geoIdv4")


class SchoolSearchParams(PaginationParams):
    """Parameters for school search endpoint"""
    radius: float = 5.0
    geo_id_v4: Optional[str] = Field(None, alias="geoIdv4")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    school_type: Optional[SchoolType] = Field(None, alias="schoolType")


class SchoolProfileResponse(ApiResponse):
    """Response for school profile endpoint"""
    data: School


class SchoolDistrictResponse(ApiResponse):
    """Response for school district endpoint"""
    data: SchoolDistrict


class SchoolSearchResponse(ApiResponse):
    """Response for school search endpoint"""
    data: List[School]
    total_records: int = Field(..., alias="totalRecords")
    page: int
    page_size: int = Field(..., alias="pageSize")