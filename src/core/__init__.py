"""
Core modules for Writing Assistant Pro

This package contains the core functionality modules including:
- translation: Language management and internationalization using
  gettext/Babel
- logger: Centralized logging system
- styles: Theme management (placeholder for Flet)
- config: Application configuration and command line argument parsing
- window_manager: Window visibility and lifecycle management
- hotkey_manager: Global hotkey registration and management
"""

from __future__ import annotations

# Import config system
from .config.manager import ConfigManager, parse_arguments
from .enums import AttachmentID, AttachmentType, DialogType, EventType, SourceType
from .error_handler import (
    AppError,
    ConfigError,
    ErrorContext,
    HotkeyError,
    InputError,
    UIError,
    handle_error,
    safe_execute,
)
from .event_bus import EventBus, emit_event, get_event_bus, on_event

# Import hotkey management system
from .managers.hotkey import HotkeyManager

# Import systray management system
from .managers.systray import SystrayManager

# Import window manager system
from .managers.window import WindowManager
from .resource_manager import (
    ResourceTracker,
    safe_file_read,
    safe_file_write,
    safe_image_open,
    safe_json_read,
    safe_json_write,
    temp_working_directory,
)

# Import monitoring (activates global event subscribers)
# Import logger system
from .services.logger import setup_exception_handler, setup_root_logger

# Import translation system
from .services.translation import (
    LanguageManager,
    _,
    change_language,
    get_current_language,
    get_language_manager,
    init_translation,
)
from .state import AppState, UIState
from .utils.paths import get_app_root, get_icon_path

__all__ = [
    # Translation system
    "LanguageManager",
    "get_language_manager",
    "init_translation",
    "_",
    "change_language",
    "get_current_language",
    # Logger system
    "setup_root_logger",
    "setup_exception_handler",
    # Config system
    "parse_arguments",
    "ConfigManager",
    # Hotkey management system
    "HotkeyManager",
    # Systray management system
    "SystrayManager",
    # Window manager system
    "WindowManager",
    # State management
    "AppState",
    "UIState",
    # Event bus
    "EventBus",
    "get_event_bus",
    "emit_event",
    "on_event",
    # Enums
    "AttachmentID",
    "AttachmentType",
    "SourceType",
    "EventType",
    "DialogType",
    # Error handling
    "AppError",
    "ConfigError",
    "HotkeyError",
    "InputError",
    "UIError",
    "handle_error",
    "safe_execute",
    "ErrorContext",
    # Resource management
    "safe_image_open",
    "safe_file_read",
    "safe_file_write",
    "safe_json_read",
    "safe_json_write",
    "temp_working_directory",
    "ResourceTracker",
    "get_icon_path",
    "get_app_root",
]
