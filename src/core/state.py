"""
Application State Management

Centralized state management for Writing Assistant Pro.
Provides a single source of truth for application state.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.config.manager import ConfigManager
from src.core.services.input_source import InputState


@dataclass
class UIState:
    """UI-related state"""

    sidebar_visible: bool = False
    settings_visible: bool = False
    about_visible: bool = False
    dark_mode: bool = True
    language: str = "fr"


@dataclass
class AppState:
    """Centralized application state"""

    config: ConfigManager
    input_state: InputState
    ui_state: UIState
