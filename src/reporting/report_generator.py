"""
Report Generator Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from datetime import datetime
from .formatters import JSONFormatter, TextFormatter, HTMLFormatter
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generate security reports in various formats"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.formatters = {
            "json": JSONFormatter(),
            "text": TextFormatter(),
            "html": HTMLFormatter(),
        }

    def generate_report(
        self,
        data: Dict[str, Any],
        format: str = "json",
        output_path: Optional[str] = None,
        template: Optional[str] = None,
    ) -> str:
        """
        Generate a security report

        Args:
            data: Report data
            format: Output format (json, text, html)
            output_path: Path to save report
            template: Template name for HTML reports

        Returns:
            Path to generated report
        """
        logger.info(f"Generating report in format: {format}")

        formatter = self.formatters.get(format)

        if not formatter:
            raise ValueError(f"Unsupported format: {format}")

        # Format the data
        content = formatter.format(data)

        # Save to file
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"security_report_{timestamp}.{format}"

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Report saved to: {output_path}")
        return str(output_file)

    def generate_summary_report(
        self, scan_results: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """
        Generate a summary report from multiple scan results

        Args:
            scan_results: List of scan results
            output_path: Path to save report

        Returns:
            Path to generated report
        """
        # Calculate summary statistics
        total_findings = 0
        severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}

        for scan in scan_results:
            findings = scan.get("findings", [])
            total_findings += len(findings)

            for finding in findings:
                severity = finding.get("severity", "LOW")
                severity_count[severity] = severity_count.get(severity, 0) + 1

        # Build summary data
        summary_data = {
            "report_type": "Summary Report",
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_scans": len(scan_results),
                "total_findings": total_findings,
                "severity_distribution": severity_count,
            },
            "scans": scan_results,
        }

        return self.generate_report(summary_data, "json", output_path)

    def generate_comparison_report(
        self,
        baseline_results: List[Dict[str, Any]],
        current_results: List[Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate a comparison report between baseline and current results

        Args:
            baseline_results: Baseline scan results
            current_results: Current scan results
            output_path: Path to save report

        Returns:
            Path to generated report
        """
        # Calculate differences
        baseline_count = sum(len(scan.get("findings", [])) for scan in baseline_results)
        current_count = sum(len(scan.get("findings", [])) for scan in current_results)

        comparison_data = {
            "report_type": "Comparison Report",
            "generated_at": datetime.now().isoformat(),
            "baseline_findings": baseline_count,
            "current_findings": current_count,
            "change": current_count - baseline_count,
            "baseline": baseline_results,
            "current": current_results,
        }

        return self.generate_report(comparison_data, "json", output_path)

    def export_csv(
        self, data: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """
        Export data to CSV format

        Args:
            data: List of dictionaries
            output_path: Path to save CSV

        Returns:
            Path to generated CSV
        """
        import csv

        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"export_{timestamp}.csv"

        output_file = Path(output_path)

        if not data:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([])
            return str(output_file)

        fieldnames = list(data[0].keys())

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"CSV exported to: {output_path}")
        return str(output_file)

    def register_formatter(self, format: str, formatter):
        """
        Register a custom formatter

        Args:
            format: Format identifier
            formatter: Formatter instance
        """
        self.formatters[format] = formatter
        logger.info(f"Formatter registered: {format}")
