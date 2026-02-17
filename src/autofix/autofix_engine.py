"""
AutoFix Engine Module
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import shutil
import json
from ..config.settings import Settings
from ..utils.logger import get_logger
from ..knowledge_base.knowledge_base import KnowledgeBase
from ..safety.safety_manager import SafetyManager

logger = get_logger(__name__)


class AutoFixEngine:
    """Engine for automatically fixing security issues"""

    def __init__(
        self,
        config: Optional[Settings] = None,
        knowledge_base: Optional[KnowledgeBase] = None,
    ):
        self.config = config or Settings()
        self.knowledge_base = knowledge_base or KnowledgeBase(config)
        self.safety_manager = SafetyManager(config)

        # Track fixes
        self.fix_history = []

    def analyze_issue(self, vuln_id: str, target_path: str) -> Dict[str, Any]:
        """
        Analyze a security issue

        Args:
            vuln_id: Vulnerability ID
            target_path: Path to target file/system

        Returns:
            Analysis results
        """
        logger.info(f"Analyzing issue: {vuln_id} at {target_path}")

        vulnerability = self.knowledge_base.get_vulnerability(vuln_id)
        if not vulnerability:
            return {"error": f"Vulnerability not found: {vuln_id}", "fixable": False}

        # Get fix recommendation
        fix_rec = self.knowledge_base.get_fix_recommendation(vuln_id)

        # Assess risk
        risk_assessment = self.safety_manager.assess_fix_risk(
            vuln_id, target_path, vulnerability.get("severity", "medium")
        )

        return {
            "vulnerability": vulnerability,
            "fix_recommendation": fix_rec,
            "risk_assessment": risk_assessment,
            "fixable": fix_rec is not None,
            "target_path": target_path,
        }

    def apply_fix(
        self,
        vuln_id: str,
        target_path: str,
        safety_level: str = "safe",
        auto_confirm: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Apply fix for a vulnerability

        Args:
            vuln_id: Vulnerability ID
            target_path: Path to target file/system
            safety_level: Safety level (discovery, safe, moderate, aggressive)
            auto_confirm: Auto-apply without confirmation
            dry_run: Dry run mode (show changes without applying)

        Returns:
            Fix results
        """
        logger.info(f"Applying fix: {vuln_id} at {target_path} (dry_run={dry_run})")

        # Analyze issue
        analysis = self.analyze_issue(vuln_id, target_path)

        if not analysis["fixable"]:
            return {
                "success": False,
                "message": "Issue is not fixable",
                "analysis": analysis,
            }

        # Check safety level
        risk = analysis["risk_assessment"]
        if risk["level"] in ["HIGH", "CRITICAL"] and not auto_confirm:
            if not self.safety_manager.confirm_fix(vuln_id, target_path, risk["level"]):
                return {
                    "success": False,
                    "message": "Fix cancelled by user",
                    "analysis": analysis,
                }

        # Apply fix
        try:
            result = self._execute_fix(
                vuln_id, target_path, analysis["fix_recommendation"], dry_run
            )

            # Record fix
            fix_record = {
                "vuln_id": vuln_id,
                "target_path": target_path,
                "safety_level": safety_level,
                "success": result["success"],
                "timestamp": self._get_timestamp(),
                "dry_run": dry_run,
            }

            self.fix_history.append(fix_record)

            return {
                "success": result["success"],
                "message": result.get("message", "Fix applied"),
                "changes": result.get("changes", []),
                "analysis": analysis,
            }

        except Exception as e:
            logger.error(f"Fix application error: {e}")
            return {
                "success": False,
                "message": f"Fix failed: {str(e)}",
                "analysis": analysis,
            }

    def _execute_fix(
        self, vuln_id: str, target_path: str, fix_rec: Dict[str, Any], dry_run: bool
    ) -> Dict[str, Any]:
        """Execute fix steps"""
        changes = []

        for step in fix_rec.get("steps", []):
            step_type = step.get("type")
            step_description = step.get("description", "")

            try:
                if step_type == "file_edit":
                    if dry_run:
                        changes.append(
                            {
                                "type": "file_edit",
                                "target": target_path,
                                "description": step_description,
                                "dry_run": True,
                            }
                        )
                    else:
                        self._execute_file_edit(target_path, step)
                        changes.append(
                            {
                                "type": "file_edit",
                                "target": target_path,
                                "description": step_description,
                                "dry_run": False,
                            }
                        )

                elif step_type == "file_copy":
                    source = step.get("source")
                    dest = step.get("destination", target_path)

                    if dry_run:
                        changes.append(
                            {
                                "type": "file_copy",
                                "source": source,
                                "destination": dest,
                                "description": step_description,
                                "dry_run": True,
                            }
                        )
                    else:
                        self._execute_file_copy(source, dest)
                        changes.append(
                            {
                                "type": "file_copy",
                                "source": source,
                                "destination": dest,
                                "description": step_description,
                                "dry_run": False,
                            }
                        )

                elif step_type == "command":
                    command = step.get("command")

                    if dry_run:
                        changes.append(
                            {
                                "type": "command",
                                "command": command,
                                "description": step_description,
                                "dry_run": True,
                            }
                        )
                    else:
                        self._execute_command(command)
                        changes.append(
                            {
                                "type": "command",
                                "command": command,
                                "description": step_description,
                                "dry_run": False,
                            }
                        )

                elif step_type == "permission_change":
                    permissions = step.get("permissions")

                    if dry_run:
                        changes.append(
                            {
                                "type": "permission_change",
                                "target": target_path,
                                "permissions": permissions,
                                "description": step_description,
                                "dry_run": True,
                            }
                        )
                    else:
                        self._execute_permission_change(target_path, permissions)
                        changes.append(
                            {
                                "type": "permission_change",
                                "target": target_path,
                                "permissions": permissions,
                                "description": step_description,
                                "dry_run": False,
                            }
                        )

            except Exception as e:
                logger.error(f"Error executing step: {step_description}: {e}")
                return {
                    "success": False,
                    "message": f"Step failed: {step_description}",
                    "changes": changes,
                }

        return {"success": True, "changes": changes}

    def _execute_file_edit(self, target_path: str, step: Dict[str, Any]):
        """Execute file edit step"""
        path = Path(target_path)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Apply replacements
        for replacement in step.get("replacements", []):
            old_text = replacement.get("old")
            new_text = replacement.get("new")
            content = content.replace(old_text, new_text)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"File edited: {target_path}")

    def _execute_file_copy(self, source: str, destination: str):
        """Execute file copy step"""
        source_path = Path(source)
        dest_path = Path(destination)

        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_path, dest_path)

        logger.info(f"File copied: {source} -> {destination}")

    def _execute_command(self, command: str):
        """Execute command step"""
        import subprocess

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=300
        )

        if result.returncode != 0:
            raise Exception(f"Command failed: {result.stderr}")

        logger.info(f"Command executed: {command}")

    def _execute_permission_change(self, target_path: str, permissions: str):
        """Execute permission change step"""
        path = Path(target_path)

        # Convert octal string to int
        perm = int(permissions, 8)

        path.chmod(perm)

        logger.info(f"Permissions changed: {target_path} -> {permissions}")

    def apply_batch_fixes(
        self,
        fixes: List[Dict[str, str]],
        safety_level: str = "safe",
        auto_confirm: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Apply multiple fixes

        Args:
            fixes: List of {vuln_id, target_path}
            safety_level: Safety level
            auto_confirm: Auto-apply without confirmation
            dry_run: Dry run mode

        Returns:
            Batch fix results
        """
        logger.info(f"Applying {len(fixes)} fixes (dry_run={dry_run})")

        results = []

        for fix in fixes:
            result = self.apply_fix(
                fix["vuln_id"], fix["target_path"], safety_level, auto_confirm, dry_run
            )
            results.append(result)

        success_count = sum(1 for r in results if r["success"])

        return {
            "total": len(fixes),
            "successful": success_count,
            "failed": len(fixes) - success_count,
            "results": results,
        }

    def rollback_fix(self, fix_record: Dict[str, Any]) -> bool:
        """
        Rollback a fix

        Args:
            fix_record: Fix record from history

        Returns:
            True if successful
        """
        logger.info(f"Rolling back fix: {fix_record['vuln_id']}")

        # Check if backup exists
        backup_path = Path(f"{fix_record['target_path']}.backup")

        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_path}")
            return False

        try:
            # Restore from backup
            shutil.copy2(backup_path, fix_record["target_path"])

            # Remove backup
            backup_path.unlink()

            logger.info(f"Fix rolled back: {fix_record['vuln_id']}")
            return True

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False

    def get_fix_history(self) -> List[Dict[str, Any]]:
        """Get fix history"""
        return self.fix_history

    def clear_history(self):
        """Clear fix history"""
        self.fix_history = []
        logger.info("Fix history cleared")

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()
