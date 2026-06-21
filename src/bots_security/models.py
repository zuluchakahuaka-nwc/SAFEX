"""
Data models for bots security module
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


class PlatformType(str, Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    SLACK = "slack"
    VK = "vk"
    VIBER = "viber"
    WHATSAPP = "whatsapp"
    GENERIC = "generic"


class FindingCategory(str, Enum):
    TOKEN_LEAK = "token_leak"
    WEBHOOK_MISCONFIG = "webhook_misconfig"
    INPUT_VALIDATION = "input_validation"
    FILE_UPLOAD = "file_upload"
    INSECURE_DEPENDENCY = "insecure_dependency"
    PERMISSION_FLAW = "permission_flaw"
    CONTAINER_SECURITY = "container_security"
    NETWORK_EXPOSURE = "network_exposure"
    LOGGING_LEAK = "logging_leak"
    DESERIALIZATION = "deserialization"
    COMMAND_INJECTION = "command_injection"
    RATE_LIMITING = "rate_limiting"
    SECRET_STORAGE = "secret_storage"


class RiskLevel(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class BotSecurityFinding:
    category: FindingCategory
    risk_level: RiskLevel
    title: str
    description: str
    location: str = ""
    code_snippet: str = ""
    line_number: int = 0
    recommendation: str = ""
    cwe_id: str = ""
    platform: PlatformType = PlatformType.GENERIC
    remediation_code: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "risk_level": self.risk_level.value,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "code_snippet": self.code_snippet,
            "line_number": self.line_number,
            "recommendation": self.recommendation,
            "cwe_id": self.cwe_id,
            "platform": self.platform.value,
        }


@dataclass
class BotAuditResult:
    target: str
    platform: PlatformType
    findings: List[BotSecurityFinding] = field(default_factory=list)
    scan_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    total_findings: int = 0
    risk_score: float = 0.0
    passed: bool = True

    def add_finding(self, finding: BotSecurityFinding):
        self.findings.append(finding)
        self.total_findings = len(self.findings)
        self._recalculate_score()

    def _recalculate_score(self):
        weights = {
            RiskLevel.CRITICAL: 25.0,
            RiskLevel.HIGH: 15.0,
            RiskLevel.MEDIUM: 7.0,
            RiskLevel.LOW: 3.0,
            RiskLevel.INFO: 0.0,
        }
        total = sum(
            weights.get(f.risk_level, 0.0) for f in self.findings
        )
        self.risk_score = min(total, 100.0)
        self.passed = self.risk_score < 40.0

    def severity_count(self) -> Dict[str, int]:
        count: Dict[str, int] = {}
        for f in self.findings:
            key = f.risk_level.value
            count[key] = count.get(key, 0) + 1
        return count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target,
            "platform": self.platform.value,
            "findings": [f.to_dict() for f in self.findings],
            "scan_timestamp": self.scan_timestamp,
            "total_findings": self.total_findings,
            "risk_score": self.risk_score,
            "passed": self.passed,
            "severity_count": self.severity_count(),
        }
