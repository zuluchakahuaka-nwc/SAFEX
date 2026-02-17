"""
Safety warnings and confirmations
"""

from enum import Enum
from typing import List, Dict, Any
from ..utils.logger import get_logger

logger = get_logger("safety.warnings")


class WarningLevel(Enum):
    """Warning severity levels"""

    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    CRITICAL = "critical"


class SafetyWarning:
    """Safety warning with risk assessment"""

    def __init__(
        self,
        level: WarningLevel,
        title: str,
        description: str,
        impact: str,
        mitigations: List[str],
        requires_confirmation: bool = False,
    ):
        self.level = level
        self.title = title
        self.description = description
        self.impact = impact
        self.mitigations = mitigations
        self.requires_confirmation = requires_confirmation

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "level": self.level.value,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "mitigations": self.mitigations,
            "requires_confirmation": self.requires_confirmation,
        }


class SafetyWarnings:
    """Predefined safety warnings for different operations"""

    @staticmethod
    def get_scan_warnings(
        safety_level: str, scan_type: str, target: str
    ) -> List[SafetyWarning]:
        """
        Get safety warnings for a scan

        Args:
            safety_level: Safety level (discovery, safe, moderate, aggressive)
            scan_type: Type of scan (network, web, vulnerability)
            target: Target being scanned

        Returns:
            List of safety warnings
        """
        warnings = []

        # Warning based on safety level
        if safety_level == "discovery":
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.SAFE,
                    title="SAFE - Discovery Scan",
                    description="This is a purely passive scan. No modifications will be made.",
                    impact="No impact to target system. Only observation and analysis.",
                    mitigations=[
                        "Scan is read-only",
                        "No data modifications",
                        "Rate limiting enabled",
                        "Safe for production systems",
                    ],
                    requires_confirmation=False,
                )
            )
        elif safety_level == "safe":
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.LOW_RISK,
                    title="LOW RISK - Safe Scan",
                    description="Safe scanning mode. Non-invasive checks only.",
                    impact="Minimal impact. May trigger monitoring systems but no disruption.",
                    mitigations=[
                        "Read-only operations only",
                        "Rate limited to prevent overload",
                        "Safe for production systems with caution",
                        "Monitoring systems may log activity",
                    ],
                    requires_confirmation=False,
                )
            )
        elif safety_level == "moderate":
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.MEDIUM_RISK,
                    title="MEDIUM RISK - Moderate Scan",
                    description="Moderate scanning mode. Invasive but generally safe checks.",
                    impact="May cause temporary slowdown or trigger security alerts.",
                    mitigations=[
                        "Read-only by default",
                        "Aggressive rate limiting",
                        "Recommended for staging/test environments",
                        "Monitor system performance during scan",
                        "Have emergency stop ready",
                    ],
                    requires_confirmation=True,
                )
            )
        elif safety_level == "aggressive":
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.HIGH_RISK,
                    title="HIGH RISK - Aggressive Scan",
                    description="Aggressive scanning mode. Potentially disruptive checks.",
                    impact="May cause service disruption, high CPU usage, or trigger alerts.",
                    mitigations=[
                        "WARNING: Can be disruptive!",
                        "NOT recommended for production systems",
                        "Use isolated test environment",
                        "Schedule during maintenance window",
                        "Have full backup ready",
                        "Monitor continuously",
                    ],
                    requires_confirmation=True,
                )
            )

        # Warning about target
        if (
            "localhost" in target
            or target.startswith("127.")
            or target.startswith("192.168.")
            or target.startswith("10.")
        ):
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.HIGH_RISK,
                    title="LOCAL TARGET",
                    description="Target appears to be a local/internal system.",
                    impact="Scanning local systems can disrupt your own network and services.",
                    mitigations=[
                        "You are scanning YOUR OWN system",
                        "May disrupt your work",
                        "May affect other users",
                        "Double-check target address",
                        "Consider using test environment",
                    ],
                    requires_confirmation=True,
                )
            )

        return warnings

    @staticmethod
    def confirm_high_risk_operation() -> bool:
        """
        Get user confirmation for high-risk operation

        Returns:
            True if user confirms
        """
        print("\n" + "=" * 60)
        print("HIGH RISK OPERATION CONFIRMATION")
        print("=" * 60)
        print("\nYou are about to perform a high-risk operation.")
        print("Please confirm you understand the risks:")
        print("\n1. I have a backup of system")
        print("2. I understand this may cause service disruption")
        print("3. I have permission to scan this target")
        print("4. I will monitor the system during operation")
        print("5. I can stop the operation if issues occur")
        print("\nType 'I CONFIRM' to proceed:")
        print("=" * 60 + "\n")

        try:
            response = input("> ").strip()
            return response.upper() == "I CONFIRM"
        except KeyboardInterrupt:
            return False

    @staticmethod
    def get_autofix_warnings(findings: List[Dict[str, Any]]) -> List[SafetyWarning]:
        """
        Get safety warnings for auto-fix operations

        Args:
            findings: List of vulnerability findings

        Returns:
            List of safety warnings
        """
        warnings = []

        # General warning
        warnings.append(
            SafetyWarning(
                level=WarningLevel.MEDIUM_RISK,
                title="AUTO-FIX OPERATIONS",
                description="Automatic fixes will be applied to system.",
                impact="System configurations will be modified. Full backup will be created first.",
                mitigations=[
                    "Full backup created automatically",
                    "Review each fix before applying",
                    "Interactive mode available",
                    "Can restore from backup if needed",
                    "Test fixes on staging first",
                ],
                requires_confirmation=True,
            )
        )

        # Count by severity
        critical_count = sum(1 for f in findings if f.get("severity") == "critical")
        high_count = sum(1 for f in findings if f.get("severity") == "high")

        if critical_count > 0 or high_count > 0:
            warnings.append(
                SafetyWarning(
                    level=WarningLevel.HIGH_RISK,
                    title=f"HIGH SEVERITY FINDINGS: {critical_count + high_count}",
                    description=f"Found {critical_count} critical and {high_count} high severity issues.",
                    impact="Fixes for critical/high issues may require system restarts or service interruptions.",
                    mitigations=[
                        "These are serious vulnerabilities",
                        "Fixes may cause downtime",
                        "Schedule maintenance window",
                        "Notify users in advance",
                        "Have rollback plan ready",
                        "Test fixes on staging first",
                    ],
                    requires_confirmation=True,
                )
            )

        return warnings
