"""
Core modules for Writing Assistant Pro

This package contains the core functionality modules including:
- translation: Language management and internationalization using gettext/Babel
- logger: Centralized logging system
- styles: Theme management (light/dark)
- config: Application configuration and command line argument parsing
- window_manager: Window visibility and lifecycle management
- hotkey_manager: Global hotkey registration and management
"""

# Import translation system
# Import app system
from .app import WritingAssistantApp

# Import config system
from .config import ConfigManager, parse_arguments

# Import hotkey management system
from .hotkey_manager import HotkeyManager

# Import logger system
from .logger import setup_root_logger

# Import styles system
from .styles import apply_theme, setup_css_hot_reload, stop_css_hot_reload
from .translation import (
    LanguageManager,
    _,
    change_language,
    get_current_language,
    get_language_manager,
    init_translation,
    register_ui_update,
)

# Import window manager system
from .window_manager import WindowManager

__all__ = [
    # Translation system
    "LanguageManager",
    "get_language_manager",
    "init_translation",
    "_",
    "change_language",
    "get_current_language",
    "register_ui_update",
    # Logger system
    "setup_root_logger",
    # Styles system
    "apply_theme",
    "setup_css_hot_reload",
    "stop_css_hot_reload",
    # Config system
    "parse_arguments",
    "ConfigManager",
    # App system
    "WritingAssistantApp",
    # Hotkey management system
    "HotkeyManager",
    # Window manager system
    "WindowManager",
]
