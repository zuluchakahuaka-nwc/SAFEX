"""
Code Scanner Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import re
from .base_scanner import BaseScanner
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CodeScanner(BaseScanner):
    """Scanner for source code files"""

    def __init__(self, config: Optional[Settings] = None):
        super().__init__(config)
        self.supported_languages = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".cs": "csharp",
            ".go": "go",
            ".rb": "ruby",
            ".php": "php",
            ".rs": "rust",
        }

    def get_name(self) -> str:
        return "Source Code Scanner"

    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan source code file for security issues

        Args:
            target: Path to source file
            options: Scan options

        Returns:
            Scan results
        """
        logger.info(f"Scanning code file: {target}")

        path = Path(target)

        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {target}",
                "findings": [],
            }

        if path.suffix.lower() not in self.supported_languages:
            return {
                "success": False,
                "error": f"Unsupported language: {path.suffix}",
                "findings": [],
            }

        # Load code
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            code_content = f.read()

        language = self.supported_languages[path.suffix.lower()]
        findings = []

        # Scan for issues
        findings.extend(self._check_hardcoded_secrets(code_content, path))
        findings.extend(self._check_sql_injection(code_content, path, language))
        findings.extend(self._check_xss(code_content, path, language))
        findings.extend(
            self._check_insecure_deserialization(code_content, path, language)
        )
        findings.extend(self._check_weak_crypto(code_content, path, language))
        findings.extend(self._check_command_injection(code_content, path, language))

        result = {
            "success": True,
            "target": target,
            "language": language,
            "scanner": self.get_name(),
            "findings": findings,
            "total_findings": len(findings),
            "severity_count": self._count_by_severity(findings),
        }

        self.scan_results.append(result)

        return result

    def _check_hardcoded_secrets(self, code: str, path: Path) -> List[Dict[str, Any]]:
        """Check for hardcoded secrets"""
        findings = []

        # Common patterns for secrets
        patterns = {
            r'password\s*=\s*["\'][^"\']+["\']': "Hardcoded password",
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']': "Hardcoded API key",
            r'secret[_-]?key\s*=\s*["\'][^"\']+["\']': "Hardcoded secret key",
            r'token\s*=\s*["\'][^"\']+["\']': "Hardcoded token",
            r'private[_-]?key\s*=\s*["\'][^"\']+["\']': "Hardcoded private key",
        }

        for pattern, description in patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE)

            for match in matches:
                line_num = code[: match.start()].count("\n") + 1
                findings.append(
                    {
                        "type": "hardcoded_secret",
                        "severity": "CRITICAL",
                        "line": line_num,
                        "description": description,
                        "code_snippet": match.group(0),
                        "location": f"{path}:{line_num}",
                    }
                )

        return findings

    def _check_sql_injection(
        self, code: str, path: Path, language: str
    ) -> List[Dict[str, Any]]:
        """Check for SQL injection vulnerabilities"""
        findings = []

        # Patterns for potential SQL injection
        if language in ["python", "java", "php"]:
            # Pattern: string concatenation in SQL queries
            patterns = [
                r"(SELECT|INSERT|UPDATE|DELETE).*\+\s*[a-zA-Z_][a-zA-Z0-9_]*",
                r"(SELECT|INSERT|UPDATE|DELETE).*%s.*%.*format",
                r"(SELECT|INSERT|UPDATE|DELETE).*\{.*\}.*format",
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)

                for match in matches:
                    line_num = code[: match.start()].count("\n") + 1
                    findings.append(
                        {
                            "type": "sql_injection",
                            "severity": "HIGH",
                            "line": line_num,
                            "description": "Potential SQL injection via string concatenation",
                            "code_snippet": match.group(0),
                            "location": f"{path}:{line_num}",
                        }
                    )

        return findings

    def _check_xss(self, code: str, path: Path, language: str) -> List[Dict[str, Any]]:
        """Check for XSS vulnerabilities"""
        findings = []

        if language in ["javascript", "typescript", "php"]:
            # Pattern: direct insertion of user input into HTML/JavaScript
            patterns = [
                r"innerHTML\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*",
                r"document\.write\s*\([a-zA-Z_][a-zA-Z0-9_]*",
                r"eval\s*\([a-zA-Z_][a-zA-Z0-9_]*",
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)

                for match in matches:
                    line_num = code[: match.start()].count("\n") + 1
                    findings.append(
                        {
                            "type": "xss",
                            "severity": "HIGH",
                            "line": line_num,
                            "description": "Potential XSS vulnerability",
                            "code_snippet": match.group(0),
                            "location": f"{path}:{line_num}",
                        }
                    )

        return findings

    def _check_insecure_deserialization(
        self, code: str, path: Path, language: str
    ) -> List[Dict[str, Any]]:
        """Check for insecure deserialization"""
        findings = []

        if language == "python":
            # Pattern: unsafe pickle usage
            patterns = [
                r"pickle\.loads\s*\(",
                r"pickle\.load\s*\([^,)]*\)",
                r"yaml\.load\s*\([^,)]*\)",  # Should use yaml.safe_load
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)

                for match in matches:
                    line_num = code[: match.start()].count("\n") + 1
                    findings.append(
                        {
                            "type": "insecure_deserialization",
                            "severity": "HIGH",
                            "line": line_num,
                            "description": "Insecure deserialization detected",
                            "code_snippet": match.group(0),
                            "location": f"{path}:{line_num}",
                        }
                    )

        return findings

    def _check_weak_crypto(
        self, code: str, path: Path, language: str
    ) -> List[Dict[str, Any]]:
        """Check for weak cryptography"""
        findings = []

        # Weak algorithms
        weak_algos = ["DES", "RC4", "MD5", "SHA1", "SHA-1"]

        for algo in weak_algos:
            pattern = rf"{re.escape(algo)}\s*\("
            matches = re.finditer(pattern, code)

            for match in matches:
                line_num = code[: match.start()].count("\n") + 1
                findings.append(
                    {
                        "type": "weak_crypto",
                        "severity": "HIGH",
                        "line": line_num,
                        "description": f"Weak cryptographic algorithm: {algo}",
                        "code_snippet": match.group(0),
                        "location": f"{path}:{line_num}",
                    }
                )

        return findings

    def _check_command_injection(
        self, code: str, path: Path, language: str
    ) -> List[Dict[str, Any]]:
        """Check for command injection vulnerabilities"""
        findings = []

        if language == "python":
            # Pattern: unsafe subprocess/os calls with user input
            patterns = [
                r"os\.system\s*\([^)]*[a-zA-Z_][a-zA-Z0-9_]*[^)]*\)",
                r"subprocess\.call\s*\([^)]*[a-zA-Z_][a-zA-Z0-9_]*[^)]*shell\s*=\s*True[^)]*\)",
                r"subprocess\.Popen\s*\([^)]*[a-zA-Z_][a-zA-Z0-9_]*[^)]*shell\s*=\s*True[^)]*\)",
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)

                for match in matches:
                    line_num = code[: match.start()].count("\n") + 1
                    findings.append(
                        {
                            "type": "command_injection",
                            "severity": "CRITICAL",
                            "line": line_num,
                            "description": "Potential command injection via shell=True",
                            "code_snippet": match.group(0),
                            "location": f"{path}:{line_num}",
                        }
                    )

        return findings

    def _count_by_severity(self, findings: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count findings by severity"""
        count = {}

        for finding in findings:
            severity = finding.get("severity", "LOW")
            count[severity] = count.get(severity, 0) + 1

        return count
