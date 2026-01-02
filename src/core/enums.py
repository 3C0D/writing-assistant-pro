"""
Enums for Writing Assistant Pro

Centralized enums for IDs, event types, and constants.
"""

from __future__ import annotations

from enum import Enum


class AttachmentID(str, Enum):
    """Attachment IDs for source-based attachments"""

    SELECTION_TEXT = "selection_text"
    CLIPBOARD_TEXT = "clipboard_text"
    CLIPBOARD_IMAGE = "clipboard_image"


class AttachmentType(str, Enum):
    """Attachment types"""

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"


class SourceType(str, Enum):
    """Input source types"""

    SELECTION = "selection"
    CLIPBOARD = "clipboard"


class EventType(str, Enum):
    """Event types for EventBus"""

    # Window events
    WINDOW_PRE_SHOW = "window_pre_show"  # Before window gains focus
    WINDOW_SHOWN = "window_shown"
    WINDOW_HIDDEN = "window_hidden"

    # Input events
    INPUT_SOURCE_DETECTED = "input_source_detected"
    ATTACHMENT_ADDED = "attachment_added"
    ATTACHMENT_REMOVED = "attachment_removed"

    # UI events
    THEME_CHANGED = "theme_changed"
    LANGUAGE_CHANGED = "language_changed"
    SETTINGS_TOGGLED = "settings_toggled"
    SIDEBAR_TOGGLED = "sidebar_toggled"

    # Hotkey events
    HOTKEY_REGISTERED = "hotkey_registered"
    HOTKEY_CHANGED = "hotkey_changed"
    HOTKEY_CAPTURED = "hotkey_captured"

    # Submission events
    PROMPT_SUBMITTED = "prompt_submitted"

    # Update events
    UPDATE_CHECK_STARTED = "update_check_started"
    UPDATE_AVAILABLE = "update_available"
    UPDATE_NOT_AVAILABLE = "update_not_available"
    UPDATE_ERROR = "update_error"


class DialogType(str, Enum):
    """Dialog types"""

    HOTKEY_CAPTURE = "hotkey_capture"
    UPDATE_AVAILABLE = "update_available"
    UPDATE_ERROR = "update_error"
    NO_UPDATE = "no_update"
