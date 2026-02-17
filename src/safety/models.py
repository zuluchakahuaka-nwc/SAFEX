"""
Safety models for SAFEX
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SafetyLevel(Enum):
    """Safety levels for scanning operations"""

    DISCOVERY = 1
    SAFE = 2
    MODERATE = 3
    AGGRESSIVE = 4


class SafetyConfiguration(BaseModel):
    """Safety configuration"""

    level: SafetyLevel = Field(default=SafetyLevel.SAFE)
    max_parallel_scans: int = Field(default=1)
    scan_timeout_minutes: int = Field(default=60)
    emergency_stop_enabled: bool = Field(default=True)
    rate_limit_requests_per_second: int = Field(default=10)
