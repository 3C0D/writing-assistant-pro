"""UI dialogs"""

from __future__ import annotations

from src.ui.dialogs.hotkey_dialog import HotkeyDialogResult, show_hotkey_capture_dialog
from src.ui.dialogs.update_dialog import (
    show_no_update_dialog,
    show_update_dialog,
    show_update_error_dialog,
)

__all__ = [
    "show_update_dialog",
    "show_no_update_dialog",
    "show_update_error_dialog",
    "show_hotkey_capture_dialog",
    "HotkeyDialogResult",
]
