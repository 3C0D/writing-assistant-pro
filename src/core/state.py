"""
Application State Management

Centralized state management for Writing Assistant Pro.
Provides a single source of truth for application state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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
    attachments: list[Any] = field(default_factory=list)

    def update_config(self, key: str, value: Any) -> None:
        """Update configuration and persist"""
        self.config.set(key, value)

    def update_ui_state(self, **kwargs) -> None:
        """Update UI state"""
        for key, value in kwargs.items():
            if hasattr(self.ui_state, key):
                setattr(self.ui_state, key, value)

    def clear_attachments(self) -> None:
        """Clear all attachments"""
        self.attachments.clear()

    def add_attachment(self, attachment: Any) -> None:
        """Add an attachment"""
        self.attachments.append(attachment)

    def remove_attachment(self, attachment_id: str) -> None:
        """Remove attachment by ID"""
        self.attachments = [a for a in self.attachments if getattr(a, "id", None) != attachment_id]
