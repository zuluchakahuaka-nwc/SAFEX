"""
API Routes module initialization
"""

from .validation import router as validation_router
from .scanning import router as scanning_router
from .reporting import router as reporting_router
from .status import router as status_router
from .i18n import router as i18n_router

__all__ = [
    "validation_router",
    "scanning_router",
    "reporting_router",
    "status_router",
    "i18n_router",
]
