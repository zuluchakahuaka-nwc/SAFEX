"""
Report Formatters Module
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import json
from datetime import datetime


class BaseFormatter(ABC):
    """Base class for report formatters"""

    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """Format data into string"""
        pass


class JSONFormatter(BaseFormatter):
    """JSON formatter"""

    def format(self, data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        return json.dumps(data, indent=2, ensure_ascii=False)


class TextFormatter(BaseFormatter):
    """Plain text formatter"""

    def format(self, data: Dict[str, Any]) -> str:
        """Format data as plain text"""
        lines = []
        self._format_dict(data, lines, 0)
        return "\n".join(lines)

    def _format_dict(self, data: Any, lines: list, indent: int):
        """Recursively format dictionary"""
        prefix = "  " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    self._format_dict(value, lines, indent + 1)
                else:
                    lines.append(f"{prefix}{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                self._format_dict(item, lines, indent)
        else:
            lines.append(f"{prefix}{data}")


class HTMLFormatter(BaseFormatter):
    """HTML formatter"""

    def format(self, data: Dict[str, Any]) -> str:
        """Format data as HTML"""
        html = self._generate_html(data)
        return html

    def _generate_html(self, data: Any) -> str:
        """Generate HTML from data"""
        if isinstance(data, dict):
            return self._dict_to_html(data)
        elif isinstance(data, list):
            return self._list_to_html(data)
        else:
            return str(data)

    def _dict_to_html(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to HTML"""
        html = '<table class="data-table">\n'

        for key, value in data.items():
            html += "  <tr>\n"
            html += f'    <td class="key">{self._escape_html(key)}</td>\n'

            if isinstance(value, (dict, list)):
                html += '    <td class="value">\n'
                html += self._generate_html(value)
                html += "    </td>\n"
            else:
                html += f'    <td class="value">{self._escape_html(str(value))}</td>\n'

            html += "  </tr>\n"

        html += "</table>\n"
        return html

    def _list_to_html(self, data: list) -> str:
        """Convert list to HTML"""
        html = '<ul class="data-list">\n'

        for item in data:
            html += "  <li>\n"
            html += self._generate_html(item)
            html += "  </li>\n"

        html += "</ul>\n"
        return html

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )


class MarkdownFormatter(BaseFormatter):
    """Markdown formatter"""

    def format(self, data: Dict[str, Any]) -> str:
        """Format data as Markdown"""
        lines = []
        self._format_dict(data, lines, 0)
        return "\n".join(lines)

    def _format_dict(self, data: Any, lines: list, level: int):
        """Recursively format dictionary to Markdown"""
        prefix = "#" * (level + 1)

        if isinstance(data, dict):
            for key, value in data.items():
                if level == 0:
                    lines.append(f"{prefix} {key}")
                else:
                    lines.append(f"**{key}**:")

                if isinstance(value, (dict, list)):
                    self._format_dict(value, lines, level + 1)
                    lines.append("")
                else:
                    lines.append(f"{value}\n")
        elif isinstance(data, list):
            for item in data:
                lines.append(f"- {item}")
        else:
            lines.append(f"{data}")
