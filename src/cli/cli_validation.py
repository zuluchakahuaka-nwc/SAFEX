"""
Validation commands for CLI
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.validation_engine import ValidationEngine
from src.safety.safety_manager import SafetyManager
from src.i18n.translation_manager import TranslationManager
from src.utils.logger import get_logger

logger = get_logger("cli_validation")


def validate_ownership(
    target: str,
    method: str = "auto",
    safety_level: str = "safe",
    language: str = "en",
    auto_confirm: bool = False,
):
    """
    Validate ownership of target

    Args:
        target: Target to validate
        method: Validation method
        safety_level: Safety level
        language: Language for output
        auto_confirm: Auto-confirm without prompts
    """
    tm = TranslationManager()

    logger.info(tm.translate("validating_target", language=language) % target)

    # Check safety level
    sm = SafetyManager()
    if safety_level in ["moderate", "aggressive"] and not auto_confirm:
        risk = sm.assess_fix_risk("VALIDATION", target, "HIGH")
        warning_emoji = sm.get_warning_emoji(risk["level"])

        print(f"\n{warning_emoji} {risk['message']}")

        if not sm.confirm_fix("VALIDATION", target, risk["level"]):
            logger.info(tm.translate("operation_cancelled", language=language))
            return {"success": False, "message": "Cancelled by user"}

    # Perform validation
    engine = ValidationEngine()
    result = engine.validate_target(target, method, safety_level)

    return result


def validate_batch(targets: list, safety_level: str = "safe", language: str = "en"):
    """
    Validate multiple targets

    Args:
        targets: List of targets
        safety_level: Safety level
        language: Language for output
    """
    tm = TranslationManager()

    logger.info(
        f"{tm.translate('batch_validation', language=language)}: {len(targets)} targets"
    )

    engine = ValidationEngine()
    result = engine.validate_batch(targets, safety_level)

    return result


def validate_directory(
    directory: str,
    pattern: str = "*",
    safety_level: str = "safe",
    recursive: bool = False,
    language: str = "en",
):
    """
    Validate all files in a directory

    Args:
        directory: Directory path
        pattern: File pattern
        safety_level: Safety level
        recursive: Recursive scan
        language: Language for output
    """
    tm = TranslationManager()

    logger.info(
        f"{tm.translate('directory_validation', language=language)}: {directory}"
    )

    engine = ValidationEngine()
    result = engine.validate_directory(directory, pattern, safety_level, recursive)

    return result
