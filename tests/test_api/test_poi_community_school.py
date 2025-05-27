import pytest
import json

# POI API tests
async def test_poi_search_with_lat_lon(client):
    """Test POI search endpoint with latitude and longitude"""
    response = await client.get("/v4/neighborhood/poi?latitude=33.8150&longitude=-117.9265&radius=1.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "pois" in data
    assert len(data["pois"]) > 0
    assert "total_records" in data

async def test_poi_search_missing_location(client):
    """Test POI search endpoint with missing location parameters"""
    response = await client.get("/v4/neighborhood/poi")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 400

async def test_poi_category_lookup(client):
    """Test POI category lookup endpoint"""
    response = await client.get("/v4/neighborhood/poi/categorylookup")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "categories" in data
    assert len(data["categories"]) > 0
    assert "total_records" in data

# Community API tests
async def test_neighborhood_community_success(client):
    """Test neighborhood community endpoint with valid geoIdv4"""
    response = await client.get("/v4.0.0/neighborhood/community?geoIdv4=08f3762070941bf29ff66a3927612f05")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "community" in data
    assert data["community"]["geo_id_v4"] == "08f3762070941bf29ff66a3927612f05"

async def test_neighborhood_community_not_found(client):
    """Test neighborhood community endpoint with invalid geoIdv4"""
    response = await client.get("/v4.0.0/neighborhood/community?geoIdv4=invalid_id")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 404

async def test_location_lookup_success(client):
    """Test location lookup endpoint"""
    response = await client.get("/v4/location/lookup?geographyTypeAbbreviation=ZI")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "locations" in data
    assert len(data["locations"]) > 0
    assert "total_records" in data

# School API tests
async def test_school_profile_success(client):
    """Test school profile endpoint with valid geoIdv4"""
    response = await client.get("/v4/school/profile?geoIdv4=9c6bded31fd0e089485f276acb947875")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "school" in data
    assert data["school"]["geo_id_v4"] == "9c6bded31fd0e089485f276acb947875"

async def test_school_district_success(client):
    """Test school district endpoint with valid geoIdv4"""
    response = await client.get("/v4/school/district?geoIdv4=8370d93a17ba7fb07f115392bd1225d9")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "district" in data
    assert data["district"]["geo_id_v4"] == "8370d93a17ba7fb07f115392bd1225d9"

async def test_school_search_success(client):
    """Test school search endpoint"""
    response = await client.get("/v4/school/search?latitude=33.8320&longitude=-117.9265&radius=5.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "schools" in data
    assert len(data["schools"]) > 0
    assert "total_records" in data