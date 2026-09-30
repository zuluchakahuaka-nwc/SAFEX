"""
Token Guard - detects leaked tokens and recommends rotation.

Checks for:
- Bot tokens in source code, configs, and logs
- Tokens in version control history (basic check)
- Token format validation
- Token storage best practices
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from ..config.settings import Settings
from ..utils.logger import get_logger
from .models import (
    BotSecurityFinding,
    FindingCategory,
    RiskLevel,
    PlatformType,
)

logger = get_logger(__name__)

PLATFORM_TOKEN_REGEX: Dict[PlatformType, List[Tuple[str, str, str]]] = {
    PlatformType.TELEGRAM: [
        (
            r"\b(\d{8,10}:[A-Za-z0-9_-]{33,38})\b",
            "Telegram Bot API Token",
            "Rotate via @BotFather -> Revoke token",
        ),
        (
            r"\b(\d{8,10}[A-Za-z0-9_-]{33,38})\b",
            "Potential Telegram Token (malformed)",
            "Check format and rotate if real",
        ),
    ],
    PlatformType.DISCORD: [
        (
            r"\b([A-Za-z0-9_-]{24}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27})\b",
            "Discord Bot Token",
            "Regenerate in Discord Developer Portal",
        ),
    ],
    PlatformType.SLACK: [
        (
            r"\b(xox[baprs]-[A-Za-z0-9-]{10,})\b",
            "Slack Bot/User Token",
            "Rotate in Slack admin dashboard",
        ),
    ],
    PlatformType.VK: [
        (
            r"\b(vk1\.[A-Za-z0-9_-]{20,})\b",
            "VK Access Token",
            "Revoke in VK app settings",
        ),
    ],
}

_ENV_TOKEN_PATTERNS = [
    (r"\.env\b", "Token in .env file — ensure .env is in .gitignore"),
    (r"\.env\.example\b", ".env.example is acceptable if it has placeholder values"),
]

_COMMON_SECRET_FIELDS = [
    "TELEGRAM_TOKEN",
    "DISCORD_TOKEN",
    "SLACK_TOKEN",
    "BOT_TOKEN",
    "WEBHOOK_SECRET",
    "API_KEY",
    "SECRET_KEY",
]


class TokenGuard:
    """Detects leaked tokens and validates token storage practices."""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()

    def scan_file(
        self, file_path: Path, content: Optional[str] = None
    ) -> List[BotSecurityFinding]:
        findings: List[BotSecurityFinding] = []

        if content is None:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                return findings

        name_lower = file_path.name.lower()

        for platform, entries in PLATFORM_TOKEN_REGEX.items():
            for regex, title, remediation in entries:
                for m in re.finditer(regex, content):
                    line_num = content[: m.start()].count("\n") + 1
                    findings.append(
                        BotSecurityFinding(
                            category=FindingCategory.TOKEN_LEAK,
                            risk_level=RiskLevel.CRITICAL,
                            title=f"Leaked {title}",
                            description=(
                                f"A {title} was found in {file_path.name}. "
                                "This allows full control of the bot."
                            ),
                            location=str(file_path),
                            line_number=line_num,
                            code_snippet=m.group(0)[:20] + "...",
                            recommendation=remediation,
                            cwe_id="CWE-798",
                            platform=platform,
                        )
                    )

        if name_lower.endswith((".py", ".js", ".ts")):
            findings.extend(
                self._check_inline_secrets(content, file_path)
            )

        if name_lower == ".env" or name_lower.endswith(".env"):
            findings.extend(self._check_env_file(content, file_path))

        return findings

    def _check_inline_secrets(
        self, code: str, file_path: Path
    ) -> List[BotSecurityFinding]:
        findings: List[BotSecurityFinding] = []
        patterns = [
            (
                r'(?:TELEGRAM_TOKEN|BOT_TOKEN|DISCORD_TOKEN)\s*=\s*["\'][^"\']{10,}["\']',
                "Hardcoded bot token in source code",
            ),
            (
                r'(?:WEBHOOK_SECRET|SECRET_KEY)\s*=\s*["\'][^"\']{6,}["\']',
                "Hardcoded secret in source code",
            ),
            (
                r'(?:API_KEY|PRIVATE_KEY)\s*=\s*["\'][^"\']{10,}["\']',
                "Hardcoded API/private key in source code",
            ),
        ]
        for pat, title in patterns:
            for m in re.finditer(pat, code, re.IGNORECASE):
                line_num = code[: m.start()].count("\n") + 1
                findings.append(
                    BotSecurityFinding(
                        category=FindingCategory.SECRET_STORAGE,
                        risk_level=RiskLevel.CRITICAL,
                        title=title,
                        description=(
                            f"{title}. Use env vars or secret manager."
                        ),
                        location=str(file_path),
                        line_number=line_num,
                        recommendation=(
                            "Move to .env (not committed) or vault. "
                            "Read via os.environ['KEY']."
                        ),
                        cwe_id="CWE-798",
                    )
                )
        return findings

    def _check_env_file(
        self, content: str, file_path: Path
    ) -> List[BotSecurityFinding]:
        findings: List[BotSecurityFinding] = []
        parent = file_path.parent
        gitignore_path = parent / ".gitignore"
        env_is_ignored = False

        if gitignore_path.exists():
            try:
                gi = gitignore_path.read_text(encoding="utf-8", errors="ignore")
                env_is_ignored = ".env" in gi
            except Exception:
                pass

        if not env_is_ignored:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.SECRET_STORAGE,
                    risk_level=RiskLevel.HIGH,
                    title=".env file not in .gitignore",
                    description=(
                        "The .env file contains secrets but may be committed to VCS."
                    ),
                    location=str(file_path),
                    recommendation='Add ".env" to .gitignore.',
                    cwe_id="CWE-312",
                )
            )

        for line_no, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for field in _COMMON_SECRET_FIELDS:
                if field in stripped:
                    value_part = stripped.split("=", 1)[-1].strip().strip('"').strip("'")
                    if value_part and not any(
                        placeholder in value_part.lower()
                        for placeholder in ("your_", "changeme", "xxx", "example", "placeholder")
                    ):
                        findings.append(
                            BotSecurityFinding(
                                category=FindingCategory.SECRET_STORAGE,
                                risk_level=RiskLevel.CRITICAL,
                                title=f"Real secret value in .env: {field}",
                                description=(
                                    f"The field {field} appears to contain a real "
                                    "value, not a placeholder."
                                ),
                                location=str(file_path),
                                line_number=line_no,
                                recommendation="Ensure .env is never committed.",
                                cwe_id="CWE-798",
                            )
                        )
        return findings

    def validate_token_format(
        self, token: str, platform: PlatformType
    ) -> Dict[str, any]:
        patterns = PLATFORM_TOKEN_REGEX.get(platform, [])
        for regex, name, _ in patterns:
            if re.match(regex, token):
                return {"valid_format": True, "type": name, "platform": platform.value}
        return {"valid_format": False, "type": "unknown", "platform": platform.value}

    def scan_directory(
        self, directory: str, max_depth: int = 5
    ) -> List[BotSecurityFinding]:
        findings: List[BotSecurityFinding] = []
        root = Path(directory)
        if not root.is_dir():
            return findings

        exclude = {
            "__pycache__", ".git", "node_modules", ".venv", "venv",
            ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache",
        }

        for fp in root.rglob("*"):
            if any(p.name in exclude for p in fp.parents):
                continue
            if fp.suffix not in (
                ".py", ".js", ".ts", ".env", ".yaml", ".yml", ".json", ".toml",
            ):
                continue
            if fp.name in (".env.example", ".env.template"):
                continue
            findings.extend(self.scan_file(fp))
        return findings
