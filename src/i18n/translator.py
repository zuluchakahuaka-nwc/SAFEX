"""
Internationalization (i18n) for SAFEX
Supports multiple languages for CLI, Web, and TUI interfaces
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class Language(Enum):
    """Supported languages"""

    ENGLISH = "en"
    RUSSIAN = "ru"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    ARABIC = "ar"
    PORTUGUESE = "pt"
    ITALIAN = "it"


class TranslationManager:
    """Manages translations for all interfaces"""

    def __init__(self, language: Language = Language.ENGLISH):
        """Initialize translation manager

        Args:
            language: Default language
        """
        self.language = language
        self.translations_dir = Path(__file__).parent / "i18n_data"
        self.translations_dir.mkdir(parents=True, exist_ok=True)

        self._initialize_translations()
        self._load_translations()

    def _initialize_translations(self):
        """Initialize translation files"""
        # This would be called during build/first run
        pass

    def _load_translations(self):
        """Load translations from file"""
        # Get all translations
        self.all_translations = self._get_all_translations()

        # Load current language
        self.current_translations = self.all_translations.get(
            self.language.value, self.all_translations["en"]
        )

    def _get_all_translations(self) -> Dict[str, Dict[str, str]]:
        """Get all translations"""
        return {
            "en": {
                # App info
                "app_name": "SAFEX",
                "app_version": "1.0.0",
                "app_description": "Security Framework for Testing and Execution",
                # CLI
                "cli_header": "SAFEX - Security Framework for Testing and Execution",
                "cli_version": "Version",
                "cli_help": "Show this help message",
                "cli_debug": "Enable debug mode",
                "cli_verbose": "Increase verbosity",
                # Commands
                "cmd_validate": "Validate ownership of target",
                "cmd_scan": "Start security scan",
                "cmd_report": "Generate reports",
                "cmd_autofix": "Apply auto-fixes",
                "cmd_tui": "Launch TUI interface",
                "cmd_status": "Show system status",
                # Validation
                "validation_title": "Ownership Validation",
                "validation_target": "Target",
                "validation_email": "Target Email",
                "validation_user_email": "Your Email",
                "validation_start": "Start Validation",
                "validation_stages": "Stages",
                "validation_stage1": "Stage 1 Verification",
                "validation_stage2": "Stage 2 Verification",
                "validation_cooling": "Cooling Period",
                "validation_authorized": "Authorized",
                # Safety levels
                "safety_discovery": "Discovery",
                "safety_safe": "Safe",
                "safety_moderate": "Moderate",
                "safety_aggressive": "Aggressive",
                # Safety warnings
                "warning_safe": "SAFE",
                "warning_low_risk": "LOW RISK",
                "warning_medium_risk": "MEDIUM RISK",
                "warning_high_risk": "HIGH RISK",
                "warning_critical": "CRITICAL",
                "warning_title_safe": "Safe Operation",
                "warning_title_low_risk": "Low Risk Operation",
                "warning_title_medium_risk": "Medium Risk Operation",
                "warning_title_high_risk": "High Risk Operation",
                "warning_title_critical": "Critical Risk Operation",
                # Messages
                "msg_success": "Success",
                "msg_error": "Error",
                "msg_warning": "Warning",
                "msg_info": "Information",
                "welcome": "Welcome to SAFEX",
                "scan": "Scanning",
                "validate": "Validation",
                "report": "Report",
                "low_risk": "LOW RISK",
                "medium_risk": "MEDIUM RISK",
                "high_risk": "HIGH RISK",
                "critical_risk": "CRITICAL RISK",
                "system_status": "System Status",
                "version": "Version",
                "environment": "Environment",
                "language": "Language",
                "safety_level": "Safety Level",
                "available_scanners": "Available Scanners",
                "available_tools": "Available Tools",
                "available_languages": "Available Languages",
                "validating_target": "Validating target: %s",
                "scanning_target": "Scanning target: %s",
                "generating_report": "Generating report...",
                "validation_success": "Validation successful",
                "validation_failed": "Validation failed",
                "scan_complete": "Scan complete",
                "scan_failed": "Scan failed",
                "findings": "Findings",
                "report_generated": "Report generated",
                "operation_cancelled": "Operation cancelled",
                "aggressive_mode_warning": "WARNING: Aggressive mode enabled!",
            },
            "ru": {
                # App info
                "app_name": "SAFEX",
                "app_version": "1.0.0",
                "app_description": "Структура безопасности для тестирования и выполнения",
                # CLI
                "cli_header": "SAFEX - Структура безопасности для тестирования и выполнения",
                "cli_version": "Версия",
                "cli_help": "Показать справку",
                "cli_debug": "Включить режим отладки",
                "cli_verbose": "Увеличить подробность",
                # Commands
                "cmd_validate": "Валидировать владение целью",
                "cmd_scan": "Запустить сканирование безопасности",
                "cmd_report": "Сгенерировать отчеты",
                "cmd_autofix": "Применить авто-исправления",
                "cmd_tui": "Запустить TUI интерфейс",
                "cmd_status": "Показать статус системы",
                # Validation
                "validation_title": "Валидация владения",
                "validation_target": "Цель",
                "validation_email": "Email цели",
                "validation_user_email": "Ваш Email",
                "validation_start": "Начать валидацию",
                "validation_stages": "Этапы",
                "validation_stage1": "Этап 1: Проверка",
                "validation_stage2": "Этап 2: Проверка",
                "validation_cooling": "Период ожидания",
                "validation_authorized": "Авторизовано",
                # Safety levels
                "safety_discovery": "Обнаружение",
                "safety_safe": "Безопасно",
                "safety_moderate": "Умеренно",
                "safety_aggressive": "Агрессивно",
                # Safety warnings
                "warning_safe": "БЕЗОПАСНО",
                "warning_low_risk": "НИЗКИЙ РИСК",
                "warning_medium_risk": "СРЕДНИЙ РИСК",
                "warning_high_risk": "ВЫСОКИЙ РИСК",
                "warning_critical": "КРИТИЧЕСКИЙ",
                # Messages
                "msg_success": "Успех",
                "msg_error": "Ошибка",
                "msg_warning": "Предупреждение",
                "msg_info": "Информация",
                "welcome": "Добро пожаловать в SAFEX",
                "scan": "Сканирование",
                "validate": "Валидация",
                "report": "Отчет",
                "low_risk": "[+] НИЗКИЙ РИСК",
                "medium_risk": "[!] СРЕДНИЙ РИСК",
                "high_risk": "[X] ВЫСОКИЙ РИСК",
                "critical_risk": "[!!] КРИТИЧЕСКИЙ РИСК",
                "system_status": "Статус системы",
                "version": "Версия",
                "environment": "Среда",
                "language": "Язык",
                "safety_level": "Уровень безопасности",
                "available_scanners": "Доступные сканеры",
                "available_tools": "Доступные инструменты",
                "available_languages": "Доступные языки",
                "validating_target": "Валидация цели: %s",
                "scanning_target": "Сканирование цели: %s",
                "generating_report": "Генерация отчета...",
                "validation_success": "Валидация успешна",
                "validation_failed": "Валидация не удалась",
                "scan_complete": "Сканирование завершено",
                "scan_failed": "Сканирование не удалось",
                "findings": "Результаты",
                "report_generated": "Отчет сгенерирован",
                "operation_cancelled": "Операция отменена",
                "aggressive_mode_warning": "ВНИМАНИЕ: Агрессивный режим включен!",
            },
        }

    def translate(self, key: str, language: Optional[str] = None) -> str:
        """
        Get translation for key

        Args:
            key: Translation key
            language: Optional language code (e.g. 'en', 'ru')

        Returns:
            Translated string or key if not found
        """
        if language is not None:
            translations = self.all_translations.get(language, self.current_translations)
            return translations.get(key, key)
        return self.current_translations.get(key, key)

    def set_language(self, language: Language):
        """
        Set current language

        Args:
            language: Language to set
        """
        self.language = language
        self.current_translations = self.all_translations.get(
            language.value, self.all_translations["en"]
        )

    def get_language_name(self, language: Language) -> str:
        """
        Get language display name

        Args:
            language: Language enum

        Returns:
            Language display name
        """
        names = {
            Language.ENGLISH: "English",
            Language.RUSSIAN: "Русский",
            Language.SPANISH: "Español",
            Language.FRENCH: "Français",
            Language.GERMAN: "Deutsch",
            Language.CHINESE: "中文",
            Language.JAPANESE: "日本語",
            Language.ARABIC: "العربية",
            Language.PORTUGUESE: "Português",
            Language.ITALIAN: "Italiano",
        }
        return names.get(language, language.value)

    def get_available_languages(self) -> list:
        """Get list of available language codes"""
        return list(self.all_translations.keys())


# Global translation manager instance
_translation_manager = None


def get_translation_manager(language: Optional[Language] = None) -> TranslationManager:
    """
    Get global translation manager instance

    Args:
        language: Optional language to set

    Returns:
        TranslationManager instance
    """
    global _translation_manager

    if _translation_manager is None:
        _translation_manager = TranslationManager(language or Language.ENGLISH)
    elif language is not None:
        _translation_manager.set_language(language)

    return _translation_manager


def t(key: str) -> str:
    """
    Translate a key (shorthand function)

    Args:
        key: Translation key

    Returns:
        Translated string
    """
    return get_translation_manager().translate(key)


# Convenience functions for common translations
def get_safety_warning(level: str) -> str:
    """Get safety warning label for level"""
    warnings = {
        "safe": t("warning_safe"),
        "low_risk": t("warning_low_risk"),
        "medium_risk": t("warning_medium_risk"),
        "high_risk": t("warning_high_risk"),
        "critical": t("warning_critical"),
    }
    return warnings.get(level, t("warning_safe"))


def get_safety_level(level: str) -> str:
    """Get safety level name"""
    levels = {
        "discovery": t("safety_discovery"),
        "safe": t("safety_safe"),
        "moderate": t("safety_moderate"),
        "aggressive": t("safety_aggressive"),
    }
    return levels.get(level, level)
