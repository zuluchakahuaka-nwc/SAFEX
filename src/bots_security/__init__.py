"""
Bots Security Module - Security scanning and protection for Telegram bots
(and other messaging platform bots).

Provides:
- BotScanner: scans bot source code for security vulnerabilities
- WebhookGuard: validates webhook configuration and signature verification
- TokenGuard: detects leaked tokens and recommends rotation
- AuditChecklist: generates security audit reports for bot owners
- PodmanTemplates: generates secure container deployment configurations
"""

from .models import BotSecurityFinding, BotAuditResult, PlatformType
from .bot_scanner import BotScanner
from .webhook_guard import WebhookGuard
from .token_guard import TokenGuard
from .audit_checklist import AuditChecklist
from .podman_templates import PodmanTemplates

__all__ = [
    "BotScanner",
    "WebhookGuard",
    "TokenGuard",
    "AuditChecklist",
    "PodmanTemplates",
    "BotSecurityFinding",
    "BotAuditResult",
    "PlatformType",
]
