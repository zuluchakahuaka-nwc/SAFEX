"""
Ownership Validation Module
This module handles the 2-stage email-based ownership validation system.
"""

from datetime import datetime, timedelta
from typing import Optional
import random
import string

from .models import (
    ValidationRequest,
    ValidationResponse,
    CodeVerification,
    ValidationStage,
    ValidationTargetType,
)
from ..utils.logger import get_logger
from ..utils.helpers import generate_uuid, generate_token
from ..utils.exceptions import ValidationError, EmailError

logger = get_logger("validation")


class OwnershipValidator:
    """
    Handles ownership validation using 2-stage email verification
    """

    def __init__(self):
        """Initialize the validator"""
        self.validations = {}  # In-memory storage (will be replaced with database)

    def create_validation_request(
        self, target: str, target_email: str, user_email: Optional[str] = None
    ) -> ValidationResponse:
        """
        Create a new validation request

        Args:
            target: Target domain/IP to validate
            target_email: Email address at target domain
            user_email: User's contact email (optional)

        Returns:
            ValidationResponse with validation ID and next steps

        Raises:
            ValidationError: If validation request fails
        """
        logger.info(f"Creating validation request for target: {target}")

        # Generate validation ID and codes
        validation_id = generate_uuid()
        stage1_code = self._generate_verification_code()

        # Create validation record
        validation_record = {
            "id": validation_id,
            "target": target,
            "target_type": self._determine_target_type(target),
            "target_email": target_email,
            "user_email": user_email,
            "stage1_code": stage1_code,
            "stage2_code": None,
            "stage1_verified_at": None,
            "stage2_verified_at": None,
            "permission_token": None,
            "status": ValidationStage.PENDING_STAGE_1,
            "expires_at": datetime.utcnow() + timedelta(days=30),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        # Store validation (in-memory for now)
        self.validations[validation_id] = validation_record

        # Send verification email (placeholder)
        self._send_verification_email(
            target_email=target_email, code=stage1_code, stage=1, target=target
        )

        logger.info(f"Validation request created: {validation_id}")

        return ValidationResponse(
            validation_id=validation_id,
            target=target,
            stage=ValidationStage.PENDING_STAGE_1,
            message=f"Verification code sent to {target_email}. Please verify your ownership.",
            next_action=f"Run: safex verify-code --target {target} --code {stage1_code}",
        )

    def verify_code(self, target: str, code: str) -> ValidationResponse:
        """
        Verify ownership validation code

        Args:
            target: Target domain/IP
            code: Verification code

        Returns:
            ValidationResponse with updated status

        Raises:
            ValidationError: If code is invalid or target not found
        """
        logger.info(f"Verifying code for target: {target}")

        # Find validation record by target
        validation_record = None
        for record in self.validations.values():
            if record["target"] == target:
                validation_record = record
                break

        if not validation_record:
            raise ValidationError(f"No validation request found for target: {target}")

        # Check current stage
        if validation_record["status"] == ValidationStage.PENDING_STAGE_1:
            # Verify Stage 1 code
            if validation_record["stage1_code"] == code:
                validation_record["stage1_verified_at"] = datetime.utcnow()
                validation_record["status"] = ValidationStage.STAGE_1_VERIFIED
                validation_record["updated_at"] = datetime.utcnow()

                logger.info(f"Stage 1 verified for target: {target}")

                return ValidationResponse(
                    validation_id=validation_record["id"],
                    target=target,
                    stage=ValidationStage.STAGE_1_VERIFIED,
                    message="Stage 1 verification successful. Cooling period of 30 days begins.",
                    next_action=f"Wait 30 days, then run: safex validate --target {target}",
                )
            else:
                raise ValidationError("Invalid verification code")

        elif validation_record["status"] == ValidationStage.PENDING_STAGE_2:
            # Verify Stage 2 code
            if validation_record["stage2_code"] == code:
                # Generate permission token
                permission_token = generate_token()
                validation_record["stage2_verified_at"] = datetime.utcnow()
                validation_record["permission_token"] = permission_token
                validation_record["status"] = ValidationStage.VERIFIED
                validation_record["updated_at"] = datetime.utcnow()

                logger.info(f"Stage 2 verified for target: {target}")

                return ValidationResponse(
                    validation_id=validation_record["id"],
                    target=target,
                    stage=ValidationStage.VERIFIED,
                    message="Ownership validation complete! Permission token issued.",
                    next_action=f"Token: {permission_token}\nUse this token to start scans.",
                )
            else:
                raise ValidationError("Invalid verification code")

        else:
            raise ValidationError(
                f"Invalid state for code verification: {validation_record['status']}"
            )

    def request_stage_2(self, target: str) -> ValidationResponse:
        """
        Request Stage 2 validation after cooling period

        Args:
            target: Target domain/IP

        Returns:
            ValidationResponse with stage 2 code

        Raises:
            ValidationError: If Stage 2 cannot be requested
        """
        logger.info(f"Requesting Stage 2 for target: {target}")

        # Find validation record
        validation_record = None
        for record in self.validations.values():
            if record["target"] == target:
                validation_record = record
                break

        if not validation_record:
            raise ValidationError(f"No validation request found for target: {target}")

        # Check if Stage 1 is verified
        if validation_record["status"] != ValidationStage.STAGE_1_VERIFIED:
            raise ValidationError("Stage 1 must be verified before requesting Stage 2")

        # Check cooling period
        days_since_stage1 = (
            datetime.utcnow() - validation_record["stage1_verified_at"]
        ).days
        if days_since_stage1 < 30:
            raise ValidationError(
                f"Cannot request Stage 2 yet. {30 - days_since_stage1} days remaining in cooling period."
            )

        # Generate Stage 2 code
        stage2_code = self._generate_verification_code()
        validation_record["stage2_code"] = stage2_code
        validation_record["status"] = ValidationStage.PENDING_STAGE_2
        validation_record["updated_at"] = datetime.utcnow()

        # Send verification email
        self._send_verification_email(
            target_email=validation_record["target_email"],
            code=stage2_code,
            stage=2,
            target=target,
        )

        logger.info(f"Stage 2 request created for target: {target}")

        return ValidationResponse(
            validation_id=validation_record["id"],
            target=target,
            stage=ValidationStage.PENDING_STAGE_2,
            message=f"Stage 2 code sent to {validation_record['target_email']}",
            next_action=f"Run: safex verify-code --target {target} --code {stage2_code}",
        )

    def _generate_verification_code(self, length: int = 6) -> str:
        """
        Generate a random verification code

        Args:
            length: Length of the code

        Returns:
            Random numeric code
        """
        return "".join(random.choices(string.digits, k=length))

    def _determine_target_type(self, target: str) -> ValidationTargetType:
        """
        Determine target type from target string

        Args:
            target: Target domain/IP

        Returns:
            ValidationTargetType
        """
        from ..utils.helpers import validate_ip, validate_domain

        if validate_ip(target):
            return ValidationTargetType.IP_ADDRESS
        elif validate_domain(target):
            return ValidationTargetType.DOMAIN
        else:
            return ValidationTargetType.OTHER

    def _send_verification_email(
        self, target_email: str, code: str, stage: int, target: str
    ) -> None:
        """
        Send verification email to target

        Args:
            target_email: Email address to send to
            code: Verification code
            stage: Validation stage (1 or 2)
            target: Target being validated

        Raises:
            EmailError: If email sending fails
        """
        logger.info(f"Sending verification email to: {target_email}")
        logger.info(f"Stage: {stage}, Code: {code}")

        # Send email using EmailHandler
        from .email_handler import EmailHandler

        email_handler = EmailHandler()

        try:
            email_handler.send_verification_email(
                to_email=target_email,
                code=code,
                stage=stage,
                target=target,
                target_type=self._determine_target_type(target).value,
            )
            logger.info(f"Verification email sent successfully to {target_email}")
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            raise EmailError(f"Failed to send email: {e}")

    def get_validation_status(self, validation_id: str) -> dict:
        """
        Get status of a validation request

        Args:
            validation_id: Validation ID

        Returns:
            Validation record dictionary

        Raises:
            ValidationError: If validation not found
        """
        if validation_id not in self.validations:
            raise ValidationError(f"Validation not found: {validation_id}")

        return self.validations[validation_id]
