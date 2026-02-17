"""
Email Handler for sending verification emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from ..utils.logger import get_logger
from ..utils.config import settings
from ..utils.exceptions import EmailError

logger = get_logger("email_handler")


class EmailHandler:
    """Handles sending emails for verification and notifications"""

    def __init__(self):
        """Initialize email handler"""
        self.smtp_host = settings.email_host
        self.smtp_port = settings.email_port
        self.smtp_user = settings.email_user
        self.smtp_password = settings.email_password
        self.from_email = settings.email_from
        self.use_tls = settings.email_use_tls

        logger.info("Email handler initialized")

    def send_verification_email(
        self, to_email: str, code: str, stage: int, target: str, target_type: str
    ) -> bool:
        """
        Send verification email to target

        Args:
            to_email: Email address to send to
            code: Verification code
            stage: Validation stage (1 or 2)
            target: Target being validated
            target_type: Type of target (domain, ip, etc.)

        Returns:
            True if email sent successfully

        Raises:
            EmailError: If email sending fails
        """
        logger.info(f"Sending verification email to: {to_email}")

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"SAFEX Ownership Verification - Stage {stage}"
            msg["From"] = self.from_email
            msg["To"] = to_email

            # Plain text version
            text_part = MIMEText(
                self._get_email_text(code, stage, target, target_type), "plain"
            )
            msg.attach(text_part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)

                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise EmailError(f"Failed to send email: {e}")

    def _get_email_text(
        self, code: str, stage: int, target: str, target_type: str
    ) -> str:
        """
        Generate email text content

        Args:
            code: Verification code
            stage: Validation stage
            target: Target being validated
            target_type: Type of target

        Returns:
            Email text content
        """
        return f"""
SAFEX Ownership Verification
{"=" * 50}

Stage {stage} Verification Code: {code}

Target: {target} ({target_type})

{"=" * 50}

You are receiving this email because you requested ownership verification for this target with SAFEX Security Framework.

If you did not request this verification, please ignore this email.

{"=" * 50}

SAFEX - Security Framework for Testing and Execution
https://github.com/zuluchakahuaka-nwc/safex
"""
