"""
Audit Checklist Generator - produces a prioritized security audit report
for bot owners with actionable recommendations.
"""

from typing import Dict, List, Optional, Any
from ..config.settings import Settings
from ..utils.logger import get_logger
from .models import (
    BotAuditResult,
    BotSecurityFinding,
    FindingCategory,
    RiskLevel,
    PlatformType,
)

logger = get_logger(__name__)

HIGH_PRIORITY_CHECKS = [
    {
        "id": "A-001",
        "title": "Token Storage & Rotation",
        "description": (
            "Bot tokens must be stored in a secret manager or env vars, "
            "never in source code. Rotate tokens regularly."
        ),
        "category": FindingCategory.SECRET_STORAGE,
        "severity": RiskLevel.CRITICAL,
        "checks": [
            "No tokens in source code",
            "Tokens stored in env vars or vault",
            "Tokens not in VCS history",
            "Rotation policy documented",
        ],
    },
    {
        "id": "A-002",
        "title": "Webhook Secret Verification",
        "description": (
            "Verify X-Telegram-Bot-Api-Secret-Token header on every "
            "webhook request. Reject requests without valid secret."
        ),
        "category": FindingCategory.WEBHOOK_MISCONFIG,
        "severity": RiskLevel.HIGH,
        "checks": [
            "Secret token set via set_webhook",
            "Header verified on each request",
            "Constant-time comparison (hmac.compare_digest)",
            "Reject invalid with 403",
        ],
    },
    {
        "id": "A-003",
        "title": "HTTPS for Webhooks",
        "description": "All webhook URLs must use HTTPS with valid TLS certificates.",
        "category": FindingCategory.WEBHOOK_MISCONFIG,
        "severity": RiskLevel.HIGH,
        "checks": [
            "Webhook URL uses HTTPS",
            "Valid TLS certificate from trusted CA",
            "TLS 1.2+ with strong ciphers",
            "Auto-renewal configured",
        ],
    },
    {
        "id": "A-004",
        "title": "Input Validation & Sanitization",
        "description": (
            "Never eval/exec user data. Whitelist commands. "
            "Sanitize all input before processing."
        ),
        "category": FindingCategory.INPUT_VALIDATION,
        "severity": RiskLevel.HIGH,
        "checks": [
            "No eval/exec on user input",
            "Command whitelist",
            "Input length limits",
            "Type validation",
        ],
    },
    {
        "id": "A-005",
        "title": "File Upload Security",
        "description": (
            "Validate MIME type, file size, scan for malware. "
            "Save outside webroot, no execute permissions."
        ),
        "category": FindingCategory.FILE_UPLOAD,
        "severity": RiskLevel.HIGH,
        "checks": [
            "MIME type whitelist",
            "Max file size enforced",
            "Files saved outside webroot",
            "No execute permissions",
            "Antivirus scan if possible",
        ],
    },
    {
        "id": "A-006",
        "title": "Unprivileged Runtime",
        "description": (
            "Run bot as non-root user in container. "
            "Drop capabilities, read-only FS where possible."
        ),
        "category": FindingCategory.CONTAINER_SECURITY,
        "severity": RiskLevel.HIGH,
        "checks": [
            "Non-root user in container",
            "Read-only filesystem",
            "Dropped capabilities",
            "no-new-privileges",
        ],
    },
    {
        "id": "A-007",
        "title": "Network Isolation",
        "description": (
            "Run bot in isolated network. Only expose nginx/LB. "
            "Block outbound except needed endpoints."
        ),
        "category": FindingCategory.NETWORK_EXPOSURE,
        "severity": RiskLevel.HIGH,
        "checks": [
            "Private container network",
            "Only reverse proxy exposed",
            "Outbound restricted",
            "Firewall configured",
        ],
    },
]

MEDIUM_PRIORITY_CHECKS = [
    {
        "id": "B-001",
        "title": "Rate Limiting",
        "description": "Implement rate limiting to prevent flood and abuse.",
        "category": FindingCategory.RATE_LIMITING,
        "severity": RiskLevel.MEDIUM,
        "checks": [
            "Per-user rate limit",
            "Global rate limit",
            "Burst handling",
            "Timeout on slow requests",
        ],
    },
    {
        "id": "B-002",
        "title": "Dependency Audit",
        "description": "Keep dependencies updated. Run vulnerability scanners.",
        "category": FindingCategory.INSECURE_DEPENDENCY,
        "severity": RiskLevel.MEDIUM,
        "checks": [
            "pip-audit / npm audit regular",
            "Pin dependency versions",
            "Minimal dependencies",
            "Supply chain verification",
        ],
    },
    {
        "id": "B-003",
        "title": "Logging & Monitoring",
        "description": "Log security events. Never log secrets. Set up alerts.",
        "category": FindingCategory.LOGGING_LEAK,
        "severity": RiskLevel.MEDIUM,
        "checks": [
            "No secrets in logs",
            "Failed auth logged",
            "Anomaly alerts configured",
            "Log retention policy",
        ],
    },
    {
        "id": "B-004",
        "title": "Container Resource Limits",
        "description": "Set memory/CPU limits and timeouts.",
        "category": FindingCategory.CONTAINER_SECURITY,
        "severity": RiskLevel.MEDIUM,
        "checks": [
            "Memory limit set",
            "CPU limit set",
            "Request timeouts",
            "Health checks configured",
        ],
    },
]

