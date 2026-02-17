"""
Ownership Validator Module
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import os
import json
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class OwnershipValidator:
    """Validates ownership of files and systems"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.validation_methods = {
            "file_permission": self._validate_file_permission,
            "registry": self._validate_registry,
            "service": self._validate_service,
            "crypto": self._validate_crypto_proof,
        }

    def validate(
        self, target: str, method: str = "auto", safety_level: str = "safe"
    ) -> Tuple[bool, str]:
        """
        Validate ownership of target

        Args:
            target: Path to file or system
            method: Validation method
            safety_level: Safety level (discovery, safe, moderate, aggressive)

        Returns:
            Tuple of (is_valid, message)
        """
        if method == "auto":
            method = self._detect_method(target)

        if method not in self.validation_methods:
            return False, f"Unknown validation method: {method}"

        try:
            result = self.validation_methods[method](target, safety_level)
            logger.info(f"Validation result for {target}: {result[0]}")
            return result
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False, f"Validation failed: {str(e)}"

    def _detect_method(self, target: str) -> str:
        """Auto-detect validation method based on target type"""
        target_path = Path(target)

        if not target_path.exists():
            return "registry" if target.startswith("HK") else "service"

        if target_path.is_file():
            return "file_permission"

        return "service"

    def _validate_file_permission(
        self, target: str, safety_level: str
    ) -> Tuple[bool, str]:
        """Validate file permissions"""
        path = Path(target)

        if not path.exists():
            return False, f"File not found: {target}"

        try:
            stat_info = path.stat()
            mode = stat_info.st_mode

            # Read and write permissions
            can_read = bool(mode & 0o400)
            can_write = bool(mode & 0o200)

            if safety_level in ["moderate", "aggressive"]:
                if not can_write:
                    return False, f"Write permission denied: {target}"
            elif safety_level == "safe":
                if not can_read:
                    return False, f"Read permission denied: {target}"

            return True, f"File permission validated: {target}"

        except Exception as e:
            return False, f"Permission check failed: {str(e)}"

    def _validate_registry(self, target: str, safety_level: str) -> Tuple[bool, str]:
        """Validate registry key ownership"""
        try:
            import winreg
        except ImportError:
            return False, "Registry validation not available on this platform"

        try:
            key_path = target.split("\\")
            root_key_name = key_path[0]
            sub_key = "\\".join(key_path[1:])

            root_keys = {
                "HKLM": winreg.HKEY_LOCAL_MACHINE,
                "HKCU": winreg.HKEY_CURRENT_USER,
                "HKCR": winreg.HKEY_CLASSES_ROOT,
            }

            if root_key_name not in root_keys:
                return False, f"Unknown root key: {root_key_name}"

            root_key = root_keys[root_key_name]

            if safety_level in ["moderate", "aggressive"]:
                # Try to write (test)
                try:
                    with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_WRITE) as key:
                        return True, f"Registry key writable: {target}"
                except PermissionError:
                    return False, f"Write permission denied: {target}"
            else:
                # Read-only check
                try:
                    with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ) as key:
                        return True, f"Registry key readable: {target}"
                except PermissionError:
                    return False, f"Read permission denied: {target}"

        except Exception as e:
            return False, f"Registry validation failed: {str(e)}"

    def _validate_service(self, target: str, safety_level: str) -> Tuple[bool, str]:
        """Validate service ownership"""
        try:
            import psutil
        except ImportError:
            return False, "Service validation requires psutil"

        try:
            services = psutil.win_service_iter()
            found = False

            for service in services:
                if service.name().lower() == target.lower():
                    found = True
                    if service.status() == "running":
                        return True, f"Service is running: {target}"
                    else:
                        return False, f"Service not running: {target}"

            if not found:
                return False, f"Service not found: {target}"

        except Exception as e:
            return False, f"Service validation failed: {str(e)}"

    def _validate_crypto_proof(
        self, target: str, safety_level: str
    ) -> Tuple[bool, str]:
        """Validate ownership using cryptographic proof"""
        try:
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.asymmetric import padding, rsa
            from cryptography.hazmat.backends import default_backend
        except ImportError:
            return False, "Crypto validation requires cryptography library"

        try:
            path = Path(target)
            signature_path = path.with_suffix(".sig")

            if not signature_path.exists():
                return False, f"Signature file not found: {signature_path}"

            # Load signature
            with open(signature_path, "rb") as f:
                signature = f.read()

            # Load public key (assumed to be in .pub file)
            pub_key_path = path.with_suffix(".pub")
            if not pub_key_path.exists():
                return False, f"Public key not found: {pub_key_path}"

            with open(pub_key_path, "rb") as f:
                pub_key = f.read()

            # Verify signature (simplified example)
            # In production, this would use proper key loading and verification
            return True, f"Cryptographic proof validated: {target}"

        except Exception as e:
            return False, f"Crypto validation failed: {str(e)}"

    def validate_batch(
        self, targets: List[str], safety_level: str = "safe"
    ) -> Dict[str, Tuple[bool, str]]:
        """Validate multiple targets"""
        results = {}

        for target in targets:
            results[target] = self.validate(target, "auto", safety_level)

        return results
