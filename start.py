# SAFEX Startup Script
# Starts all services (API, Celery workers, etc.)

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ..utils.logger import get_logger
from ..utils.config import settings

logger = get_logger("startup")


def check_dependencies():
    """Check if all dependencies are installed"""
    logger.info("Checking dependencies...")

    dependencies = [
        ("python", "python3", "--version"),
        ("git", "--version"),
        ("docker", "--version"),
        ("docker-compose", "--version"),
    ]

    missing = []

    for name, command, flag in dependencies:
        try:
            result = subprocess.run(
                [name, flag],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                version_info = result.stdout.strip()
                logger.info(f"✓ {name}: {version_info}")
            else:
                logger.warning(f"{name} version check returned {result.returncode}")
        except FileNotFoundError:
            missing.append(name)
            logger.warning(f"✗ {name}: not found")
        except subprocess.TimeoutExpired:
            missing.append(name)
            logger.error(f"✗ {name}: version check timed out")
        except Exception as e:
            logger.error(f"✗ {name}: {e}")
            missing.append(name)

    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        return False

    return True


def setup_environment():
    """Setup environment variables"""
    logger.info("Setting up environment...")

    env_file = project_root / ".env"

    if not env_file.exists():
        env_example = project_root / ".env.example"

        if env_example.exists():
            import shutil

            shutil.copy(env_example, env_file)
            logger.info("Created .env file from .env.example")
            logger.warning("Please configure .env file with your configuration")
        else:
            logger.error(".env.example not found")
            return False
    else:
        logger.info("✓ .env file exists")

    return True


def create_directories():
    """Create necessary directories"""
    logger.info("Creating directories...")

    directories = [
        "data",
        "data/backups",
        "data/temp",
        "data/wordlists",
        "data/exploits",
        "reports",
        "logs",
    ]

    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"✓ {directory}")

    return True


def start_services():
    """Start all services"""
    logger.info("Starting services...")

    # Check if using Docker
    use_docker = os.getenv("USE_DOCKER", "true").lower() == "true"

    if use_docker:
        logger.info("Starting services with Docker Compose...")

        try:
            subprocess.run(
                ["docker-compose", "up", "-d"],
                cwd=project_root,
                check=True,
                timeout=300,
            )
            logger.info("✓ Services started with Docker Compose")
            return True
        else:
        logger.info("Starting services locally...")

        # Start API server
        try:
            api_process = subprocess.Popen(
                ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd=project_root,
            stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            logger.info("✓ API server started")
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            return False

        # Start Celery worker
        try:
            worker_process = subprocess.Popen(
                ["celery", "-A", "src.queue.celery_app", "worker", "--loglevel=info", "--concurrency=2"],
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            logger.info("✓ Celery worker started")
        except Exception as e:
            logger.error(f"Failed to start Celery worker: {e}")
            return False

        # Start Celery beat
        try:
            beat_process = subprocess.Popen(
                ["celery", "-A", "src.queue.celery_app", "beat", "--loglevel=info"],
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            logger.info("✓ Celery beat started")
        except Exception as e:
            logger.error(f"Failed to start Celery beat: {e}")
            return False

        return True


def main():
    """Main startup function"""
    logger.info("=" * 60)
    logger.info("SAFEX - Security Framework for Testing and Execution")
    logger.info("=" * 60)
    logger.info("")

    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Please install missing dependencies.")
        sys.exit(1)

    # Setup environment
    if not setup_environment():
        logger.error("Environment setup failed.")
        sys.exit(1)

    # Create directories
    if not create_directories():
        logger.error("Directory creation failed.")
        sys.exit(1)

    # Start services
    if not start_services():
        logger.error("Failed to start services.")
        sys.exit(1)

    # Success message
    logger.info("")
    logger.info("=" * 60)
    logger.info("SAFEX is now running!")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Access points:")
    logger.info("  - API: http://localhost:8000")
    logger.info("  - API Docs: http://localhost:8000/docs")
    logger.info("  - Web Console: http://localhost:8000")
    logger.info("  - Redis UI: http://localhost:8081")
    logger.info("  - PgAdmin: http://localhost:5050")
    logger.info("")
    logger.info("CLI usage:")
    logger.info("  - Activate environment: source venv/bin/activate")
    logger.info("  - Run CLI: safex --help")
    logger.info("  - Validate: safex validate --domain example.com --target-email admin@example.com")
    logger.info("  - Start scan: safex scan --target 1.2.3.4 --token <token>")
    logger.info("  - Generate report: safex report --scan-id <uuid> --format json,html,pdf")
    logger.info("")
    logger.info("For deployment:")
    logger.info("  - Local: docker-compose up -d")
    logger.info("  - Cloud: docker-compose -f docker-compose.yml up -d")
    logger.info("")

    logger.info("")


if __name__ == "__main__":
    main()
