"""
Tool Manager Module
"""

from typing import Dict, List, Optional, Any
from .base_tool import BaseTool
from .tool_factory import ToolFactory
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ToolManager:
    """Manager for security tools"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.available_tools = self._discover_tools()
        self.tool_instances = {}

    def _discover_tools(self) -> Dict[str, Dict[str, Any]]:
        """Discover available tools"""
        tools = {}

        # Built-in tools
        built_in_tools = [
            {
                "type": "port_scanner",
                "name": "Port Scanner",
                "description": "Scan ports for open services",
            },
            {
                "type": "vulnerability_scanner",
                "name": "Vulnerability Scanner",
                "description": "Scan for known vulnerabilities",
            },
            {
                "type": "dependency_checker",
                "name": "Dependency Checker",
                "description": "Check dependencies for vulnerabilities",
            },
            {
                "type": "config_auditor",
                "name": "Configuration Auditor",
                "description": "Audit configuration files",
            },
        ]

        for tool in built_in_tools:
            tools[tool["type"]] = tool

        return tools

    def get_tool(self, tool_type: str) -> Optional[BaseTool]:
        """
        Get a tool instance

        Args:
            tool_type: Type of tool

        Returns:
            Tool instance or None
        """
        if tool_type not in self.available_tools:
            logger.error(f"Tool not found: {tool_type}")
            return None

        # Return cached instance if available
        if tool_type in self.tool_instances:
            return self.tool_instances[tool_type]

        # Create new instance
        try:
            tool = ToolFactory.create_tool(tool_type)
            self.tool_instances[tool_type] = tool
            return tool
        except Exception as e:
            logger.error(f"Error creating tool {tool_type}: {e}")
            return None

    def execute_tool(self, tool_type: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool

        Args:
            tool_type: Type of tool
            **kwargs: Tool parameters

        Returns:
            Execution result
        """
        tool = self.get_tool(tool_type)

        if not tool:
            return {"success": False, "error": f"Tool not available: {tool_type}"}

        if not tool.is_available():
            return {
                "success": False,
                "error": f"Tool not available for execution: {tool_type}",
            }

        try:
            logger.info(f"Executing tool: {tool_type}")
            result = tool.execute(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_type}: {e}")
            return {"success": False, "error": str(e)}

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [
            {"type": tool_type, **tool_info}
            for tool_type, tool_info in self.available_tools.items()
        ]

    def get_tool_info(self, tool_type: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        return self.available_tools.get(tool_type)

    def refresh_tools(self):
        """Refresh available tools"""
        self.available_tools = self._discover_tools()
        logger.info("Tools refreshed")
