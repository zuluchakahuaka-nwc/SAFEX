"""
Tool Factory Module
"""

from typing import Dict, Type
from .base_tool import BaseTool


class ToolFactory:
    """Factory for creating tools"""

    _tools: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def create_tool(cls, tool_type: str) -> BaseTool:
        """
        Create a tool instance

        Args:
            tool_type: Type of tool

        Returns:
            Tool instance

        Raises:
            ValueError: If tool type is not found
        """
        if tool_type not in cls._tools:
            available = ", ".join(cls._tools.keys())
            raise ValueError(f"Unknown tool type: {tool_type}. Available: {available}")

        tool_class = cls._tools[tool_type]
        return tool_class()

    @classmethod
    def get_available_tools(cls) -> list:
        """Get list of available tool types"""
        return list(cls._tools.keys())

    @classmethod
    def register_tool(cls, tool_type: str, tool_class: Type[BaseTool]):
        """
        Register a custom tool

        Args:
            tool_type: Tool type identifier
            tool_class: Tool class
        """
        cls._tools[tool_type] = tool_class
