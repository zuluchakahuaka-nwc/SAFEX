"""
Custom exceptions for SAFEX
"""

from typing import Optional, Any


class SAFEXError(Exception):
    """Base exception for SAFEX"""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details


class ValidationError(SAFEXError):
    """Validation related errors"""

    pass


class EmailError(SAFEXError):
    """Email sending errors"""

    pass


class ScanError(SAFEXError):
    """Scanning errors"""

    pass


class ToolError(SAFEXError):
    """External tool errors (nmap, openvas, etc.)"""

    pass


class ReportError(SAFEXError):
    """Report generation errors"""

    pass


class BackupError(SAFEXError):
    """Backup errors"""

    pass


class AutoFixError(SAFEXError):
    """Auto-fix errors"""

    pass


class ConfigError(SAFEXError):
    """Configuration errors"""

    pass


class AuthenticationError(SAFEXError):
    """Authentication errors"""

    pass


class PermissionError(SAFEXError):
    """Permission errors"""

    pass


class SafetyError(SAFEXError):
    """Safety violations"""

    pass
