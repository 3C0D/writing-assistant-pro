"""
UI Views package for Writing Assistant Pro
"""

from __future__ import annotations

from src.ui.views.about_view import create_about_view
from src.ui.views.main_view import create_main_content
from src.ui.views.settings_view import SettingsView

__all__ = [
    "create_about_view",
    "create_main_content",
    "SettingsView",
]
