import pytest
import os
import sys

# We're not going to auto-import app here, to avoid the settings issue
# Tests can import what they need directly

# Mock context classes for testing FastMCP tools
class MockRequest:
    """Mock request object for testing"""
    def __init__(self, headers=None):
        self.headers = headers or {}


class MockContext:
    """Mock Context for testing FastMCP tools"""
    def __init__(self, headers=None):
        self.request = MockRequest(headers)


@pytest.fixture
def api_key_context():
    """Context with valid API key for testing"""
    return MockContext(headers={"apikey": "test_api_key"})


@pytest.fixture
def no_auth_context():
    """Context without API key for testing"""
    return MockContext()