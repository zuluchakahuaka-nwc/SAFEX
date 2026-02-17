"""
Scanner Factory Module
"""

from typing import Dict, Type
from .base_scanner import BaseScanner
from .config_scanner import ConfigScanner
from .code_scanner import CodeScanner
from .system_scanner import SystemScanner


class ScannerFactory:
    """Factory for creating scanners"""

    _scanners: Dict[str, Type[BaseScanner]] = {
        "config": ConfigScanner,
        "code": CodeScanner,
        "system": SystemScanner,
    }

    @classmethod
    def create_scanner(cls, scanner_type: str) -> BaseScanner:
        """
        Create a scanner instance

        Args:
            scanner_type: Type of scanner (config, code, system)

        Returns:
            Scanner instance

        Raises:
            ValueError: If scanner type is not found
        """
        if scanner_type not in cls._scanners:
            available = ", ".join(cls._scanners.keys())
            raise ValueError(
                f"Unknown scanner type: {scanner_type}. Available: {available}"
            )

        scanner_class = cls._scanners[scanner_type]
        return scanner_class()

    @classmethod
    def get_available_scanners(cls) -> List[str]:
        """Get list of available scanner types"""
        return list(cls._scanners.keys())

    @classmethod
    def register_scanner(cls, scanner_type: str, scanner_class: Type[BaseScanner]):
        """
        Register a custom scanner

        Args:
            scanner_type: Scanner type identifier
            scanner_class: Scanner class
        """
        cls._scanners[scanner_type] = scanner_class
