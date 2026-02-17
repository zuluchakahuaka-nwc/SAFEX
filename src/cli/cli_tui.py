"""
TUI (Text User Interface) for SAFEX
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import get_logger
from src.i18n.translation_manager import TranslationManager

logger = get_logger("tui")


def display_menu(language: str = "en"):
    """Display main menu"""
    tm = TranslationManager()

    print()
    print("=" * 60)
    print(f"🛡️  {tm.translate('menu_title', language=language)}")
    print("=" * 60)
    print()
    print("  1. " + tm.translate("menu_validate", language=language))
    print("  2. " + tm.translate("menu_scan", language=language))
    print("  3. " + tm.translate("menu_report", language=language))
    print("  4. " + tm.translate("menu_status", language=language))
    print("  5. " + tm.translate("menu_settings", language=language))
    print("  6. " + tm.translate("menu_language", language=language))
    print("  0. " + tm.translate("menu_exit", language=language))
    print()
    print("=" * 60)


def display_language_menu():
    """Display language selection menu"""
    print()
    print("=" * 60)
    print("🌍 Language / Язык / Idioma / Langue")
    print("=" * 60)
    print()
    print("  1. English")
    print("  2. Русский")
    print("  3. Español")
    print("  4. Français")
    print("  5. Deutsch")
    print("  6. 中文")
    print("  7. 日本語")
    print("  8. العربية")
    print("  9. Português")
    print(" 10. Italiano")
    print()
    print("  0. Back / Назад / Volver")
    print()
    print("=" * 60)


def get_choice(prompt: str, max_choice: int) -> int:
    """Get user choice"""
    while True:
        try:
            choice = int(input(prompt))
            if 0 <= choice <= max_choice:
                return choice
            else:
                print(f"⚠️  Please enter a number between 0 and {max_choice}")
        except ValueError:
            print("⚠️  Please enter a valid number")


def main():
    """Main TUI loop"""
    language = "en"

    while True:
        display_menu(language)
        choice = get_choice("Enter your choice: ", 6)

        if choice == 0:
            print("👋 Goodbye!")
            break
        elif choice == 1:
            print(
                f"\n🔍 {TranslationManager().translate('menu_validate', language=language)}"
            )
            print("   (Functionality coming soon)")
        elif choice == 2:
            print(
                f"\n🔎 {TranslationManager().translate('menu_scan', language=language)}"
            )
            print("   (Functionality coming soon)")
        elif choice == 3:
            print(
                f"\n📊 {TranslationManager().translate('menu_report', language=language)}"
            )
            print("   (Functionality coming soon)")
        elif choice == 4:
            print(
                f"\n📈 {TranslationManager().translate('menu_status', language=language)}"
            )
            print("   (Functionality coming soon)")
        elif choice == 5:
            print(
                f"\n⚙️  {TranslationManager().translate('menu_settings', language=language)}"
            )
            print("   (Functionality coming soon)")
        elif choice == 6:
            display_language_menu()
            lang_choice = get_choice("Select language: ", 10)

            lang_map = {
                1: "en",
                2: "ru",
                3: "es",
                4: "fr",
                5: "de",
                6: "zh",
                7: "ja",
                8: "ar",
                9: "pt",
                10: "it",
            }

            if lang_choice in lang_map:
                language = lang_map[lang_choice]
                print(f"✅ Language changed to: {language}")
            else:
                print("👋 Back to main menu")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
