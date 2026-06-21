"""
Tests for bots_security module
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.bots_security.models import (
    BotAuditResult,
    BotSecurityFinding,
    FindingCategory,
    PlatformType,
    RiskLevel,
)
from src.bots_security.bot_scanner import BotScanner
from src.bots_security.token_guard import TokenGuard
from src.bots_security.webhook_guard import WebhookGuard
from src.bots_security.audit_checklist import AuditChecklist
from src.bots_security.podman_templates import PodmanTemplates


@pytest.fixture
def tmp_bot_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def vulnerable_bot_code():
    return '''
import os
import pickle
import subprocess

TELEGRAM_TOKEN = "1234567890:AAH_fLhGpXx2vVd1eXzY3wW4uU5sS6rR7tT8"
WEBHOOK_SECRET = "my_super_secret_123"
password = "admin123"

def handle_message(msg):
    eval(msg.text)
    subprocess.call(msg.text, shell=True)
    data = pickle.loads(msg.data)

def webhook():
    pass

def process_file(f):
    f.save("/app/uploads/" + f.name)
'''


@pytest.fixture
def safe_bot_code():
    return '''
import os
import hmac
import json

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")

def verify_secret(request):
    header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    return hmac.compare_digest(header, WEBHOOK_SECRET or "")

def handle_message(msg):
    if msg.text.startswith("/start"):
        pass
'''


class TestModels:
    def test_finding_to_dict(self):
        f = BotSecurityFinding(
            category=FindingCategory.TOKEN_LEAK,
            risk_level=RiskLevel.CRITICAL,
            title="Test",
            description="Test desc",
        )
        d = f.to_dict()
        assert d["category"] == "token_leak"
        assert d["risk_level"] == "CRITICAL"

    def test_audit_result_score(self):
        audit = BotAuditResult(target="test", platform=PlatformType.TELEGRAM)
        assert audit.risk_score == 0.0
        assert audit.passed is True

        audit.add_finding(BotSecurityFinding(
            category=FindingCategory.TOKEN_LEAK,
            risk_level=RiskLevel.CRITICAL,
            title="Leak",
            description="desc",
        ))
        assert audit.risk_score == 25.0
        assert audit.total_findings == 1
        assert "CRITICAL" in audit.severity_count()

    def test_audit_result_passed_threshold(self):
        audit = BotAuditResult(target="test", platform=PlatformType.TELEGRAM)
        for i in range(4):
            audit.add_finding(BotSecurityFinding(
                category=FindingCategory.TOKEN_LEAK,
                risk_level=RiskLevel.CRITICAL,
                title=f"Leak {i}",
                description="desc",
            ))
        assert audit.risk_score == 100.0
        assert audit.passed is False

    def test_audit_to_dict(self):
        audit = BotAuditResult(target="test", platform=PlatformType.TELEGRAM)
        d = audit.to_dict()
        assert d["target"] == "test"
        assert d["platform"] == "telegram"


class TestBotScanner:
    def test_scan_nonexistent_target(self):
        scanner = BotScanner()
        result = scanner.scan("/nonexistent/path")
        assert result["success"] is False

    def test_scan_vulnerable_code(self, tmp_bot_dir, vulnerable_bot_code):
        code_file = tmp_bot_dir / "bot.py"
        code_file.write_text(vulnerable_bot_code, encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["success"] is True
        assert result["total_findings"] > 0
        assert result["risk_score"] > 0

    def test_scan_safe_code(self, tmp_bot_dir, safe_bot_code):
        code_file = tmp_bot_dir / "bot.py"
        code_file.write_text(safe_bot_code, encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["success"] is True
        assert result["total_findings"] == 0

    def test_detect_telegram_platform(self, tmp_bot_dir):
        code_file = tmp_bot_dir / "bot.py"
        code_file.write_text("from telegram import Bot\n", encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["platform"] == "telegram"

    def test_detect_eval(self, tmp_bot_dir):
        code = 'eval(user_input)\n'
        (tmp_bot_dir / "bot.py").write_text(code, encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["total_findings"] >= 1

    def test_detect_command_injection(self, tmp_bot_dir):
        code = 'subprocess.call(cmd, shell=True)\n'
        (tmp_bot_dir / "bot.py").write_text(code, encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["total_findings"] >= 1

    def test_detect_pickle(self, tmp_bot_dir):
        code = 'data = pickle.loads(raw)\n'
        (tmp_bot_dir / "bot.py").write_text(code, encoding="utf-8")

        scanner = BotScanner()
        result = scanner.scan(str(tmp_bot_dir))
        assert result["total_findings"] >= 1


class TestTokenGuard:
    def test_detect_telegram_token(self):
        guard = TokenGuard()
        code = 'TOKEN = "1234567890:AAH_fLhGpXx2vVd1eXzY3wW4uU5sS6rR7tT8"\n'
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            f.flush()
            findings = guard.scan_file(Path(f.name))
        os.unlink(f.name)
        assert len(findings) >= 1
        token_leaks = [
            f for f in findings if f.category == FindingCategory.TOKEN_LEAK
        ]
        assert len(token_leaks) >= 1

    def test_no_false_positive(self):
        guard = TokenGuard()
        code = 'TOKEN = os.environ.get("TELEGRAM_TOKEN")\n'
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            f.flush()
            findings = guard.scan_file(Path(f.name))
        os.unlink(f.name)
        token_leaks = [
            f for f in findings if f.category == FindingCategory.TOKEN_LEAK
        ]
        assert len(token_leaks) == 0

    def test_validate_token_format(self):
        guard = TokenGuard()
        result = guard.validate_token_format(
            "1234567890:AAH_fLhGpXx2vVd1eXzY3wW4uU5sS6rR7tT8",
            PlatformType.TELEGRAM,
        )
        assert result["valid_format"] is True

    def test_validate_bad_token(self):
        guard = TokenGuard()
        result = guard.validate_token_format(
            "not_a_token", PlatformType.TELEGRAM
        )
        assert result["valid_format"] is False

    def test_env_file_check(self):
        guard = TokenGuard()
        with tempfile.TemporaryDirectory() as td:
            env_file = Path(td) / ".env"
            env_file.write_text(
                "TELEGRAM_TOKEN=1234567890:AAH_real_token_here_xxxxxxxxxxxxxxxxxxx\n",
                encoding="utf-8",
            )
            findings = guard.scan_file(env_file)
            categories = {f.category for f in findings}
            assert FindingCategory.SECRET_STORAGE in categories

    def test_scan_directory(self, tmp_bot_dir):
        (tmp_bot_dir / "bot.py").write_text(
            'TOKEN = "1234567890:AAH_fLhGpXx2vVd1eXzY3wW4uU5sS6rR7tT8"\n',
            encoding="utf-8",
        )
        guard = TokenGuard()
        findings = guard.scan_directory(str(tmp_bot_dir))
        assert len(findings) >= 1


class TestWebhookGuard:
    def test_detect_http_webhook(self):
        guard = WebhookGuard()
        code = 'webhook_url = "http://example.com/webhook"\n'
        findings = guard.audit_webhook_code(code, "bot.py")
        https_issues = [
            f for f in findings
            if f.title == "Webhook uses HTTP instead of HTTPS"
        ]
        assert len(https_issues) >= 1

    def test_detect_missing_secret(self):
        guard = WebhookGuard()
        code = '''
from flask import Flask, request
app = Flask(__name__)

@app.post("/webhook")
def webhook():
    data = request.json
    return "ok"
'''
        findings = guard.audit_webhook_code(code, "bot.py")
        secret_issues = [
            f for f in findings
            if "secret" in f.title.lower()
        ]
        assert len(secret_issues) >= 1

    def test_generate_template(self):
        guard = WebhookGuard()
        template = guard.generate_secure_webhook_template(PlatformType.TELEGRAM)
        assert "hmac.compare_digest" in template
        assert "WEBHOOK_SECRET" in template


class TestAuditChecklist:
    def test_generate_full_checklist(self):
        audit = AuditChecklist()
        checklist = audit.generate_full_checklist(PlatformType.TELEGRAM)
        assert checklist["platform"] == "telegram"
        assert checklist["total_checks"] > 0
        assert len(checklist["sections"]) == 3

    def test_generate_from_audit(self):
        bot_audit = BotAuditResult(
            target="test", platform=PlatformType.TELEGRAM
        )
        bot_audit.add_finding(BotSecurityFinding(
            category=FindingCategory.SECRET_STORAGE,
            risk_level=RiskLevel.CRITICAL,
            title="Leak",
            description="desc",
        ))
        bot_audit.add_finding(BotSecurityFinding(
            category=FindingCategory.WEBHOOK_MISCONFIG,
            risk_level=RiskLevel.HIGH,
            title="Bad webhook",
            description="desc",
        ))
        audit = AuditChecklist()
        result = audit.generate_from_audit(bot_audit)
        assert result["total_failed"] >= 1
        assert result["total_passed"] >= 1

    def test_generate_incident_response(self):
        audit = AuditChecklist()
        steps = audit.generate_incident_response(PlatformType.TELEGRAM)
        assert len(steps) == 7
        assert steps[0]["action"] == "Revoke compromised token immediately"

    def test_generate_text_report(self):
        audit = AuditChecklist()
        report = audit.generate_text_report(PlatformType.TELEGRAM)
        assert "SAFEX" in report
        assert "HIGH PRIORITY" in report
        assert "Incident Response" in report


class TestPodmanTemplates:
    def test_generate_dockerfile(self):
        templates = PodmanTemplates()
        df = templates.generate_dockerfile(PlatformType.TELEGRAM)
        assert "botuser" in df
        assert "USER botuser" in df

    def test_generate_podman_compose(self):
        templates = PodmanTemplates()
        compose = templates.generate_podman_compose(
            PlatformType.TELEGRAM, "mybot.example.com"
        )
        assert "TELEGRAM_TOKEN" in compose
        assert "no-new-privileges" in compose
        assert "cap_drop" in compose

    def test_generate_nginx_config(self):
        templates = PodmanTemplates()
        nginx = templates.generate_nginx_config("mybot.example.com")
        assert "443 ssl" in nginx
        assert "TLSv1.2" in nginx
        assert "limit_req" in nginx

    def test_generate_systemd_unit(self):
        templates = PodmanTemplates()
        unit = templates.generate_systemd_unit(PlatformType.TELEGRAM)
        assert "NoNewPrivileges=yes" in unit
        assert "botuser" in unit

    def test_generate_all(self):
        templates = PodmanTemplates()
        all_files = templates.generate_all(PlatformType.TELEGRAM)
        assert "Containerfile" in all_files
        assert "podman-compose.yml" in all_files
        assert "nginx/nginx.conf" in all_files
        assert "systemd/bot.service" in all_files
        assert ".env.example" in all_files


class TestScannerIntegration:
    def test_scanner_factory_creates_bot_scanner(self):
        from src.scanners.scanner_factory import ScannerFactory
        scanner = ScannerFactory.create_scanner("bot")
        assert scanner.get_name() == "Bot Security Scanner"

    def test_scanner_factory_lists_bot_scanner(self):
        from src.scanners.scanner_factory import ScannerFactory
        ScannerFactory._ensure_bot_scanner()
        available = ScannerFactory.get_available_scanners()
        assert "bot" in available
