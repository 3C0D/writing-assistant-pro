"""
Core modules for Writing Assistant Pro

This package contains the core functionality modules including:
- translation: Language management and internationalization using gettext/Babel
- logger: Centralized logging system
- styles: Theme management (light/dark)
"""

# Import translation system
from .translation import (
    LanguageManager,
    get_language_manager,
    init_translation,
    _,
    change_language,
    get_current_language,
    register_ui_update
)

# Import logger system
from .logger import setup_logger

# Import styles system
from .styles import apply_theme

__all__ = [
    # Translation system
    'LanguageManager',
    'get_language_manager',
    'init_translation',
    '_',
    'change_language',
    'get_current_language',
    'register_ui_update',
    
    # Logger system
    'setup_logger',
    
    # Styles system
    'apply_theme'
]