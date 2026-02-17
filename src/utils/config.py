"""
Configuration management for SAFEX
"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "SAFEX"
    app_version: str = "1.0.0"
    app_description: str = "Security Audit Framework for Enhanced Protection"
    debug: bool = True
    environment: str = "development"

    # Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    configs_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "configs"
    )
    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data"
    )
    reports_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "reports"
    )
    backups_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "backups"
    )
    temp_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "temp"
    )

    # Database
    database_url: str = "postgresql://safex:safex_password@localhost:5432/safex_db"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_result_backend: str = "redis://localhost:6379/1"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    celery_task_always_eager: bool = True
    celery_worker_concurrency: int = 1

    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # Email
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = "your-email@gmail.com"
    email_password: str = "your-app-password"
    email_from: str = "noreply@safex.io"
    email_use_tls: bool = True

    # Validation
    validation_cooling_period_days: int = 30
    validation_token_expire_hours: int = 24

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Scanning
    max_concurrent_scans: int = 1
    scan_timeout_minutes: int = 60
    backup_retention_days: int = 30

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "./logs/safex.log"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 10
    rate_limit_period: int = 3600
    rate_limit_requests_per_second: int = 1

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
