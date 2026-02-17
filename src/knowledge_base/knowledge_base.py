"""
Knowledge Base Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import yaml
from ..config.settings import Settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class KnowledgeBase:
    """Knowledge base for vulnerability patterns, fixes, and security rules"""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()
        self.knowledge_base_path = self.config.knowledge_base_path
        self._cache = {}

        # Initialize knowledge base
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load knowledge base from files"""
        kb_path = Path(self.knowledge_base_path)

        if not kb_path.exists():
            logger.warning(f"Knowledge base path not found: {kb_path}")
            kb_path.mkdir(parents=True, exist_ok=True)

        # Load vulnerability patterns
        self.vulnerabilities = self._load_patterns("vulnerabilities.json")

        # Load security rules
        self.security_rules = self._load_patterns("security_rules.yaml")

        # Load fix recommendations
        self.fix_recommendations = self._load_patterns("fix_recommendations.json")

        logger.info(
            f"Knowledge base loaded with {len(self.vulnerabilities)} vulnerabilities"
        )

    def _load_patterns(self, filename: str) -> Dict[str, Any]:
        """Load patterns from file"""
        file_path = Path(self.knowledge_base_path) / filename

        if not file_path.exists():
            logger.warning(f"Pattern file not found: {filename}")
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if filename.endswith(".json"):
                    return json.load(f)
                elif filename.endswith(".yaml") or filename.endswith(".yml"):
                    return yaml.safe_load(f)
                else:
                    logger.warning(f"Unsupported format: {filename}")
                    return {}
        except Exception as e:
            logger.error(f"Error loading patterns from {filename}: {e}")
            return {}

    def get_vulnerability(self, vuln_id: str) -> Optional[Dict[str, Any]]:
        """Get vulnerability by ID"""
        return self.vulnerabilities.get(vuln_id)

    def search_vulnerabilities(
        self, query: str, field: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search vulnerabilities

        Args:
            query: Search query
            field: Specific field to search (name, description, severity, etc.)

        Returns:
            List of matching vulnerabilities
        """
        results = []

        for vuln_id, vuln_data in self.vulnerabilities.items():
            match = False

            if field:
                # Search in specific field
                if (
                    field in vuln_data
                    and query.lower() in str(vuln_data[field]).lower()
                ):
                    match = True
            else:
                # Search in all fields
                for value in vuln_data.values():
                    if query.lower() in str(value).lower():
                        match = True
                        break

            if match:
                results.append({"id": vuln_id, **vuln_data})

        logger.info(f"Found {len(results)} vulnerabilities matching '{query}'")
        return results

    def get_vulnerabilities_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get vulnerabilities by severity level"""
        results = []

        for vuln_id, vuln_data in self.vulnerabilities.items():
            if vuln_data.get("severity") == severity:
                results.append({"id": vuln_id, **vuln_data})

        return results

    def get_fix_recommendation(self, vuln_id: str) -> Optional[Dict[str, Any]]:
        """Get fix recommendation for vulnerability"""
        return self.fix_recommendations.get(vuln_id)

    def get_security_rules(
        self, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get security rules, optionally filtered by category"""
        rules = []

        if not self.security_rules:
            return rules

        if "rules" in self.security_rules:
            for rule in self.security_rules["rules"]:
                if category is None or rule.get("category") == category:
                    rules.append(rule)

        return rules

    def add_vulnerability(self, vuln_id: str, data: Dict[str, Any]) -> bool:
        """Add a new vulnerability to knowledge base"""
        if vuln_id in self.vulnerabilities:
            logger.warning(f"Vulnerability already exists: {vuln_id}")
            return False

        self.vulnerabilities[vuln_id] = data
        self._save_patterns("vulnerabilities.json", self.vulnerabilities)
        return True

    def add_fix_recommendation(self, vuln_id: str, data: Dict[str, Any]) -> bool:
        """Add fix recommendation for vulnerability"""
        self.fix_recommendations[vuln_id] = data
        self._save_patterns("fix_recommendations.json", self.fix_recommendations)
        return True

    def add_security_rule(self, rule: Dict[str, Any]) -> bool:
        """Add a new security rule"""
        if "rules" not in self.security_rules:
            self.security_rules["rules"] = []

        self.security_rules["rules"].append(rule)
        self._save_patterns("security_rules.yaml", self.security_rules)
        return True

    def _save_patterns(self, filename: str, data: Dict[str, Any]):
        """Save patterns to file"""
        file_path = Path(self.knowledge_base_path) / filename

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                if filename.endswith(".json"):
                    json.dump(data, f, indent=2, ensure_ascii=False)
                elif filename.endswith(".yaml") or filename.endswith(".yml"):
                    yaml.safe_dump(
                        data, f, default_flow_style=False, allow_unicode=True
                    )

            logger.info(f"Patterns saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving patterns to {filename}: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        return {
            "total_vulnerabilities": len(self.vulnerabilities),
            "total_fixes": len(self.fix_recommendations),
            "total_rules": len(self.security_rules.get("rules", []))
            if self.security_rules
            else 0,
            "severity_distribution": self._get_severity_distribution(),
        }

    def _get_severity_distribution(self) -> Dict[str, int]:
        """Get vulnerability distribution by severity"""
        distribution = {}

        for vuln_data in self.vulnerabilities.values():
            severity = vuln_data.get("severity", "unknown")
            distribution[severity] = distribution.get(severity, 0) + 1

        return distribution

    def update_from_remote(self, url: str) -> bool:
        """Update knowledge base from remote source"""
        try:
            import requests

            logger.info(f"Updating knowledge base from: {url}")
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                data = response.json()

                # Update vulnerabilities
                if "vulnerabilities" in data:
                    self.vulnerabilities.update(data["vulnerabilities"])
                    self._save_patterns("vulnerabilities.json", self.vulnerabilities)

                # Update fixes
                if "fix_recommendations" in data:
                    self.fix_recommendations.update(data["fix_recommendations"])
                    self._save_patterns(
                        "fix_recommendations.json", self.fix_recommendations
                    )

                # Update rules
                if "security_rules" in data:
                    self.security_rules = data["security_rules"]
                    self._save_patterns("security_rules.yaml", self.security_rules)

                logger.info("Knowledge base updated successfully")
                return True
            else:
                logger.error(
                    f"Failed to update knowledge base: HTTP {response.status_code}"
                )
                return False

        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
            return False

    def validate_patterns(self) -> Dict[str, List[str]]:
        """Validate knowledge base patterns and return errors"""
        errors = {"vulnerabilities": [], "fixes": [], "rules": []}

        # Validate vulnerabilities
        for vuln_id, vuln_data in self.vulnerabilities.items():
            if "severity" not in vuln_data:
                errors["vulnerabilities"].append(f"{vuln_id}: Missing severity field")

            if "description" not in vuln_data:
                errors["vulnerabilities"].append(
                    f"{vuln_id}: Missing description field"
                )

        # Validate fixes
        for vuln_id, fix_data in self.fix_recommendations.items():
            if vuln_id not in self.vulnerabilities:
                errors["fixes"].append(f"{vuln_id}: No matching vulnerability")

            if "steps" not in fix_data:
                errors["fixes"].append(f"{vuln_id}: Missing steps field")

        return errors
