"""
Safety monitor for system health during scans
"""

import time
from typing import Optional, Dict, Any

from ..utils.logger import get_logger
from ..utils.config import settings

logger = get_logger("safety.monitor")


class SafetyMonitor:
    """Monitors system health during scanning operations"""

    def __init__(self):
        """Initialize safety monitor"""
        self.check_interval = 5  # seconds
        self.max_response_time = 10.0  # seconds
        self.max_error_rate = 0.5  # 50%
        self.is_running = False
        self.current_target: Optional[str] = None

        logger.info("Safety monitor initialized")

    def start_monitoring(self, target: str):
        """
        Start monitoring a target

        Args:
            target: Target to monitor
        """
        logger.info(f"Starting safety monitoring for target: {target}")
        self.current_target = target
        self.is_running = True

    def stop_monitoring(self):
        """Stop monitoring"""
        logger.info("Stopping safety monitoring")
        self.is_running = False
        self.current_target = None

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status

        Returns:
            Dictionary with system health metrics
        """
        import psutil

        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent
            if hasattr(psutil, "disk_usage")
            else 0,
            "network_connections": len(psutil.net_connections())
            if hasattr(psutil, "net_connections")
            else 0,
        }

    def check_target_health(self, target: str) -> bool:
        """
        Check if target is healthy

        Args:
            target: Target to check

        Returns:
            True if target is healthy
        """
        try:
            # Placeholder health check
            # In production, would ping or check HTTP status
            import socket

            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((target, 80))
            return True
        except Exception as exc:
            logger.warning(f"Target health check failed for {target}: {exc}")
            return False

    def abort_if_unhealthy(self) -> bool:
        """
        Abort scan if system or target is unhealthy

        Returns:
            True if aborted
        """
        if not self.is_running or not self.current_target:
            return False

        # Check system status
        sys_status = self.get_system_status()

        # Check CPU usage
        if sys_status["cpu_percent"] > 90:
            logger.error("CPU usage too high, aborting scan")
            return True

        # Check memory usage
        if sys_status["memory_percent"] > 90:
            logger.error("Memory usage too high, aborting scan")
            return True

        # Check target health
        if not self.check_target_health(self.current_target):
            logger.error("Target is unhealthy, aborting scan")
            return True

        return False
