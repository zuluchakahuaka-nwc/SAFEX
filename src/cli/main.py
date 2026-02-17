"""
SAFEX CLI - Main Entry Point
"""

import click
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger
from ..utils.config import settings
from ..safety.warnings import SafetyWarnings
from ..validation.validator import OwnershipValidator

logger = get_logger("cli")


def print_safety_warnings(warnings):
    """Print safety warnings in formatted way"""
    for warning in warnings:
        print("\n" + "=" * 60)
        print(f"{warning.level.value.upper()} - {warning.title}")
        print("=" * 60)
        print(f"\nDescription: {warning.description}")
        print(f"\nImpact: {warning.impact}")
        print(f"\nMitigations:")
        for mitigation in warning.mitigations:
            print(f"  - {mitigation}")

        if warning.requires_confirmation:
            print(f"\nThis operation requires confirmation!")
            print("\nType 'confirm' to proceed or 'cancel' to abort:")

        print("=" * 60 + "\n")


@click.group()
@click.version_option(version=settings.app_version)
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--verbose", "-v", count=True, help="Increase verbosity")
def cli(debug: bool = False, verbose: int = 0):
    """
    SAFEX - Security Framework for Testing and Execution

    Automated security testing for servers, web applications, and IoT devices.
    """
    if debug:
        logger.info("Debug mode enabled")
    if verbose >= 1:
        logger.info(f"SAFEX v{settings.app_version}")


