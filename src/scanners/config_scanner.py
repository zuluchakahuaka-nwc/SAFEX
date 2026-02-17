"""
Config Scanner Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
import json
from .base_scanner import BaseScanner
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ConfigScanner(BaseScanner):
    """Scanner for configuration files"""

    def __init__(self, config: Optional[Settings] = None):
        super().__init__(config)
        self.supported_formats = [
            ".yaml",
            ".yml",
            ".json",
            ".xml",
            ".ini",
            ".conf",
            ".cfg",
        ]

    def get_name(self) -> str:
        return "Configuration File Scanner"

    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan configuration file for security issues

        Args:
            target: Path to config file
            options: Scan options

        Returns:
            Scan results
        """
        logger.info(f"Scanning config file: {target}")

        path = Path(target)

        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {target}",
                "findings": [],
            }

        if not path.suffix.lower() in self.supported_formats:
            return {
                "success": False,
                "error": f"Unsupported format: {path.suffix}",
                "findings": [],
            }

        findings = []

        # Load config
        config_data = self._load_config(path)

        if config_data is None:
            return {
                "success": False,
                "error": "Failed to load configuration",
                "findings": [],
            }

        # Scan for issues
        findings.extend(self._check_insecure_defaults(config_data, path))
        findings.extend(self._check_exposed_secrets(config_data, path))
        findings.extend(self._check_weak_encryption(config_data, path))
        findings.extend(self._check_insecure_permissions(path))

        result = {
            "success": True,
            "target": target,
            "scanner": self.get_name(),
            "findings": findings,
            "total_findings": len(findings),
            "severity_count": self._count_by_severity(findings),
        }

        self.scan_results.append(result)

        return result

    def _load_config(self, path: Path) -> Optional[Dict[str, Any]]:
        """Load configuration file"""
        try:
            if path.suffix in [".yaml", ".yml"]:
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            elif path.suffix == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            elif path.suffix in [".ini", ".conf", ".cfg"]:
                # Simple parsing for INI-like files
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    return {"raw_content": content}
            elif path.suffix == ".xml":
                # Simplified XML handling
                import xml.etree.ElementTree as ET

                tree = ET.parse(path)
                root = tree.getroot()
                return {"xml_root": root.tag}

            return None

        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return None

    def _check_insecure_defaults(
        self, config: Dict[str, Any], path: Path
    ) -> List[Dict[str, Any]]:
        """Check for insecure default values"""
        findings = []

        insecure_patterns = {
            "password": ["password", "123456", "admin", "root"],
            "secret": ["secret", "default"],
            "key": ["private_key", "public_key"],
            "token": ["default_token", "test_token"],
        }

        def check_dict(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    check_dict(value, new_prefix)
            elif isinstance(data, str):
                for field, patterns in insecure_patterns.items():
                    if field in prefix.lower():
                        for pattern in patterns:
                            if pattern.lower() in data.lower():
                                findings.append(
                                    {
                                        "type": "insecure_default",
                                        "severity": "HIGH",
                                        "field": prefix,
                                        "value": data,
                                        "description": f"Default {field} value found: {pattern}",
                                        "location": str(path),
                                    }
                                )
                                break

        check_dict(config)

        return findings

    def _check_exposed_secrets(
        self, config: Dict[str, Any], path: Path
    ) -> List[Dict[str, Any]]:
        """Check for exposed secrets"""
        findings = []

        secret_patterns = [
            r"[A-Z0-9]{32}",  # Potential API key
            r"sk-[a-zA-Z0-9]{32}",  # Stripe key
            r"AIza[a-zA-Z0-9_-]{35}",  # Google API key
            r"AKIA[0-9A-Z]{16}",  # AWS access key
        ]

        import re

        def check_dict(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    check_dict(value, new_prefix)
            elif isinstance(data, str):
                for pattern in secret_patterns:
                    if re.search(pattern, data):
                        findings.append(
                            {
                                "type": "exposed_secret",
                                "severity": "CRITICAL",
                                "field": prefix,
                                "description": f"Potential secret exposed: {prefix}",
                                "location": str(path),
                            }
                        )
                        break

        check_dict(config)

        return findings

    def _check_weak_encryption(
        self, config: Dict[str, Any], path: Path
    ) -> List[Dict[str, Any]]:
        """Check for weak encryption settings"""
        findings = []

        def check_dict(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_prefix = f"{prefix}.{key}" if prefix else key

                    # Check for weak algorithms
                    if "algorithm" in key.lower() or "cipher" in key.lower():
                        if isinstance(value, str):
                            weak_algos = ["DES", "RC4", "MD5", "SHA1"]
                            for weak_algo in weak_algos:
                                if weak_algo.lower() in value.lower():
                                    findings.append(
                                        {
                                            "type": "weak_encryption",
                                            "severity": "HIGH",
                                            "field": prefix,
                                            "value": value,
                                            "description": f"Weak encryption algorithm: {weak_algo}",
                                            "location": str(path),
                                        }
                                    )
                                    break

                    check_dict(value, new_prefix)

        check_dict(config)

        return findings

    def _check_insecure_permissions(self, path: Path) -> List[Dict[str, Any]]:
        """Check for insecure file permissions"""
        findings = []

        try:
            stat_info = path.stat()
            mode = stat_info.st_mode

            # Check if file is world-readable or world-writable
            is_world_readable = bool(mode & 0o004)
            is_world_writable = bool(mode & 0o002)

            if is_world_writable:
                findings.append(
                    {
                        "type": "insecure_permissions",
                        "severity": "HIGH",
                        "field": "file_permissions",
                        "value": oct(mode),
                        "description": "File is world-writable",
                        "location": str(path),
                    }
                )

            if is_world_readable:
                findings.append(
                    {
                        "type": "insecure_permissions",
                        "severity": "MEDIUM",
                        "field": "file_permissions",
                        "value": oct(mode),
                        "description": "File is world-readable",
                        "location": str(path),
                    }
                )

        except Exception as e:
            logger.error(f"Error checking permissions: {e}")

        return findings

    def _count_by_severity(self, findings: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count findings by severity"""
        count = {}

        for finding in findings:
            severity = finding.get("severity", "LOW")
            count[severity] = count.get(severity, 0) + 1

        return count
