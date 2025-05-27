import pytest
import os
import sys

# Add the project root to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """Test client for the FastMCP app with API key"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        client.headers = {"apikey": "test_api_key"}
        yield client


@pytest.fixture
async def client_no_auth():
    """Test client for the FastMCP app without API key"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client