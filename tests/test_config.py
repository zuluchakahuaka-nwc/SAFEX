"""
Tests for Config Module
"""

import pytest
from pathlib import Path
import tempfile
import os


def test_settings():
    """Test Settings class"""
    from src.config.settings import Settings

    settings = Settings()

    # Test default values
    assert settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]
    assert settings.output_dir is not None
    assert settings.knowledge_base_path is not None

    # Test that paths are strings
    assert isinstance(settings.output_dir, str)
    assert isinstance(settings.knowledge_base_path, str)


def test_safety_config():
    """Test loading safety config"""
    from src.config.settings import Settings

    settings = Settings()

    # Safety levels should be accessible
    assert hasattr(settings, "safety_levels")

    # Test safety levels structure
    safety_levels = settings.safety_levels
    assert "discovery" in safety_levels
    assert "safe" in safety_levels
    assert "moderate" in safety_levels
    assert "aggressive" in safety_levels


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
