"""
Validation models for ownership verification
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ValidationStage(str, Enum):
    """Validation stages"""

    PENDING_STAGE_1 = "pending_stage_1"
    STAGE_1_VERIFIED = "stage_1_verified"
    PENDING_STAGE_2 = "pending_stage_2"
    VERIFIED = "verified"
    EXPIRED = "expired"


class ValidationTargetType(str, Enum):
    """Types of targets"""

    DOMAIN = "domain"
    IP_ADDRESS = "ip_address"
    WEB_SERVER = "web_server"
    SERVER = "server"
    IOT_DEVICE = "iot_device"
    OTHER = "other"


class ValidationRequest(BaseModel):
    """Request for ownership validation"""

    target: str = Field(..., description="Target to validate (domain, IP, etc.)")
    target_type: ValidationTargetType = Field(..., description="Type of target")
    target_email: EmailStr = Field(..., description="Email address at target domain")
    user_email: Optional[EmailStr] = Field(None, description="User's contact email")


class ValidationResponse(BaseModel):
    """Response for validation request"""

    validation_id: str = Field(..., description="Unique validation ID")
    target: str = Field(..., description="Target being validated")
    stage: ValidationStage = Field(..., description="Current validation stage")
    message: str = Field(..., description="Status message")
    next_action: Optional[str] = Field(None, description="Next action required")


class CodeVerification(BaseModel):
    """Code verification request"""

    validation_id: str = Field(..., description="Validation ID")
    code: str = Field(..., description="Verification code sent to email")


class PermissionToken(BaseModel):
    """Permission token for scanning"""

    token: str = Field(..., description="JWT permission token")
    expires_at: datetime = Field(..., description="Token expiration time")
    scopes: list[str] = Field(..., description="Allowed scopes/operations")


class ValidationRecord(BaseModel):
    """Complete validation record"""

    id: str
    target: str
    target_type: ValidationTargetType
    target_email: EmailStr
    user_email: Optional[EmailStr]
    stage1_code: Optional[str]
    stage2_code: Optional[str]
    stage1_verified_at: Optional[datetime]
    stage2_verified_at: Optional[datetime]
    permission_token: Optional[str]
    status: ValidationStage
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
