"""
Validation Engine Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
from .validator import OwnershipValidator
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ValidationEngine:
    """Main validation engine that orchestrates validation processes"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.validator = OwnershipValidator(config)
        self.validation_history = []

    def validate_target(
        self, target: str, method: str = "auto", safety_level: str = "safe"
    ) -> Dict[str, Any]:
        """
        Validate a target and return detailed results

        Args:
            target: Path to file or system
            method: Validation method
            safety_level: Safety level

        Returns:
            Dictionary with validation results
        """
        logger.info(f"Validating target: {target} with safety level: {safety_level}")

        is_valid, message = self.validator.validate(target, method, safety_level)

        result = {
            "target": target,
            "method": method,
            "safety_level": safety_level,
            "is_valid": is_valid,
            "message": message,
            "timestamp": self._get_timestamp(),
        }

        self.validation_history.append(result)

        return result

    def validate_batch(
        self, targets: List[str], safety_level: str = "safe"
    ) -> Dict[str, Any]:
        """
        Validate multiple targets

        Args:
            targets: List of targets to validate
            safety_level: Safety level

        Returns:
            Dictionary with batch validation results
        """
        logger.info(f"Batch validation of {len(targets)} targets")

        results = {}
        for target in targets:
            results[target] = self.validator.validate(target, "auto", safety_level)

        # Calculate summary statistics
        valid_count = sum(1 for result in results.values() if result[0])
        total_count = len(results)

        summary = {
            "total": total_count,
            "valid": valid_count,
            "invalid": total_count - valid_count,
            "success_rate": valid_count / total_count if total_count > 0 else 0,
        }

        return {
            "summary": summary,
            "results": results,
            "timestamp": self._get_timestamp(),
        }

    def validate_directory(
        self,
        directory: str,
        pattern: str = "*",
        safety_level: str = "safe",
        recursive: bool = False,
    ) -> Dict[str, Any]:
        """
        Validate all files in a directory

        Args:
            directory: Directory path
            pattern: File pattern (default: *)
            safety_level: Safety level
            recursive: Recursive scan

        Returns:
            Dictionary with validation results
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            return {"error": f"Directory not found: {directory}", "results": {}}

        # Find files
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))

        file_paths = [str(f) for f in files if f.is_file()]

        logger.info(f"Validating {len(file_paths)} files in {directory}")

        return self.validate_batch(file_paths, safety_level)

    def get_validation_history(
        self, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get validation history"""
        if limit:
            return self.validation_history[-limit:]

        return self.validation_history

    def clear_history(self):
        """Clear validation history"""
        self.validation_history = []
        logger.info("Validation history cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """Get validation statistics"""
        if not self.validation_history:
            return {
                "total_validations": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "success_rate": 0.0,
            }

        total = len(self.validation_history)
        valid_count = sum(1 for v in self.validation_history if v["is_valid"])

        return {
            "total_validations": total,
            "valid_count": valid_count,
            "invalid_count": total - valid_count,
            "success_rate": valid_count / total if total > 0 else 0,
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()

    def export_results(
        self, format: str = "json", output_path: Optional[str] = None
    ) -> str:
        """
        Export validation results

        Args:
            format: Export format (json, csv)
            output_path: Output file path

        Returns:
            Path to exported file
        """
        import json
        from datetime import datetime

        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"validation_results_{timestamp}.{format}"

        if format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.validation_history, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            import csv

            if not self.validation_history:
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([])
            else:
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=self.validation_history[0].keys()
                    )
                    writer.writeheader()
                    writer.writerows(self.validation_history)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Results exported to: {output_path}")
        return output_path
