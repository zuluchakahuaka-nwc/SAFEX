"""
Main CLI for SAFEX
"""

import sys
import argparse
from pathlib import Path

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
        choices=["config", "code", "system", "vulnerability", "network", "web"],
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
        print(f"⚠️  {warning}")

        if not sm.confirm_fix("VALIDATION", args.target, "HIGH"):
            logger.info(tm.translate("operation_cancelled", language=language))
            return

    # Validate
    engine = ValidationEngine()
    result = engine.validate_target(args.target, args.method, args.safety_level)

    # Show result
    if result["is_valid"]:
        print(f"✅ {tm.translate('validation_success', language=language)}")
        print(f"   {result['message']}")
    else:
        print(f"❌ {tm.translate('validation_failed', language=language)}")
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
        print(f"✅ {tm.translate('scan_complete', language=language)}")
        print(
            f"   {tm.translate('findings', language=language)}: {result['total_findings']}"
        )

        # Show severity breakdown
        severity = result["severity_count"]
        for sev, count in severity.items():
            emoji = sm.get_warning_emoji(sev)
            print(f"   {emoji} {sev}: {count}")
    else:
        print(f"❌ {tm.translate('scan_failed', language=language)}")
        print(f"   {result.get('error', 'Unknown error')}")


def report_command(args, language):
    """Handle report command"""
    tm = TranslationManager()

    logger.info(tm.translate("generating_report", language=language))

    # Generate report
    rg = ReportGenerator()

    test_data = {
        "report_type": "Security Report",
        "generated_at": sm._get_timestamp() if "sm" in locals() else "",
        "findings": [],
    }

    report_path = rg.generate_report(test_data, args.format, args.output)

    print(f"✅ {tm.translate('report_generated', language=language)}")
    print(f"   {report_path}")


def status_command(args, language):
    """Handle status command"""
    tm = TranslationManager()

    print(f"📊 {tm.translate('system_status', language=language)}")
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
        print(f"🔍 {tm.translate('available_scanners', language=language)}:")
        for scanner in ScannerFactory.get_available_scanners():
            print(f"   - {scanner}")

    elif args.item == "tools":
        from src.tools.tool_factory import ToolFactory

        print(f"🛠  {tm.translate('available_tools', language=language)}:")
        for tool in ToolFactory.get_available_tools():
            print(f"   - {tool}")

    elif args.item == "languages":
        print(f"🌍 {tm.translate('available_languages', language=language)}:")
        tm_manager = TranslationManager()
        for lang in tm_manager.get_available_languages():
            print(f"   - {lang}")


if __name__ == "__main__":
    main()
