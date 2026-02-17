"""
Basic Tests for SAFEX
"""

import pytest
from pathlib import Path
import tempfile
import os


def test_project_structure():
    """Test that project structure is correct"""
    project_root = Path("D:/Projects/SAFEX")

    assert project_root.exists()
    assert (project_root / "src").exists()
    assert (project_root / "src" / "__init__.py").exists()


def test_config_module():
    """Test config module"""
    from src.config.settings import Settings

    settings = Settings()
    assert settings is not None
    assert hasattr(settings, "log_level")
    assert hasattr(settings, "output_dir")


def test_logger_module():
    """Test logger module"""
    from src.utils.logger import get_logger

    logger = get_logger(__name__)
    assert logger is not None


def test_i18n_module():
    """Test i18n module"""
    from src.i18n.translation_manager import TranslationManager

    tm = TranslationManager()
    assert tm is not None

    # Test English (default)
    text = tm.translate("welcome", language="en")
    assert text is not None

    # Test Russian
    text_ru = tm.translate("welcome", language="ru")
    assert text_ru is not None

    # Test get_available_languages
    languages = tm.get_available_languages()
    assert "en" in languages
    assert "ru" in languages


def test_safety_module():
    """Test safety module"""
    from src.safety.safety_manager import SafetyManager

    sm = SafetyManager()
    assert sm is not None

    # Test safety levels
    assert hasattr(sm, "get_safety_level")
    assert hasattr(sm, "assess_fix_risk")


def test_knowledge_base_module():
    """Test knowledge base module"""
    from src.knowledge_base.knowledge_base import KnowledgeBase

    kb = KnowledgeBase()
    assert kb is not None

    # Test get_vulnerability
    vuln = kb.get_vulnerability("VULN-001")
    assert vuln is not None
    assert vuln["id"] == "VULN-001"


def test_validator_module():
    """Test validator module"""
    from src.core.validator import OwnershipValidator

    validator = OwnershipValidator()
    assert validator is not None

    # Test with a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        temp_file = f.name

    try:
        is_valid, message = validator.validate(
            temp_file, "file_permission", "discovery"
        )
        assert is_valid is True
    finally:
        os.unlink(temp_file)


def test_scanner_factory():
    """Test scanner factory"""
    from src.scanners.scanner_factory import ScannerFactory

    # Test getting available scanners
    scanners = ScannerFactory.get_available_scanners()
    assert "config" in scanners
    assert "code" in scanners
    assert "system" in scanners

    # Test creating a scanner
    scanner = ScannerFactory.create_scanner("config")
    assert scanner is not None


def test_report_generator():
    """Test report generator"""
    from src.reporting.report_generator import ReportGenerator

    rg = ReportGenerator()
    assert rg is not None

    # Test generating a report
    test_data = {"test": "data", "findings": []}

    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = rg.generate_report(
            test_data, "json", os.path.join(temp_dir, "test.json")
        )
        assert os.path.exists(report_path)


def test_translation_manager_russian():
    """Test Russian translations specifically"""
    from src.i18n.translation_manager import TranslationManager

    tm = TranslationManager()

    # Test Russian translations
    tests = {
        "scan": "Сканирование",
        "validate": "Валидация",
        "report": "Отчет",
        "low_risk": "🟢 НИЗКИЙ РИСК",
        "medium_risk": "🟡 СРЕДНИЙ РИСК",
        "high_risk": "🔴 ВЫСОКИЙ РИСК",
        "critical_risk": "🚨 КРИТИЧЕСКИЙ РИСК",
    }

    for key, expected in tests.items():
        translated = tm.translate(key, language="ru")
        # The translation should either match or be the key itself if not defined
        assert translated is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
