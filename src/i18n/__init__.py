"""
Internationalization (i18n) package
"""

from .translator import (
    Language,
    TranslationManager,
    get_translation_manager,
    t,
    get_safety_warning,
    get_safety_level,
)

__all__ = [
    "Language",
    "TranslationManager",
    "get_translation_manager",
    "t",
    "get_safety_warning",
    "get_safety_level",
]
