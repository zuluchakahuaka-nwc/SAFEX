"""
Bot Security Scanner - scans bot source code for security vulnerabilities.

Extends BaseScanner and integrates with the SAFEX scanner infrastructure.
Performs deep analysis specific to messaging bot platforms.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..scanners.base_scanner import BaseScanner
from ..config.settings import Settings
from ..utils.logger import get_logger
from .models import (
    BotSecurityFinding,
    BotAuditResult,
    PlatformType,
    FindingCategory,
    RiskLevel,
)
from .token_guard import TokenGuard
from .webhook_guard import WebhookGuard

logger = get_logger(__name__)

_TOKEN_PATTERNS: Dict[PlatformType, List[Dict[str, str]]] = {
    PlatformType.TELEGRAM: [
        {
            "pattern": r'\b\d{8,10}:[A-Za-z0-9_-]{33,38}\b',
            "name": "Telegram Bot Token",
            "cwe": "CWE-798",
        },
    ],
    PlatformType.DISCORD: [
        {
            "pattern": r'\b[A-Za-z0-9_-]{24}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27}\b',
            "name": "Discord Bot Token",
            "cwe": "CWE-798",
        },
    ],
    PlatformType.SLACK: [
        {
            "pattern": r'\bxox[baprs]-[A-Za-z0-9-]{10,}',
            "name": "Slack Token",
            "cwe": "CWE-798",
        },
    ],
}

_EVAL_PATTERNS = [
    {
        "pattern": r"\beval\s*\(",
        "title": "Use of eval() with potentially unsafe data",
        "severity": RiskLevel.CRITICAL,
        "category": FindingCategory.INPUT_VALIDATION,
        "cwe": "CWE-95",
    },
    {
        "pattern": r"\bexec\s*\(",
        "title": "Use of exec() with potentially unsafe data",
        "severity": RiskLevel.CRITICAL,
        "category": FindingCategory.INPUT_VALIDATION,
        "cwe": "CWE-95",
    },
    {
        "pattern": r"subprocess\.\w+\([^)]*shell\s*=\s*True",
        "title": "Subprocess call with shell=True",
        "severity": RiskLevel.HIGH,
        "category": FindingCategory.COMMAND_INJECTION,
        "cwe": "CWE-77",
    },
    {
        "pattern": r"os\.system\s*\(",
        "title": "Use of os.system()",
        "severity": RiskLevel.HIGH,
        "category": FindingCategory.COMMAND_INJECTION,
        "cwe": "CWE-78",
    },
]

_FILE_UPLOAD_PATTERNS = [
    {
        "pattern": r"(?:download|save|write).*file",
        "title": "File download/save without visible validation",
        "severity": RiskLevel.MEDIUM,
        "category": FindingCategory.FILE_UPLOAD,
        "cwe": "CWE-434",
    },
]

_DESERIALIZATION_PATTERNS = [
    {
        "pattern": r"pickle\.loads?\s*\(",
        "title": "Insecure pickle deserialization",
        "severity": RiskLevel.HIGH,
        "category": FindingCategory.DESERIALIZATION,
        "cwe": "CWE-502",
    },
    {
        "pattern": r"yaml\.load\s*\([^)]*\)(?!.*Loader)",
        "title": "Unsafe yaml.load() without Loader",
        "severity": RiskLevel.HIGH,
        "category": FindingCategory.DESERIALIZATION,
        "cwe": "CWE-502",
    },
]

_LOGGING_PATTERNS = [
    {
        "pattern": r"(?:logger|log|print)\s*\([^)]*(?:token|password|secret|key)",
        "title": "Potential secret leakage in logging",
        "severity": RiskLevel.HIGH,
        "category": FindingCategory.LOGGING_LEAK,
        "cwe": "CWE-532",
    },
]


class BotScanner(BaseScanner):
    """Scanner for messaging bot security vulnerabilities."""

    SUPPORTED_EXTENSIONS = {
        ".py", ".js", ".ts", ".env", ".yaml", ".yml", ".json", ".toml",
    }

    def __init__(self, config: Optional[Settings] = None):
        super().__init__(config)
        self.token_guard = TokenGuard()
        self.webhook_guard = WebhookGuard()

    def get_name(self) -> str:
        return "Bot Security Scanner"

    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        opts = options or {}
        target_path = Path(target)

        if not target_path.exists():
            return {
                "success": False,
                "error": f"Target not found: {target}",
                "findings": [],
            }

        platform = self._detect_platform(target_path)
        audit = BotAuditResult(target=str(target_path), platform=platform)

        files = self._collect_files(target_path, opts)
        for fp in files:
            code = self._read_file(fp)
            if code is None:
                continue
            self._scan_tokens(code, fp, platform, audit)
            self._scan_patterns(
                code, fp, _EVAL_PATTERNS + _FILE_UPLOAD_PATTERNS
                + _DESERIALIZATION_PATTERNS + _LOGGING_PATTERNS,
                audit,
            )
            self._scan_hardcoded_secrets(code, fp, audit)
            self._scan_rate_limiting(code, fp, audit)
            self._scan_webhook_usage(code, fp, audit)

        self.scan_results.append(audit.to_dict())
        return {
            "success": True,
            "target": target,
            "scanner": self.get_name(),
            "platform": platform.value,
            "findings": [f.to_dict() for f in audit.findings],
            "total_findings": audit.total_findings,
            "risk_score": audit.risk_score,
            "passed": audit.passed,
            "severity_count": audit.severity_count(),
        }

    def _detect_platform(self, path: Path) -> PlatformType:
        name = path.name.lower() if path.is_file() else ""
        if not path.is_dir():
            return PlatformType.GENERIC
        try:
            children = [p.name.lower() for p in path.iterdir()]
        except OSError:
            return PlatformType.GENERIC

        files_text = " ".join(children)
        try:
            for f in path.rglob("*.py"):
                content = self._read_file(f)
                if content and "telegram" in content.lower():
                    return PlatformType.TELEGRAM
                if content and "discord" in content.lower():
                    return PlatformType.DISCORD
                if content and "slack" in content.lower():
                    return PlatformType.SLACK
        except Exception:
            pass

        if "telegram" in files_text:
            return PlatformType.TELEGRAM
        if "discord" in files_text:
            return PlatformType.DISCORD
        return PlatformType.GENERIC

    def _collect_files(
        self, path: Path, opts: Dict[str, Any]
    ) -> List[Path]:
        if path.is_file():
            return [path] if path.suffix in self.SUPPORTED_EXTENSIONS else []
        exclude_dirs = {
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            "venv-env", ".tox", ".mypy_cache", ".pytest_cache",
        }
        max_files = opts.get("max_files", 500)
        result: List[Path] = []
        for f in path.rglob("*"):
            if any(p.name in exclude_dirs for p in f.parents):
                continue
            if f.is_file() and f.suffix in self.SUPPORTED_EXTENSIONS:
                result.append(f)
                if len(result) >= max_files:
                    break
        return result

    def _read_file(self, path: Path) -> Optional[str]:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None

    def _scan_tokens(
        self,
        code: str,
        path: Path,
        platform: PlatformType,
        audit: BotAuditResult,
    ):
        platforms = [platform]
        if platform == PlatformType.GENERIC:
            platforms = list(PlatformType)
        for plat in platforms:
            patterns = _TOKEN_PATTERNS.get(plat, [])
            for entry in patterns:
                for m in re.finditer(entry["pattern"], code):
                    line_num = code[: m.start()].count("\n") + 1
                    audit.add_finding(
                        BotSecurityFinding(
                            category=FindingCategory.TOKEN_LEAK,
                            risk_level=RiskLevel.CRITICAL,
                            title=f"Leaked {entry['name']}",
                            description=(
                                f"A {entry['name']} was found in plain text. "
                                "Rotate the token immediately."
                            ),
                            location=str(path),
                            line_number=line_num,
                            cwe_id=entry.get("cwe", ""),
                            recommendation="Rotate token and use env vars / vault.",
                            platform=plat,
                        )
                    )

    def _scan_hardcoded_secrets(
        self, code: str, path: Path, audit: BotAuditResult
    ):
        secret_patterns = {
            r'password\s*=\s*["\'][^"\']{4,}["\']': "Hardcoded password",
            r'api[_-]?key\s*=\s*["\'][^"\']{8,}["\']': "Hardcoded API key",
            r'secret[_-]?key\s*=\s*["\'][^"\']{8,}["\']': "Hardcoded secret key",
            r'private[_-]?key\s*=\s*["\'][^"\']{16,}["\']': "Hardcoded private key",
            r'WEBHOOK_SECRET\s*=\s*["\'][^"\']{4,}["\']': "Hardcoded webhook secret",
        }
        for pat, desc in secret_patterns.items():
            for m in re.finditer(pat, code, re.IGNORECASE):
                line_num = code[: m.start()].count("\n") + 1
                audit.add_finding(
                    BotSecurityFinding(
                        category=FindingCategory.SECRET_STORAGE,
                        risk_level=RiskLevel.CRITICAL,
                        title=desc,
                        description=f"{desc} detected in source code.",
                        location=str(path),
                        code_snippet=m.group(0)[:80],
                        line_number=line_num,
                        cwe_id="CWE-798",
                        recommendation="Use environment variables or secret manager.",
                    )
                )

    def _scan_patterns(
        self,
        code: str,
        path: Path,
        patterns: List[Dict[str, Any]],
        audit: BotAuditResult,
    ):
        for entry in patterns:
            for m in re.finditer(entry["pattern"], code):
                line_num = code[: m.start()].count("\n") + 1
                audit.add_finding(
                    BotSecurityFinding(
                        category=entry["category"],
                        risk_level=entry["severity"],
                        title=entry["title"],
                        description=entry["title"],
                        location=str(path),
                        code_snippet=m.group(0)[:120],
                        line_number=line_num,
                        cwe_id=entry.get("cwe", ""),
                        recommendation=self._remediation_for(entry["category"]),
                    )
                )

    def _scan_rate_limiting(self, code: str, path: Path, audit: BotAuditResult):
        handler_count = len(re.findall(
            r"@(?:app|bot|router)\.(?:message|command|callback_query)", code
        ))
        has_rate_limit = bool(re.search(
            r"rate.?limit|throttl|RateLimiter|ThrottleMiddleware", code, re.IGNORECASE
        ))
        if handler_count > 2 and not has_rate_limit:
            audit.add_finding(
                BotSecurityFinding(
                    category=FindingCategory.RATE_LIMITING,
                    risk_level=RiskLevel.MEDIUM,
                    title="No rate limiting detected",
                    description=(
                        f"Bot has {handler_count} message handlers but no "
                        "rate-limiting middleware. Susceptible to flood/spam."
                    ),
                    location=str(path),
                    recommendation="Add rate limiting middleware.",
                )
            )

    def _scan_webhook_usage(self, code: str, path: Path, audit: BotAuditResult):
        has_webhook_handler = bool(re.search(
            r"@(?:app|bot|router)\.(?:post|route|webhook)|"
            r"(?:set_webhook|webhook_url)\s*[=:(]|"
            r"def\s+webhook\s*\(",
            code, re.IGNORECASE,
        ))
        if not has_webhook_handler:
            return
        if "https://" not in code and "ssl" not in code.lower():
            audit.add_finding(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.HIGH,
                    title="Webhook without HTTPS",
                    description="Webhook URL detected without TLS.",
                    location=str(path),
                    cwe_id="CWE-319",
                    recommendation="Use HTTPS for all webhook endpoints.",
                )
            )
        has_secret_check = bool(re.search(
            r"secret.?token|X-Telegram-Bot-Api-Secret-Token|hmac\.compare_digest",
            code, re.IGNORECASE,
        ))
        if not has_secret_check:
            audit.add_finding(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.HIGH,
                    title="Webhook without secret verification",
                    description=(
                        "Webhook handler does not verify the secret token. "
                        "Attackers could forge requests."
                    ),
                    location=str(path),
                    cwe_id="CWE-345",
                    recommendation="Verify X-Telegram-Bot-Api-Secret-Token header.",
                )
            )

    @staticmethod
    def _remediation_for(category: FindingCategory) -> str:
        rem = {
            FindingCategory.INPUT_VALIDATION: (
                "Never eval/exec untrusted data. Use whitelists and parsers."
            ),
            FindingCategory.COMMAND_INJECTION: (
                "Avoid shell=True. Use argument lists for subprocess."
            ),
            FindingCategory.FILE_UPLOAD: (
                "Validate MIME type, size, and scan for malware before saving."
            ),
            FindingCategory.DESERIALIZATION: (
                "Use safe_load / json.loads. Never unpickle untrusted data."
            ),
            FindingCategory.LOGGING_LEAK: (
                "Never log tokens, passwords or secrets. Redact sensitive fields."
            ),
        }
        return rem.get(category, "Review and apply security best practices.")
