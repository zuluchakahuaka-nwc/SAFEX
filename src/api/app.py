"""
API package for SAFEX
FastAPI REST API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..utils.logger import get_logger
from ..utils.config import settings

logger = get_logger("api")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
    )

    return app
