from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .common import ApiResponse, GeoParams, PaginationParams


class Demographics(BaseModel):
    """Demographic statistics for a community"""
    population: Optional[int] = None
    population_density: Optional[float] = Field(None, alias="populationDensity")
    median_age: Optional[float] = Field(None, alias="medianAge")
    median_household_income: Optional[float] = Field(None, alias="medianHouseholdIncome")
    median_home_value: Optional[float] = Field(None, alias="medianHomeValue")
    owner_occupied_percent: Optional[float] = Field(None, alias="ownerOccupiedPercent")
    renter_occupied_percent: Optional[float] = Field(None, alias="renterOccupiedPercent")
    vacant_percent: Optional[float] = Field(None, alias="vacantPercent")


class NeighborhoodAmenities(BaseModel):
    """Neighborhood amenities information"""
    poi_count: Optional[int] = Field(None, alias="poiCount")
    restaurant_count: Optional[int] = Field(None, alias="restaurantCount")
    shopping_count: Optional[int] = Field(None, alias="shoppingCount")
    nightlife_count: Optional[int] = Field(None, alias="nightlifeCount")
    grocery_count: Optional[int] = Field(None, alias="groceryCount")
    school_count: Optional[int] = Field(None, alias="schoolCount")
    park_count: Optional[int] = Field(None, alias="parkCount")
    transit_count: Optional[int] = Field(None, alias="transitCount")


class Community(BaseModel):
    """Community information"""
    geo_id: str = Field(..., alias="geoId")
    geo_id_v4: str = Field(..., alias="geoIdV4")
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    demographics: Optional[Demographics] = None
    amenities: Optional[NeighborhoodAmenities] = None
    description: Optional[str] = None


class LocationLookupParams(GeoParams, PaginationParams):
    """Parameters for location lookup endpoint"""
    name: Optional[str] = None
    geography_type_abbreviation: Optional[str] = Field(None, alias="geographyTypeAbbreviation")


class NeighborhoodCommunityParams(BaseModel):
    """Parameters for neighborhood community endpoint"""
    geo_id_v4: str = Field(..., alias="geoIdv4")


class NeighborhoodCommunityResponse(ApiResponse):
    """Response for neighborhood community endpoint"""
    data: Community


class LocationLookupResponse(ApiResponse):
    """Response for location lookup endpoint"""
    data: List[Community]
    total_records: int = Field(..., alias="totalRecords")
    page: int
    page_size: int = Field(..., alias="pageSize")