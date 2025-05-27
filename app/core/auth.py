from starlette.requests import Request
from starlette.responses import JSONResponse as Response
from typing import Optional
from .config import settings
import logging

logger = logging.getLogger(__name__)


async def api_key_auth(request: Request) -> Optional[Response]:
    """
    Middleware to validate API key
    
    Args:
        request: The incoming request
        
    Returns:
        Response object if authentication fails, None if successful
    """
    # Extract API key from header
    api_key = request.headers.get(settings.API_KEY_HEADER)
    
    # Validate API key
    if not api_key:
        logger.warning(f"Missing API key in request to {request.url}")
        return Response(
            {
                "status": "error",
                "code": 401,
                "message": f"Missing API key. Please provide the '{settings.API_KEY_HEADER}' header."
            },
            status_code=401
        )
    
    if api_key not in settings.API_KEYS:
        logger.warning(f"Invalid API key used for request to {request.url}")
        return Response(
            {
                "status": "error",
                "code": 403,
                "message": "Invalid API key. Please provide a valid API key."
            },
            status_code=403
        )
    
    # Store the validated API key in the request state for later use
    request.state.api_key = api_key
    
    return None