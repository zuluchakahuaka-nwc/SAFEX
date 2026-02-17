"""
Base Scanner Module
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BaseScanner(ABC):
    """Base class for all scanners"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.scan_results = []

    @abstractmethod
    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan target for vulnerabilities

        Args:
            target: Path or identifier to scan
            options: Scan options

        Returns:
            Scan results
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get scanner name"""
        pass

    def validate_target(self, target: str) -> bool:
        """Validate if target can be scanned"""
        path = Path(target)
        return path.exists()

    def get_scan_history(self) -> List[Dict[str, Any]]:
        """Get scan history"""
        return self.scan_results

    def clear_history(self):
        """Clear scan history"""
        self.scan_results = []
