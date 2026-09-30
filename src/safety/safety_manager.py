"""
Safety Manager - Central safety coordination
"""

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SafetyLevel(Enum):
    """Safety levels for operations"""

    discovery = "discovery"
    safe = "safe"
    moderate = "moderate"
    aggressive = "aggressive"
    DISCOVERY = "discovery"
    SAFE = "safe"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class SafetyManager:
    """Manages safety checks, risk assessment, and user confirmations"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()

    def get_safety_level(self, level_name: str) -> SafetyLevel:
        try:
            return SafetyLevel[level_name]
        except KeyError:
            raise ValueError(
                f"Unknown safety level: {level_name}. "
                f"Available: {[l.name for l in SafetyLevel]}"
            )

    def assess_fix_risk(
        self, vuln_id: str, target_path: str, severity: str
    ) -> Dict[str, Any]:
        severity_upper = severity.upper()
        level_map = {
            "LOW": "LOW",
            "MEDIUM": "MEDIUM",
            "HIGH": "HIGH",
            "CRITICAL": "CRITICAL",
        }
        level = level_map.get(severity_upper, "MEDIUM")
        return {
            "level": level,
            "vuln_id": vuln_id,
            "target": target_path,
            "message": f"Risk assessment: {level} for {vuln_id}",
        }

    def confirm_fix(
        self, vuln_id: str, target_path: str, risk_level: str
    ) -> bool:
        if risk_level in ("HIGH", "CRITICAL"):
            logger.warning(
                f"High-risk operation: {vuln_id} on {target_path} ({risk_level})"
            )
            try:
                response = input(
                    f"Confirm {risk_level} risk operation on {target_path}? [y/N]: "
                )
                return response.strip().lower() in ("y", "yes")
            except (EOFError, KeyboardInterrupt):
                return False
        return True

    def get_warning_emoji(self, level: str) -> str:
        emoji_map = {
            "LOW": "[+] ",
            "MEDIUM": "[!] ",
            "HIGH": "[X] ",
            "CRITICAL": "[!!] ",
        }
        return emoji_map.get(level.upper(), "[?] ")

    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()
