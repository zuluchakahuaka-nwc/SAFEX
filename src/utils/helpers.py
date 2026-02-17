"""
Helper functions for SAFEX
"""

import uuid
import secrets
import string
import re
import ipaddress
from datetime import datetime
from typing import Optional
from pathlib import Path


def generate_uuid() -> str:
    """Generate a unique UUID"""
    return str(uuid.uuid4())


def generate_token(length: int = 32) -> str:
    """Generate a random token"""
    return secrets.token_urlsafe(length)


def generate_verification_code(length: int = 6) -> str:
    """Generate a numeric verification code"""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def validate_ip(ip: str) -> bool:
    """Validate IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_domain(domain: str) -> bool:
    """Validate domain name"""
    pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
    return re.match(pattern, domain) is not None


def validate_email(email: str) -> bool:
    """Validate email address"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def get_current_timestamp() -> str:
    """Get current ISO timestamp"""
    return datetime.utcnow().isoformat()


def ensure_directory(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: dict, file_path: Path) -> None:
    """Save data to JSON file"""
    import json

    ensure_directory(file_path.parent)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: Path) -> Optional[dict]:
    """Load data from JSON file"""
    import json

    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return None
    return None


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def calculate_risk_score(findings: list) -> float:
    """Calculate risk score from findings"""
    severity_weights = {"critical": 10, "high": 7, "medium": 4, "low": 1}

    total_score = 0
    total_findings = 0

    for finding in findings:
        severity = finding.get("severity", "medium").lower()
        total_score += severity_weights.get(severity, 4)
        total_findings += 1

    if total_findings == 0:
        return 0.0

    avg_score = total_score / total_findings
    return min(avg_score, 10.0)
