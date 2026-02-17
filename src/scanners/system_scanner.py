"""
System Scanner Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import platform
import subprocess
from .base_scanner import BaseScanner
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SystemScanner(BaseScanner):
    """Scanner for system-level security checks"""

    def __init__(self, config: Optional[Settings] = None):
        super().__init__(config)
        self.system_info = self._get_system_info()

    def get_name(self) -> str:
        return "System Security Scanner"

    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan system for security issues

        Args:
            target: System identifier (can be '.' for local system)
            options: Scan options

        Returns:
            Scan results
        """
        logger.info(f"Scanning system: {target}")

        findings = []

        # Perform system checks
        findings.extend(self._check_os_updates())
        findings.extend(self._check_antivirus_status())
        findings.extend(self._check_firewall_status())
        findings.extend(self._check_user_accounts())
        findings.extend(self._check_open_ports())
        findings.extend(self._check_system_services())

        result = {
            "success": True,
            "target": target,
            "scanner": self.get_name(),
            "system_info": self.system_info,
            "findings": findings,
            "total_findings": len(findings),
            "severity_count": self._count_by_severity(findings),
        }

        self.scan_results.append(result)

        return result

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
        }

    def _check_os_updates(self) -> List[Dict[str, Any]]:
        """Check for OS updates"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Check Windows Update status (simplified)
                result = subprocess.run(
                    ["wmic", "qfe", "list", "brief"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    updates = result.stdout.count("\n") - 1

                    if updates == 0:
                        findings.append(
                            {
                                "type": "os_updates",
                                "severity": "INFO",
                                "description": "No recent Windows updates found",
                                "updates_count": updates,
                            }
                        )
                    else:
                        findings.append(
                            {
                                "type": "os_updates",
                                "severity": "LOW",
                                "description": f"{updates} recent Windows updates found",
                                "updates_count": updates,
                            }
                        )

        except Exception as e:
            logger.error(f"Error checking OS updates: {e}")

        return findings

    def _check_antivirus_status(self) -> List[Dict[str, Any]]:
        """Check antivirus status"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Check Windows Defender status
                result = subprocess.run(
                    ["sc", "query", "WinDefend"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    if "RUNNING" in result.stdout:
                        findings.append(
                            {
                                "type": "antivirus",
                                "severity": "INFO",
                                "description": "Windows Defender is running",
                            }
                        )
                    else:
                        findings.append(
                            {
                                "type": "antivirus",
                                "severity": "MEDIUM",
                                "description": "Windows Defender may not be running",
                            }
                        )
                else:
                    findings.append(
                        {
                            "type": "antivirus",
                            "severity": "HIGH",
                            "description": "Antivirus status cannot be determined",
                        }
                    )

        except Exception as e:
            logger.error(f"Error checking antivirus: {e}")

        return findings

    def _check_firewall_status(self) -> List[Dict[str, Any]]:
        """Check firewall status"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Check Windows Firewall status
                result = subprocess.run(
                    ["netsh", "advfirewall", "show", "allprofiles"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    if "State                                 ON" in result.stdout:
                        findings.append(
                            {
                                "type": "firewall",
                                "severity": "INFO",
                                "description": "Windows Firewall is enabled",
                            }
                        )
                    else:
                        findings.append(
                            {
                                "type": "firewall",
                                "severity": "HIGH",
                                "description": "Windows Firewall may be disabled",
                            }
                        )

        except Exception as e:
            logger.error(f"Error checking firewall: {e}")

        return findings

    def _check_user_accounts(self) -> List[Dict[str, Any]]:
        """Check user accounts for security issues"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Get local users
                result = subprocess.run(
                    ["net", "user"], capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    lines = result.stdout.split("\n")

                    # Look for default accounts
                    if "Administrator" in result.stdout:
                        findings.append(
                            {
                                "type": "user_accounts",
                                "severity": "MEDIUM",
                                "description": "Default Administrator account exists - consider renaming or disabling",
                            }
                        )

                    if "Guest" in result.stdout:
                        findings.append(
                            {
                                "type": "user_accounts",
                                "severity": "LOW",
                                "description": "Guest account exists - ensure it is disabled",
                            }
                        )

        except Exception as e:
            logger.error(f"Error checking user accounts: {e}")

        return findings

    def _check_open_ports(self) -> List[Dict[str, Any]]:
        """Check for open ports"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Get listening ports
                result = subprocess.run(
                    ["netstat", "-an"], capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    # Count open ports
                    open_ports = 0
                    suspicious_ports = []

                    for line in result.stdout.split("\n"):
                        if "LISTENING" in line:
                            open_ports += 1

                        # Check for suspicious ports
                        if any(port in line for port in ["135", "139", "445", "3389"]):
                            if "LISTENING" in line:
                                suspicious_ports.append(line.split(":")[1].split()[0])

                    findings.append(
                        {
                            "type": "open_ports",
                            "severity": "INFO",
                            "description": f"{open_ports} listening ports found",
                            "open_ports_count": open_ports,
                        }
                    )

                    if suspicious_ports:
                        findings.append(
                            {
                                "type": "open_ports",
                                "severity": "MEDIUM",
                                "description": f"Suspicious ports open: {', '.join(set(suspicious_ports))}",
                                "suspicious_ports": list(set(suspicious_ports)),
                            }
                        )

        except Exception as e:
            logger.error(f"Error checking open ports: {e}")

        return findings

    def _check_system_services(self) -> List[Dict[str, Any]]:
        """Check system services for security issues"""
        findings = []

        try:
            if platform.system() == "Windows":
                # Get services with non-standard configurations
                result = subprocess.run(
                    ["sc", "query", "type=", "service", "state=", "all"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode == 0:
                    services = [
                        line
                        for line in result.stdout.split("\n")
                        if "SERVICE_NAME" in line
                    ]

                    findings.append(
                        {
                            "type": "services",
                            "severity": "INFO",
                            "description": f"{len(services)} services found",
                            "service_count": len(services),
                        }
                    )

        except Exception as e:
            logger.error(f"Error checking services: {e}")

        return findings

    def _count_by_severity(self, findings: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count findings by severity"""
        count = {}

        for finding in findings:
            severity = finding.get("severity", "LOW")
            count[severity] = count.get(severity, 0) + 1

        return count
