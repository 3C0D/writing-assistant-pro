"""
Translation module for NiceGUI applications.
Provides internationalization support using gettext.
"""

from __future__ import annotations

import gettext
from collections.abc import Callable
from pathlib import Path

from .config import get_app_root


class LanguageManager:
    """Manages language translations for NiceGUI applications."""

    def __init__(
        self,
        app_name: str = "writing_assistant",
        locales_dir: str = "translations",
        default_language: str = "en",
        available_languages: list[str] | None = None,
    ):
        """
        Initialize the Language Manager.

        Args:
            app_name: Application name for gettext domain
            locales_dir: Directory containing locale files
            default_language: Default language code
            available_languages: List of available language codes
        """
        self.app_name = app_name
        # Use get_app_root() to resolve relative paths
        path = Path(locales_dir)
        if not path.is_absolute():
            self.locales_dir = get_app_root() / path
        else:
            self.locales_dir = path

        self.current_language = default_language
        self.available_languages = available_languages or ["en", "fr", "it"]

        # Translation cache
        self._translations: dict[str, gettext.NullTranslations | gettext.GNUTranslations] = {}

        # UI update callbacks
        self._update_callbacks: list[Callable] = []

        # Initialize the current language
        self.set_language(default_language)

    def set_language(self, language: str) -> None:
        """
        Set the current language and load translations.

        Args:
            language: Language code (e.g., 'en', 'fr', 'it')
        """
        if language not in self.available_languages:
            language = "en"  # Fallback to default

        self.current_language = language

        # Set up gettext for this language
        try:
            # Create locale path
            locale_path = self.locales_dir / language / "LC_MESSAGES"

            # Load translation
            if locale_path.exists():
                translation = gettext.translation(
                    self.app_name,
                    localedir=str(self.locales_dir),
                    languages=[language],
                    fallback=True,
                )
                self._translations[language] = translation
            else:
                # Create a simple fallback translation
                self._translations[language] = gettext.NullTranslations()

            # Install the translation globally
            self._translations[language].install()

            # Trigger UI updates
            self._trigger_ui_updates()

        except Exception as e:
            print(f"Warning: Could not load language '{language}': {e}")
            # Fallback to null translation
            self._translations[language] = gettext.NullTranslations()
            self._translations[language].install()

    def _(self, text: str) -> str:
        """
        Translate text to the current language.

        Args:
            text: Text to translate

        Returns:
            Translated text
        """
        if self.current_language in self._translations:
            return self._translations[self.current_language].gettext(text)
        return text

    def get_language_name(self, language: str | None = None) -> str:
        """
        Get the human-readable name of a language.

        Args:
            language: Language code, defaults to current language

        Returns:
            Human-readable language name
        """
        if language is None:
            language = self.current_language

        language_names: dict[str, str] = {
            "en": "English",
            "fr": "Français",
            "it": "Italiano",
            "es": "Español",
            "de": "Deutsch",
            "pt": "Português",
            "ru": "Русский",
            "zh": "中文",
            "ja": "日本語",
        }
        return language_names.get(language, language)

    # Not used
    def register_ui_update_callback(self, callback: Callable) -> None:
        """
        Register a callback function to be called when language changes.
        This is used to update UI elements dynamically.

        Args:
            callback: Function to call on language change
        """
        self._update_callbacks.append(callback)

    def _trigger_ui_updates(self) -> None:
        """Trigger all registered UI update callbacks."""
        for callback in self._update_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in UI update callback: {e}")

    def get_current_language(self) -> str:
        """Get the current language code."""
        return self.current_language

    def get_available_languages(self) -> list[str]:
        """Get list of available language codes."""
        return self.available_languages.copy()

    def is_available(self, language: str) -> bool:
        """Check if a language is available."""
        return language in self.available_languages


# Global language manager instance
_language_manager: LanguageManager | None = None


def get_language_manager() -> LanguageManager:
    """Get the global language manager instance."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


def init_translation(
    app_name: str = "writing_assistant",
    locales_dir: str = "translations",
    default_language: str = "en",
    available_languages: list[str] | None = None,
) -> LanguageManager:
    """
    Initialize the global translation system.

    Args:
        app_name: Application name for gettext domain
        locales_dir: Directory containing locale files
        default_language: Default language code
        available_languages: List of available language codes

    Returns:
        Initialized LanguageManager instance
    """
    global _language_manager
    _language_manager = LanguageManager(
        app_name, locales_dir, default_language, available_languages
    )
    return _language_manager


def _(text: str) -> str:
    """
    Convenience function for translation.

    Args:
        text: Text to translate

    Returns:
        Translated text
    """
    return get_language_manager()._(text)


def change_language(language: str) -> None:
    """
    Change the current language.

    Args:
        language: Language code to switch to
    """
    get_language_manager().set_language(language)


def get_current_language() -> str:
    """Get the current language code."""
    return get_language_manager().get_current_language()


# Not used
def register_ui_update(callback: Callable) -> None:
    """
    Register a UI update callback for language changes.

    Args:
        callback: Function to call when language changes
    """
    get_language_manager().register_ui_update_callback(callback)
