import pytest


async def test_boundary_detail_success(client):
    """Test boundary detail endpoint with valid geoIdV4"""
    response = await client.get("/areaapi/area/boundary/detail?geoIdV4=baa5d7de09afdefd0ffcd66b581991de")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "boundary" in data
    assert data["boundary"]["format"] == "geojson"


async def test_boundary_detail_missing_parameter(client):
    """Test boundary detail endpoint with missing parameters"""
    response = await client.get("/areaapi/area/boundary/detail")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 400


async def test_hierarchy_lookup_with_lat_lon(client):
    """Test hierarchy lookup endpoint with latitude and longitude"""
    response = await client.get("/areaapi/area/hierarchy/lookup?latitude=33.8239&longitude=-117.7842")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "hierarchy" in data
    assert "state" in data["hierarchy"]
    assert "county" in data["hierarchy"]


async def test_hierarchy_lookup_missing_parameter(client):
    """Test hierarchy lookup endpoint with missing parameters"""
    response = await client.get("/areaapi/area/hierarchy/lookup")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == 400


async def test_county_lookup(client):
    """Test county lookup endpoint"""
    response = await client.get("/areaapi/area/county/lookup?stateId=ST06")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "counties" in data
    assert len(data["counties"]) > 0
    assert "total_records" in data