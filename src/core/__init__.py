"""
Core modules for Writing Assistant Pro

This package contains the core functionality modules including:
- translation: Language management and internationalization
"""

from .translation import *

__all__ = [
    'LanguageManager',
    'init_translation',
    '_',
    'change_language',
    'get_current_language',
    'get_language_manager',
    'register_ui_update'
]