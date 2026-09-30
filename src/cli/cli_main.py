"""
Main CLI for SAFEX
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import get_logger
from src.utils.config import settings
from src.core.validation_engine import ValidationEngine
from src.safety.safety_manager import SafetyManager
from src.i18n.translation_manager import TranslationManager
from src.scanners.scanner_factory import ScannerFactory
from src.reporting.report_generator import ReportGenerator

logger = get_logger("cli")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SAFEX - Security Audit Framework for Enhanced Protection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--language",
        "-l",
        choices=["en", "ru", "es", "fr", "de", "zh", "ja", "ar", "pt", "it"],
        default="en",
        help="Language for output",
    )

    parser.add_argument(
        "--safety-level",
        "-s",
        choices=["discovery", "safe", "moderate", "aggressive"],
        default="safe",
        help="Safety level for operations",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate ownership")
    validate_parser.add_argument("target", help="Target to validate")
    validate_parser.add_argument(
        "--method",
        choices=["auto", "file_permission", "registry", "service"],
        default="auto",
    )

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan target for security issues")
    scan_parser.add_argument("target", help="Target to scan")
    scan_parser.add_argument(
        "--scanner",
        choices=["config", "code", "system", "linux", "vulnerability", "network", "web", "bot"],
        default="auto",
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument(
        "--format", choices=["json", "text", "html", "markdown"], default="json"
    )
    report_parser.add_argument("--output", help="Output file path")

    # Status command
    subparsers.add_parser("status", help="Show system status")

    # List command
    list_parser = subparsers.add_parser("list", help="List items")
    list_parser.add_argument(
        "item", choices=["scanners", "tools", "languages"], help="Item to list"
    )

    # Bot security commands
    bot_scan_parser = subparsers.add_parser(
        "bot-scan", help="Scan bot project for security vulnerabilities"
    )
    bot_scan_parser.add_argument("target", help="Path to bot project directory")
    bot_scan_parser.add_argument(
        "--platform",
        choices=["telegram", "discord", "slack", "vk", "viber", "whatsapp", "generic"],
        default="telegram",
        help="Bot platform",
    )

    bot_audit_parser = subparsers.add_parser(
        "bot-audit", help="Generate security audit checklist for bot owners"
    )
    bot_audit_parser.add_argument(
        "--platform",
        choices=["telegram", "discord", "slack", "vk", "viber", "whatsapp", "generic"],
        default="telegram",
        help="Bot platform",
    )
    bot_audit_parser.add_argument(
        "--text", action="store_true", help="Output as text report"
    )
    bot_audit_parser.add_argument("--output", help="Output file path")

    bot_deploy_parser = subparsers.add_parser(
        "bot-deploy", help="Generate secure Podman deployment templates"
    )
    bot_deploy_parser.add_argument(
        "--platform",
        choices=["telegram", "discord", "slack", "vk", "viber", "whatsapp", "generic"],
        default="telegram",
        help="Bot platform",
    )
    bot_deploy_parser.add_argument(
        "--domain", default="bot.example.com", help="Webhook domain"
    )
    bot_deploy_parser.add_argument(
        "--output-dir", default="./bot-deploy", help="Output directory for templates"
    )

    args = parser.parse_args()

    # Initialize translation manager
    tm = TranslationManager()
    language = args.language

    # Set log level
    if args.verbose:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")

    # Execute command
    try:
        if args.command == "validate":
            validate_command(args, language)
        elif args.command == "scan":
            scan_command(args, language)
        elif args.command == "report":
            report_command(args, language)
        elif args.command == "status":
            status_command(args, language)
        elif args.command == "list":
            list_command(args, language)
        elif args.command == "bot-scan":
            bot_scan_command(args, language)
        elif args.command == "bot-audit":
            bot_audit_command(args, language)
        elif args.command == "bot-deploy":
            bot_deploy_command(args, language)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        logger.info(tm.translate("operation_cancelled", language=language))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def validate_command(args, language):
    """Handle validate command"""
    tm = TranslationManager()

    logger.info(tm.translate("validating_target", language=language) % args.target)

    # Show safety warning
    sm = SafetyManager()
    if args.safety_level == "aggressive":
        warning = tm.translate("aggressive_mode_warning", language=language)
        print(f"[!] {warning}")

        if not sm.confirm_fix("VALIDATION", args.target, "HIGH"):
            logger.info(tm.translate("operation_cancelled", language=language))
            return

    # Validate
    engine = ValidationEngine()
    result = engine.validate_target(args.target, args.method, args.safety_level)

    # Show result
    if result["is_valid"]:
        print(f"[OK] {tm.translate('validation_success', language=language)}")
        print(f"   {result['message']}")
    else:
        print(f"[FAIL] {tm.translate('validation_failed', language=language)}")
        print(f"   {result['message']}")


def scan_command(args, language):
    """Handle scan command"""
    tm = TranslationManager()

    logger.info(tm.translate("scanning_target", language=language) % args.target)

    # Show safety warning
    sm = SafetyManager()
    risk_level = sm.assess_fix_risk("SCAN", args.target, "MEDIUM")
    warning_emoji = sm.get_warning_emoji(risk_level["level"])

    if risk_level["level"] in ["HIGH", "CRITICAL"]:
        print(f"{warning_emoji} {risk_level['message']}")

        if args.safety_level != "discovery":
            if not sm.confirm_fix("SCAN", args.target, risk_level["level"]):
                logger.info(tm.translate("operation_cancelled", language=language))
                return

    # Scan
    if args.scanner == "auto":
        # Auto-detect scanner
        scanner = ScannerFactory.create_scanner("config")
    else:
        scanner = ScannerFactory.create_scanner(args.scanner)

    result = scanner.scan(args.target)

    # Show result
    if result["success"]:
        print(f"[OK] {tm.translate('scan_complete', language=language)}")
        print(
            f"   {tm.translate('findings', language=language)}: {result['total_findings']}"
        )

        # Show severity breakdown
        severity = result["severity_count"]
        for sev, count in severity.items():
            emoji = sm.get_warning_emoji(sev)
            print(f"   {emoji} {sev}: {count}")
    else:
        print(f"[FAIL] {tm.translate('scan_failed', language=language)}")
        print(f"   {result.get('error', 'Unknown error')}")


def report_command(args, language):
    """Handle report command"""
    tm = TranslationManager()

    logger.info(tm.translate("generating_report", language=language))

    # Generate report
    rg = ReportGenerator()

    test_data = {
        "report_type": "Security Report",
        "generated_at": datetime.utcnow().isoformat(),
        "findings": [],
    }

    report_path = rg.generate_report(test_data, args.format, args.output)

    print(f"[OK] {tm.translate('report_generated', language=language)}")
    print(f"   {report_path}")


def status_command(args, language):
    """Handle status command"""
    tm = TranslationManager()

    print(f" {tm.translate('system_status', language=language)}")
    print()
    print(f"   {tm.translate('app_name', language=language)}: {settings.app_name}")
    print(f"   {tm.translate('version', language=language)}: {settings.app_version}")
    print(
        f"   {tm.translate('environment', language=language)}: {settings.environment}"
    )
    print()
    print(f"   {tm.translate('language', language=language)}: {language}")
    print(f"   {tm.translate('safety_level', language=language)}: {args.safety_level}")


def list_command(args, language):
    """Handle list command"""
    tm = TranslationManager()

    if args.item == "scanners":
        print(f" {tm.translate('available_scanners', language=language)}:")
        for scanner in ScannerFactory.get_available_scanners():
            print(f"   - {scanner}")

    elif args.item == "tools":
        from src.tools.tool_factory import ToolFactory

        print(f" {tm.translate('available_tools', language=language)}:")
        for tool in ToolFactory.get_available_tools():
            print(f"   - {tool}")

    elif args.item == "languages":
        print(f" {tm.translate('available_languages', language=language)}:")
        tm_manager = TranslationManager()
        for lang in tm_manager.get_available_languages():
            print(f"   - {lang}")


if __name__ == "__main__":
    main()


def bot_scan_command(args, language):
    """Handle bot-scan command — scan bot project for security issues"""
    from src.bots_security.bot_scanner import BotScanner
    from src.bots_security.models import PlatformType

    platform = PlatformType(args.platform)
    logger.info(f"Scanning bot project: {args.target} (platform: {platform.value})")

    scanner = BotScanner()
    result = scanner.scan(args.target, options={"platform": platform.value})

    if result["success"]:
        passed = "PASSED" if result.get("passed", True) else "FAILED"
        print(f"{'[OK]' if result.get('passed', True) else '[FAIL]'} Bot Security Scan [{passed}]")
        print(f"   Platform: {result.get('platform', 'unknown')}")
        print(f"   Risk Score: {result.get('risk_score', 0):.1f}/100")
        print(f"   Total Findings: {result.get('total_findings', 0)}")
        severity = result.get("severity_count", {})
        for sev, count in severity.items():
            print(f"   {sev}: {count}")
        print()
        for finding in result.get("findings", []):
            print(f"   [{finding.get('risk_level', '?')}] {finding.get('title', '?')}")
            if finding.get("location"):
                print(f"      Location: {finding['location']}")
            if finding.get("recommendation"):
                print(f"      Fix: {finding['recommendation']}")
            print()
    else:
        print(f"[FAIL] Scan failed: {result.get('error', 'Unknown error')}")


def bot_audit_command(args, language):
    """Handle bot-audit command — generate security audit checklist"""
    import json
    from src.bots_security.audit_checklist import AuditChecklist
    from src.bots_security.models import PlatformType

    platform = PlatformType(args.platform)
    audit = AuditChecklist()

    if args.text:
        report = audit.generate_text_report(platform)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"[OK] Text report saved to: {args.output}")
        else:
            print(report)
    else:
        checklist = audit.generate_full_checklist(platform)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(checklist, f, indent=2, ensure_ascii=False)
            print(f"[OK] Checklist saved to: {args.output}")
        else:
            print(json.dumps(checklist, indent=2, ensure_ascii=False))


def bot_deploy_command(args, language):
    """Handle bot-deploy command — generate Podman deployment templates"""
    from src.bots_security.podman_templates import PodmanTemplates
    from src.bots_security.models import PlatformType

    platform = PlatformType(args.platform)
    templates = PodmanTemplates()
    all_templates = templates.generate_all(platform, args.domain)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for relative_path, content in all_templates.items():
        file_path = output_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"  Created: {file_path}")

    print("\n[OK] Deployment templates generated in: %s" % output_dir)
    print("   Platform: %s" % platform.value)
    print("   Next steps:")
    print("     1. cd %s" % output_dir)
    print("     2. Copy .env.example to .env and fill in real values")
    print("     3. Add TLS certificates to nginx/certs/")
    print("     4. podman-compose up -d")
