from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse as Response
import logging
from .api.routes import register_all_routes
from .core.config import settings, logger
from .core.auth import api_key_auth


def create_app() -> FastMCP:
    """Create and configure the FastMCP application"""
    
    # Create FastMCP app instance
    app = FastMCP(
        name=settings.API_TITLE,
        instructions=settings.API_DESCRIPTION,
    )
    
    # Add custom middleware for API key authentication
    @app.custom_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def handle_request(request: Request):
        # Check authentication
        auth_result = await api_key_auth(request)
        if auth_result:
            return auth_result
        
        # If authenticated, let regular routing handle the request
        return Response({"error": "Route not found"}, status_code=404)
    
    # Register API routes
    register_all_routes(app)
    
    # Add root endpoint with API information
    @app.custom_route("/", methods=["GET"])
    async def root(request: Request):
        """Root endpoint - API information"""
        return Response({
            "name": settings.API_TITLE,
            "version": settings.API_VERSION,
            "description": settings.API_DESCRIPTION
        })
    
    return app


app = create_app()


if __name__ == "__main__":
    # Run the app
    import uvicorn
    
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )