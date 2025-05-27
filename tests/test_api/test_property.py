import pytest
import json


async def test_root_endpoint(client):
    """Test the root endpoint returns API information"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data


async def test_property_detail_success(client):
    """Test property detail endpoint with valid AttomID"""
    response = await client.get("/propertyapi/v1.0.0/property/detail?AttomID=145423726")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "property" in data
    assert data["property"]["attomId"] == "145423726"


async def test_property_detail_missing_parameter(client):
    """Test property detail endpoint with missing parameters"""
    response = await client.get("/propertyapi/v1.0.0/property/detail")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 400


async def test_property_detail_not_found(client):
    """Test property detail endpoint with invalid AttomID"""
    response = await client.get("/propertyapi/v1.0.0/property/detail?AttomID=999999")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 404


async def test_property_snapshot_success(client):
    """Test property snapshot endpoint with valid AttomID"""
    response = await client.get("/propertyapi/v1.0.0/property/snapshot?AttomID=145423726")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "property" in data


async def test_property_id_search(client):
    """Test property ID search endpoint with postal code"""
    response = await client.get("/propertyapi/v1.0.0/property/id?postalcode=90703")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "properties" in data or "property" in data
    assert "total_matches" in data or "page" in data


async def test_missing_api_key(client_no_auth):
    """Test that requests without API key are rejected"""
    response = await client_no_auth.get("/propertyapi/v1.0.0/property/detail?AttomID=145423726")
    assert response.status_code == 401
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 401


async def test_post_property_detail(client):
    """Test POST to property detail endpoint"""
    response = await client.post(
        "/propertyapi/v1.0.0/property/detail",
        data={"AttomID": "145423726"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "property" in data
    assert data["property"]["attomId"] == "145423726"