LOW_PRIORITY_CHECKS = [
    {
        "id": "C-001",
        "title": "Admin Endpoint Protection",
        "description": "Protect admin endpoints with IP allowlist and auth.",
        "category": FindingCategory.PERMISSION_FLAW,
        "severity": RiskLevel.LOW,
        "checks": [
            "IP allowlist for admin",
            "Additional auth layer",
            "Not publicly accessible",
        ],
    },
    {
        "id": "C-002",
        "title": "Backup & Incident Response",
        "description": "Regular backups. Documented incident response plan.",
        "category": FindingCategory.PERMISSION_FLAW,
        "severity": RiskLevel.LOW,
        "checks": [
            "Regular backups",
            "Incident response plan",
            "Token revocation procedure",
            "Forensic capability",
        ],
    },
]

ALL_CHECKS = HIGH_PRIORITY_CHECKS + MEDIUM_PRIORITY_CHECKS + LOW_PRIORITY_CHECKS


class AuditChecklist:
    """Generates security audit checklists for bot owners."""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()

    def generate_full_checklist(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> Dict[str, Any]:
        return {
            "platform": platform.value,
            "sections": [
                {
                    "priority": "HIGH",
                    "items": [
                        self._format_check(c, platform) for c in HIGH_PRIORITY_CHECKS
                    ],
                },
                {
                    "priority": "MEDIUM",
                    "items": [
                        self._format_check(c, platform) for c in MEDIUM_PRIORITY_CHECKS
                    ],
                },
                {
                    "priority": "LOW",
                    "items": [
                        self._format_check(c, platform) for c in LOW_PRIORITY_CHECKS
                    ],
                },
            ],
            "total_checks": len(ALL_CHECKS),
        }

    def generate_from_audit(
        self, audit: BotAuditResult
    ) -> Dict[str, Any]:
        covered_categories = {f.category for f in audit.findings}
        passed_checks = []
        failed_checks = []

        for check in ALL_CHECKS:
            entry = self._format_check(check, audit.platform)
            if check["category"] in covered_categories:
                failed_checks.append({**entry, "status": "FAIL"})
            else:
                passed_checks.append({**entry, "status": "PASS"})

        return {
            "platform": audit.platform.value,
            "target": audit.target,
            "risk_score": audit.risk_score,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "total_passed": len(passed_checks),
            "total_failed": len(failed_checks),
            "severity_count": audit.severity_count(),
        }

    def generate_incident_response(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> List[Dict[str, str]]:
        return [
            {
                "step": "1",
                "action": "Revoke compromised token immediately",
                "detail": (
                    f"Use {'@BotFather' if platform == PlatformType.TELEGRAM else 'platform admin'} "
                    "to revoke and generate new token."
                ),
            },
            {
                "step": "2",
                "action": "Isolate affected host/container",
                "detail": "Stop container, take snapshot for forensics.",
            },
            {
                "step": "3",
                "action": "Rotate all secrets",
                "detail": "Webhook secret, API keys, database credentials.",
            },
            {
                "step": "4",
                "action": "Review logs for lateral movement",
                "detail": "Check for unauthorized API calls, data exfiltration.",
            },
            {
                "step": "5",
                "action": "Patch root cause",
                "detail": "Fix the vulnerability that led to compromise.",
            },
            {
                "step": "6",
                "action": "Deploy clean instance",
                "detail": "Deploy from clean backup with new secrets.",
            },
            {
                "step": "7",
                "action": "Notify stakeholders",
                "detail": "Inform users if data was compromised.",
            },
        ]

    def generate_text_report(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> str:
        lines = [
            "=" * 60,
            f"  SAFEX Bot Security Audit Checklist — {platform.value.upper()}",
            "=" * 60,
            "",
        ]
        for section_checks, label in [
            (HIGH_PRIORITY_CHECKS, "HIGH PRIORITY"),
            (MEDIUM_PRIORITY_CHECKS, "MEDIUM PRIORITY"),
            (LOW_PRIORITY_CHECKS, "LOWER PRIORITY / ONGOING"),
        ]:
            lines.append(f"--- {label} ---")
            for check in section_checks:
                lines.append(f"")
                lines.append(f"  [{check['id']}] {check['title']}")
                lines.append(f"  Severity: {check['severity'].value}")
                lines.append(f"  {check['description']}")
                lines.append(f"  Checklist:")
                for c in check["checks"]:
                    lines.append(f"    [ ] {c}")
            lines.append("")

        lines.append("")
        lines.append("=" * 60)
        lines.append("  Quick Incident Response Steps")
        lines.append("=" * 60)
        for step in self.generate_incident_response(platform):
            lines.append(f"  Step {step['step']}: {step['action']}")
            lines.append(f"    -> {step['detail']}")
        return "\n".join(lines)

    @staticmethod
    def _format_check(check: Dict, platform: PlatformType) -> Dict[str, Any]:
        return {
            "id": check["id"],
            "title": check["title"],
            "description": check["description"],
            "severity": check["severity"].value,
            "category": check["category"].value,
            "checks": check["checks"],
        }