@cli.command()
@click.argument("domain")
@click.option("--target-email", required=True, help="Email address at target domain")
@click.option("--user-email", help="Your contact email")
def validate(domain: str, target_email: str, user_email: Optional[str] = None):
    """
    Start ownership validation for a target domain.

    Example: safex validate example.com --target-email admin@example.com
    """
    logger.info(f"Starting validation for domain: {domain}")
    logger.info(f"Target email: {target_email}")

    try:
        validator = OwnershipValidator()

        # Create validation request
        result = validator.create_validation_request(
            target=domain, target_email=target_email, user_email=user_email
        )

        click.echo("\n" + "=" * 60)
        click.echo("Ownership Validation")
        click.echo("=" * 60)
        click.echo(f"Validation ID: {result.validation_id}")
        click.echo(f"Target: {result.target}")
        click.echo(f"Stage: {result.stage.value}")
        click.echo(f"\nMessage: {result.message}")
        click.echo(f"\nNext Action: {result.next_action}")
        click.echo("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise click.ClickException(f"Validation failed: {e}")


@cli.command()
@click.argument("target")
@click.option("--token", required=True, help="Permission token from validation")
@click.option("--profile", default="quick_scan", help="Scan profile")
@click.option(
    "--safety-level",
    default="discovery",
    type=click.Choice(["discovery", "safe", "moderate", "aggressive"]),
    help="Safety level",
)
@click.option("--output", "-o", help="Output directory for reports")
def scan(
    target: str, token: str, profile: str, safety_level: str, output: Optional[str]
):
    """
    Start security scan on a target.

    Example: safex scan 1.2.3.4 --token <token> --profile comprehensive_web
    """
    logger.info(f"Starting scan on target: {target}")
    logger.info(f"Profile: {profile}")
    logger.info(f"Safety Level: {safety_level}")

    # Get safety warnings
    safety_warnings = SafetyWarnings.get_scan_warnings(safety_level, profile, target)

    # Display warnings
    print_safety_warnings(safety_warnings)

    # Check if high risk
    high_risk = any(w.level.value in ["high_risk", "critical"] for w in safety_warnings)

    if high_risk:
        # Require explicit confirmation
        if not SafetyWarnings.confirm_high_risk_operation():
            click.echo("\nOperation cancelled by user.")
            return

    try:
        click.echo("\n" + "=" * 60)
        click.echo("Starting Security Scan")
        click.echo("=" * 60)
        click.echo(f"Target: {target}")
        click.echo(f"Profile: {profile}")
        click.echo(f"Safety Level: {safety_level}")
        click.echo(f"Token: {token[:10]}...{token[-10:]}")
        click.echo("=" * 60 + "\n")

        # TODO: Implement actual scanning
        click.echo("Scan functionality will be implemented in Phase 2.")
        click.echo("Current status: Infrastructure setup complete.")

    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise click.ClickException(f"Scan failed: {e}")


@cli.command()
@click.argument("scan-id")
@click.option("--format", multiple=True, default=["json"], help="Report format(s)")
@click.option("--output", "-o", help="Output directory")
def report(scan_id: str, format: list, output: Optional[str]):
    """
    Generate reports from scan results.

    Example: safex report <uuid> --format json,html
    """
    logger.info(f"Generating report for scan: {scan_id}")
    logger.info(f"Formats: {format}")

    try:
        click.echo(f"\nGenerating report for scan: {scan_id}")
        click.echo(f"Formats: {', '.join(format)}")

        # TODO: Implement report generation
        click.echo("\nReport generation will be implemented in Phase 2.")

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise click.ClickException(f"Report generation failed: {e}")


@cli.command()
@click.argument("scan-id")
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
@click.option("--backup-id", help="Restore from specific backup")
def autofix(scan_id: str, interactive: bool, backup_id: Optional[str]):
    """
    Apply auto-fixes or restore from backup.

    Example: safex autofix <uuid> --interactive
    """
    logger.info(f"Auto-fix for scan: {scan_id}")
    if backup_id:
        logger.info(f"Restoring from backup: {backup_id}")

    try:
        if backup_id:
            click.echo(f"\nRestoring from backup: {backup_id}")
            # TODO: Implement restore functionality
            click.echo("Restore functionality will be implemented in Phase 3.")
        else:
            click.echo(f"\nAuto-fix for scan: {scan_id}")
            if interactive:
                click.echo("Interactive mode enabled")
            # TODO: Implement auto-fix functionality
            click.echo("Auto-fix functionality will be implemented in Phase 3.")

    except Exception as e:
        logger.error(f"Auto-fix failed: {e}")
        raise click.ClickException(f"Auto-fix failed: {e}")


@cli.command()
@click.option("--target", required=True, help="Target to verify code for")
@click.option("--code", required=True, help="Verification code")
def verify_code(target: str, code: str):
    """
    Verify ownership validation code.

    Example: safex verify-code example.com 123456
    """
    logger.info(f"Verifying code for target: {target}")

    try:
        from ..validation.validator import OwnershipValidator

        validator = OwnershipValidator()
        result = validator.verify_code(target=target, code=code)

        click.echo("\n" + "=" * 60)
        click.echo("Verification Result")
        click.echo("=" * 60)
        click.echo(f"Target: {result.target}")
        click.echo(f"Status: {result.stage.value}")
        click.echo(f"Message: {result.message}")
        click.echo("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"Code verification failed: {e}")
        raise click.ClickException(f"Code verification failed: {e}")


@cli.command()
def status():
    """
    Show SAFEX system status.

    Example: safex status
    """
    click.echo("\n" + "=" * 60)
    click.echo("SAFEX System Status")
    click.echo("=" * 60)
    click.echo(f"Version: {settings.app_version}")
    click.echo(f"Environment: {settings.environment}")
    click.echo(f"Debug: {settings.debug}")
    click.echo(f"\nDirectories:")
    click.echo(f"  Base: {settings.base_dir}")
    click.echo(f"  Configs: {settings.configs_dir}")
    click.echo(f"  Data: {settings.data_dir}")
    click.echo(f"  Reports: {settings.reports_dir}")
    click.echo(f"  Backups: {settings.backups_dir}")
    click.echo(f"\nConfiguration:")
    click.echo(f"  Max Concurrent Scans: {settings.max_concurrent_scans}")
    click.echo(f"  Scan Timeout: {settings.scan_timeout_minutes} min")
    click.echo(f"  Backup Retention: {settings.backup_retention_days} days")
    click.echo("=" * 60 + "\n")


def main():
    """Main entry point"""
    cli(obj={})


if __name__ == "__main__":
    main()
