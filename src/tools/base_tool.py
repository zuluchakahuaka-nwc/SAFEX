"""
Base Tool Module
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BaseTool(ABC):
    """Base class for all tools"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.tool_name = self.get_name()

    @abstractmethod
    def get_name(self) -> str:
        """Get tool name"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute tool

        Returns:
            Execution result
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if tool is available"""
        pass
