"""
Tests for Core Modules
"""

import pytest
from pathlib import Path
import tempfile
import os


def test_ownership_validator():
    """Test OwnershipValidator"""
    from src.core.validator import OwnershipValidator

    validator = OwnershipValidator()

    # Test with a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        temp_file = f.name

    try:
        # Test file permission validation
        is_valid, message = validator.validate(
            temp_file, "file_permission", "discovery"
        )
        assert is_valid is True
        assert "validated" in message.lower()

        # Test invalid target
        is_valid, message = validator.validate(
            "/nonexistent/path", "file_permission", "discovery"
        )
        assert is_valid is False
        assert "not found" in message.lower()

    finally:
        os.unlink(temp_file)


def test_validation_engine():
    """Test ValidationEngine"""
    from src.core.validation_engine import ValidationEngine

    engine = ValidationEngine()

    # Test with a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        temp_file = f.name

    try:
        # Test validate_target
        result = engine.validate_target(temp_file, "file_permission", "discovery")
        assert result["is_valid"] is True
        assert result["target"] == temp_file
        assert "timestamp" in result

        # Test validate_batch
        results = engine.validate_batch([temp_file], "discovery")
        assert "summary" in results
        assert "results" in results
        assert results["summary"]["total"] == 1
        assert results["summary"]["valid"] == 1

        # Test get_statistics
        stats = engine.get_statistics()
        assert stats["total_validations"] >= 1

    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
