"""
Logging utilities for SAFEX
Simple logging without external dependencies
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure once
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Set log level from environment or default to INFO
        log_level = logging.INFO
        logger.setLevel(log_level)

    return logger


class LoggerContext:
    """Context manager for logging with extra context"""

    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context

    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record

        logging.setLogRecordFactory(record_factory)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)
