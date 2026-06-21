"""
Webhook Guard - validates webhook security configuration.

Checks:
- HTTPS enforcement
- Secret token verification presence
- Signature verification implementation
- Webhook URL exposure in logs
- Proper error handling
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from ..config.settings import Settings
from ..utils.logger import get_logger
from .models import (
    BotSecurityFinding,
    FindingCategory,
    RiskLevel,
    PlatformType,
)

logger = get_logger(__name__)


class WebhookGuard:
    """Validates webhook security configuration for bots."""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()

    def audit_webhook_code(
        self, code: str, file_path: str, platform: PlatformType = PlatformType.TELEGRAM
    ) -> List[BotSecurityFinding]:
        findings: List[BotSecurityFinding] = []

        if not self._has_webhook(code):
            return findings

        findings.extend(self._check_https(code, file_path))
        findings.extend(self._check_secret_verification(code, file_path, platform))
        findings.extend(self._check_ip_validation(code, file_path, platform))
        findings.extend(self._check_error_handling(code, file_path))
        findings.extend(self._check_payload_size(code, file_path))
        findings.extend(self._check_timeout(code, file_path))

        return findings

    def _has_webhook(self, code: str) -> bool:
        return bool(re.search(r"webhook|/webhook|set_webhook", code, re.IGNORECASE))

    def _check_https(
        self, code: str, file_path: str
    ) -> List[BotSecurityFinding]:
        findings = []
        url_matches = re.findall(
            r'(?:webhook_url|WEBHOOK_URL|set_webhook)\s*[=:]\s*["\']?(http://[^"\']+)["\']?',
            code, re.IGNORECASE,
        )
        for url in url_matches:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.CRITICAL,
                    title="Webhook uses HTTP instead of HTTPS",
                    description=(
                        f"Webhook URL uses insecure HTTP: {url[:50]}. "
                        "Data is transmitted in plaintext."
                    ),
                    location=file_path,
                    cwe_id="CWE-319",
                    recommendation="Use HTTPS for all webhook endpoints.",
                    platform=PlatformType.TELEGRAM,
                    remediation_code='webhook_url = "https://example.com/webhook"',
                )
            )
        return findings

    def _check_secret_verification(
        self, code: str, file_path: str, platform: PlatformType
    ) -> List[BotSecurityFinding]:
        findings = []
        has_webhook_handler = bool(re.search(
            r"@(?:app|bot|router)\.(?:post|route|webhook)", code
        ))
        if not has_webhook_handler:
            return findings

        has_secret = bool(re.search(
            r"X-Telegram-Bot-Api-Secret-Token|secret.?token|"
            r"WEBHOOK_SECRET|hmac\.compare_digest",
            code, re.IGNORECASE,
        ))
        if not has_secret:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.HIGH,
                    title="Webhook handler lacks secret verification",
                    description=(
                        "Webhook endpoint does not verify secret token. "
                        "Anyone who discovers the URL can inject fake updates."
                    ),
                    location=file_path,
                    cwe_id="CWE-345",
                    recommendation=(
                        "Set secret_token in set_webhook and verify "
                        "X-Telegram-Bot-Api-Secret-Token header."
                    ),
                    platform=platform,
                    remediation_code=(
                        'import hmac\n'
                        'secret = os.environ["WEBHOOK_SECRET"]\n'
                        'header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")\n'
                        'if not hmac.compare_digest(header, secret):\n'
                        '    abort(403)'
                    ),
                )
            )
        return findings

    def _check_ip_validation(
        self, code: str, file_path: str, platform: PlatformType
    ) -> List[BotSecurityFinding]:
        findings = []
        has_ip_check = bool(re.search(
            r"remote_addr|client_ip|X-Forwarded-For|telegram.*ip|allowed_ips",
            code, re.IGNORECASE,
        ))
        if not has_ip_check and self._has_webhook(code):
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.NETWORK_EXPOSURE,
                    risk_level=RiskLevel.MEDIUM,
                    title="No IP allowlist for webhook endpoint",
                    description=(
                        "Webhook accepts requests from any IP. "
                        "Consider restricting to Telegram IP ranges."
                    ),
                    location=file_path,
                    recommendation=(
                        "Configure nginx or middleware to allow only "
                        "Telegram IP ranges (149.154.160.0/20, 91.108.4.0/22)."
                    ),
                    platform=platform,
                )
            )
        return findings

    def _check_error_handling(
        self, code: str, file_path: str
    ) -> List[BotSecurityFinding]:
        findings = []
        has_try_catch = bool(re.search(r"try\s*:", code))
        has_webhook_handler = bool(re.search(
            r"@(?:app|bot|router)\.(?:post|route)", code
        ))
        if has_webhook_handler and not has_try_catch:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.MEDIUM,
                    title="Webhook handler lacks error handling",
                    description=(
                        "No try/except in webhook handler. Unhandled exceptions "
                        "may leak stack traces or cause repeated retries."
                    ),
                    location=file_path,
                    recommendation="Wrap handler logic in try/except; return 200 quickly.",
                )
            )
        return findings

    def _check_payload_size(
        self, code: str, file_path: str
    ) -> List[BotSecurityFinding]:
        findings = []
        has_size_limit = bool(re.search(
            r"max_content_length|MAX_CONTENT_LENGTH|content_length|"
            r"client_max_body_size|payload.*size",
            code, re.IGNORECASE,
        ))
        has_webhook = self._has_webhook(code)
        if has_webhook and not has_size_limit:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.LOW,
                    title="No payload size limit for webhook",
                    description="Webhook endpoint has no explicit payload size limit.",
                    location=file_path,
                    recommendation="Limit request body size (e.g., 2 MB max).",
                )
            )
        return findings

    def _check_timeout(
        self, code: str, file_path: str
    ) -> List[BotSecurityFinding]:
        findings = []
        has_timeout = bool(re.search(
            r"timeout|TIMEOUT|proxy_read_timeout", code, re.IGNORECASE,
        ))
        has_webhook = self._has_webhook(code)
        if has_webhook and not has_timeout:
            findings.append(
                BotSecurityFinding(
                    category=FindingCategory.WEBHOOK_MISCONFIG,
                    risk_level=RiskLevel.LOW,
                    title="No timeout configured for webhook processing",
                    description="Webhook handler has no timeout. Long-running handlers can queue up.",
                    location=file_path,
                    recommendation="Set request and response timeouts (e.g., 30s).",
                )
            )
        return findings

    def generate_secure_webhook_template(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> str:
        templates = {
            PlatformType.TELEGRAM: '''import os
import hmac
import tempfile
from flask import Flask, request, abort

app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

ALLOWED_MIME = {"image/png", "image/jpeg", "application/pdf", "text/plain"}
MAX_PAYLOAD = 2 * 1024 * 1024


def verify_secret():
    header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not WEBHOOK_SECRET:
        abort(500)
    return hmac.compare_digest(header, WEBHOOK_SECRET)


@app.route("/webhook", methods=["POST"])
def webhook():
    if not verify_secret():
        abort(403)

    if request.content_length and request.content_length > MAX_PAYLOAD:
        abort(413)

    try:
        data = request.get_json(silent=True, force=True)
        if not data:
            abort(400)
    except Exception:
        abort(400)

    return "", 200


@app.route("/upload", methods=["POST"])
def upload():
    if not verify_secret():
        abort(403)
    f = request.files.get("file")
    if not f:
        abort(400)
    if f.content_length and f.content_length > MAX_PAYLOAD:
        abort(413)
    if f.mimetype not in ALLOWED_MIME:
        abort(415)
    with tempfile.NamedTemporaryFile(
        dir="/tmp/uploads", delete=True
    ) as tmp:
        f.save(tmp.name)
    return "", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
''',
        }
        return templates.get(platform, templates[PlatformType.TELEGRAM])
