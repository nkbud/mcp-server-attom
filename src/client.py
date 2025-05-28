"""ATTOM API client.

This module provides a client for making HTTP requests to the ATTOM API.
"""

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx
import structlog

from src import config

# Configure logging
logger = structlog.get_logger(__name__)


class AttomAPIError(Exception):
    """Exception raised for ATTOM API errors."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"ATTOM API Error ({status_code}): {detail}")


class AttomClient:
    """Client for the ATTOM API."""

    def __init__(
        self,
        api_key: str = config.ATTOM_API_KEY,
        host_url: str = config.ATTOM_HOST_URL,
        prop_api_prefix: str = config.ATTOM_PROP_API_PREFIX,
        dlp_v2_prefix: str = config.ATTOM_DLP_V2_PREFIX,
        dlp_v3_prefix: str = config.ATTOM_DLP_V3_PREFIX,
    ):
        """Initialize the ATTOM API client.

        Args:
            api_key: ATTOM API key
            host_url: Base URL for the ATTOM API
            prop_api_prefix: Prefix for property API endpoints
            dlp_v2_prefix: Prefix for DLP v2 API endpoints
            dlp_v3_prefix: Prefix for DLP v3 API endpoints
        """
        self.api_key = api_key
        self.host_url = host_url
        self.prop_api_prefix = prop_api_prefix
        self.dlp_v2_prefix = dlp_v2_prefix
        self.dlp_v3_prefix = dlp_v3_prefix
        self.client = httpx.Client(
            headers={
                "apikey": self.api_key,
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def _build_url(self, endpoint: str, api_prefix: Optional[str] = None) -> str:
        """Build a URL for the ATTOM API.

        Args:
            endpoint: API endpoint path
            api_prefix: API prefix to use (default: property API prefix)

        Returns:
            Full URL for the endpoint
        """
        if api_prefix is None:
            api_prefix = self.prop_api_prefix

        # Handle case where endpoint already starts with a slash
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]

        # Add prefix if not already in endpoint
        if not endpoint.startswith(api_prefix.lstrip("/")):
            url = urljoin(self.host_url, api_prefix)
            url = urljoin(url + "/" if not url.endswith("/") else url, endpoint)
        else:
            url = urljoin(self.host_url, endpoint)

        return url

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        api_prefix: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make a GET request to the ATTOM API.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            api_prefix: API prefix to use (default: property API prefix)

        Returns:
            API response as a dictionary

        Raises:
            AttomAPIError: If the API returns an error
        """
        url = self._build_url(endpoint, api_prefix)
        log = logger.bind(method="GET", url=url, params=params)

        log.debug("Making API request")

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            log.error(
                "API request failed",
                status_code=e.response.status_code,
                response=e.response.text,
            )
            raise AttomAPIError(e.response.status_code, e.response.text)
        except httpx.RequestError as e:
            log.error("API request failed", error=str(e))
            raise AttomAPIError(500, str(e))

    async def post(
        self, endpoint: str, data: Dict[str, Any], api_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """Make a POST request to the ATTOM API.

        Args:
            endpoint: API endpoint path
            data: Form data
            api_prefix: API prefix to use (default: property API prefix)

        Returns:
            API response as a dictionary

        Raises:
            AttomAPIError: If the API returns an error
        """
        url = self._build_url(endpoint, api_prefix)
        log = logger.bind(method="POST", url=url, data=data)

        log.debug("Making API request")

        try:
            response = self.client.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            log.error(
                "API request failed",
                status_code=e.response.status_code,
                response=e.response.text,
            )
            raise AttomAPIError(e.response.status_code, e.response.text)
        except httpx.RequestError as e:
            log.error("API request failed", error=str(e))
            raise AttomAPIError(500, str(e))


# Create a singleton instance of the client
client = AttomClient()
