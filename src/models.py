"""Pydantic models for the ATTOM API MCP tools.

This module provides Pydantic models for the ATTOM API MCP tools.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class PropertyIdentifier(BaseModel):
    """Base model for identifying a property using one of several methods."""

    attom_id: Optional[str] = Field(None, description="ATTOM ID for the property")
    address: Optional[str] = Field(None, description="Full address of the property")
    address1: Optional[str] = Field(
        None, description="First line of address (e.g., street address)"
    )
    address2: Optional[str] = Field(
        None, description="Second line of address (e.g., city, state, ZIP)"
    )
    fips: Optional[str] = Field(None, description="FIPS county code")
    apn: Optional[str] = Field(None, description="Assessor Parcel Number")

    @field_validator("*")
    def check_mutually_exclusive(cls, v, info):
        """Ensure that only one property identification method is used."""
        field_name = info.field_name
        if field_name == "attom_id" and v is not None:
            return v
        return v


class AttomResponse(BaseModel):
    """Base model for ATTOM API responses."""

    status_code: Optional[int] = Field(None, description="HTTP status code")
    status_message: Optional[str] = Field(None, description="Status message from the API")
    data: Dict[str, Any] = Field(default_factory=dict, description="API response data")


class ErrorResponse(BaseModel):
    """Model for error responses."""

    status_code: int = Field(description="HTTP status code")
    detail: str = Field(description="Error message")


class AddressComponents(BaseModel):
    """Model for address components."""

    street_name: Optional[str] = Field(None, description="Street name")
    street_number: Optional[str] = Field(None, description="Street number")
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State (two-letter code)")
    zip_code: Optional[str] = Field(None, description="ZIP code")
    zip_plus4: Optional[str] = Field(None, description="ZIP+4 code")
    unit_number: Optional[str] = Field(None, description="Unit/apartment number")


class PropertyBasicInfo(BaseModel):
    """Model for basic property information."""

    attom_id: Optional[str] = Field(None, description="ATTOM ID for the property")
    property_type: Optional[str] = Field(None, description="Property type (e.g., SFR, Condo)")
    address_full: Optional[str] = Field(None, description="Full formatted address")
    address_components: Optional[AddressComponents] = Field(None, description="Address components")
    fips: Optional[str] = Field(None, description="FIPS county code")
    apn: Optional[str] = Field(None, description="Assessor Parcel Number")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
