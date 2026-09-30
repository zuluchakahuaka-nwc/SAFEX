"""
Tests for Safety Module
"""

import pytest


def test_safety_manager():
    """Test SafetyManager"""
    from src.safety.safety_manager import SafetyManager

    sm = SafetyManager()

    # Test get_safety_level
    level = sm.get_safety_level("safe")
    assert level is not None
    assert level.name == "safe"

    # Test invalid safety level
    try:
        sm.get_safety_level("invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test assess_fix_risk
    risk = sm.assess_fix_risk("VULN-001", "/test/path", "CRITICAL")
    assert risk is not None
    assert "level" in risk

    # Test get_warning_emoji
    emoji = sm.get_warning_emoji("LOW")
    assert emoji == "[+] "

    emoji = sm.get_warning_emoji("CRITICAL")
    assert emoji == "[!!] "


def test_safety_levels():
    """Test SafetyLevel enum"""
    from src.safety.safety_manager import SafetyLevel

    # Test all safety levels
    assert SafetyLevel.DISCOVERY.name == "discovery"
    assert SafetyLevel.SAFE.name == "safe"
    assert SafetyLevel.MODERATE.name == "moderate"
    assert SafetyLevel.AGGRESSIVE.name == "aggressive"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
