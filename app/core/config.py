import os
import logging
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class LogConfig(BaseSettings):
    """Logging configuration"""
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_DATEFMT: str = "%Y-%m-%d %H:%M:%S"


class Settings(BaseSettings):
    """Application settings"""
    # API settings
    API_TITLE: str = "ATTOM API"
    API_DESCRIPTION: str = "MCP Server implementation of ATTOM API"
    API_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Authentication
    API_KEY_NAME: str = "apikey"
    API_KEY_HEADER: str = "apikey"
    API_KEYS: List[str] = ["test_api_key"]  # List of valid API keys
    
    # Service URLs
    ATTOM_HOST_URL: str = "https://api.gateway.attomdata.com"
    PROP_API_PREFIX: str = "/propertyapi/v1.0.0"
    DLP_V2_PREFIX: str = "/property/v2"
    DLP_V3_PREFIX: str = "/property/v3"
    
    # Logging
    LOG_CONFIG: LogConfig = LogConfig()
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Configure logging
def configure_logging():
    """Configure logging based on settings"""
    log_config = settings.LOG_CONFIG
    
    logging.basicConfig(
        level=getattr(logging, log_config.LOG_LEVEL),
        format=log_config.LOG_FORMAT,
        datefmt=log_config.LOG_DATEFMT,
    )
    
    # Reduce log level of some noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # Get root logger
    logger = logging.getLogger()
    
    return logger


# Create logger instance
logger = configure_logging()