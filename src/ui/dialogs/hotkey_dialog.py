"""
Hotkey capture dialog for Writing Assistant Pro

Modal dialog for capturing and editing keyboard shortcuts
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

import flet as ft
from loguru import logger

from src.core import _
from src.core.services.hotkey_capture import (
    DEFAULT_HOTKEY,
    HotkeyCapture,
    format_hotkey_for_display,
)
from src.ui.design_system import AppColors

if TYPE_CHECKING:
    from src.core.managers.hotkey import HotkeyManager

# Fix for Windows console encoding (emojis)
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass


class HotkeyDialogResult:
    """Result from the hotkey capture dialog."""

    def __init__(self, action: str, hotkey: str | None = None):
        """
        Initialize dialog result.

        Args:
            action: One of "save", "reset", "delete", "cancel"
            hotkey: The captured hotkey (for "save" action) or None
        """
        self.action = action
        self.hotkey = hotkey


def show_hotkey_capture_dialog(
    page: ft.Page,
    current_hotkey: str | None,
    dark_mode: bool,
    on_result: Callable[[HotkeyDialogResult], None],
    hotkey_manager: HotkeyManager | None = None,
) -> None:
    """
    Show the hotkey capture modal dialog.

    Args:
        page: Flet page instance
        current_hotkey: Current hotkey in storage format (e.g., "ctrl+shift+a")
        dark_mode: Whether dark mode is active
        on_result: Callback with dialog result
        hotkey_manager: Optional HotkeyManager to suspend during capture
    """
    log = logger.bind(name="WritingAssistant.HotkeyDialog")
    capture = HotkeyCapture()
    captured_hotkey: str | None = current_hotkey

    # Suspend global hotkey during capture to avoid conflicts
    if hotkey_manager:
        log.debug("Suspending global hotkey during capture")
        hotkey_manager.unregister()

    # Display text for current hotkey
    display_text = ft.Text(
        format_hotkey_for_display(current_hotkey) if current_hotkey else _("None"),
        size=24,
        weight=ft.FontWeight.BOLD,
        color=AppColors.ACCENT,
        text_align=ft.TextAlign.CENTER,
    )

    # Instructions text
    instructions = ft.Column(
        [
            ft.Text(
                _("Press the key combination you want to use."),
                size=14,
                color=AppColors.get_text_secondary(dark_mode),
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                _("Tip: With Shift, press the main key FIRST, then add modifiers."),
                size=12,
                italic=True,
                color=AppColors.get_text_secondary(dark_mode),
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    def on_key_update(display_hotkey: str) -> None:
        """Called when keys are pressed during capture."""
        nonlocal captured_hotkey
        display_text.value = display_hotkey
        # Convert display to storage format
        parts = [p.strip().lower() for p in display_hotkey.split(" + ")]
        captured_hotkey = "+".join(parts) if parts and parts[0] else None
        page.update()

    def close_dialog() -> None:
        """Stop capture and close dialog."""
        capture.stop_capture()
        page.close(dialog)
        # Note: hotkey re-registration is handled by the caller via on_result callback

    def on_save(e) -> None:
        """Save the current hotkey and close dialog."""
        close_dialog()
        log.info(f"Hotkey dialog: Save - {captured_hotkey}")
        on_result(HotkeyDialogResult("save", captured_hotkey))

    def on_reset(e) -> None:
        """Reset to default hotkey (update display, don't close)."""
        nonlocal captured_hotkey
        captured_hotkey = DEFAULT_HOTKEY
        display_text.value = format_hotkey_for_display(DEFAULT_HOTKEY)
        log.debug(f"Hotkey display reset to default: {DEFAULT_HOTKEY}")
        page.update()

    def on_delete(e) -> None:
        """Delete hotkey / set to None (update display, don't close)."""
        nonlocal captured_hotkey
        captured_hotkey = None
        display_text.value = _("None")
        log.debug("Hotkey display set to None")
        page.update()

    def on_cancel(e) -> None:
        """Cancel without changes."""
        close_dialog()
        log.info("Hotkey dialog: Cancel")
        on_result(HotkeyDialogResult("cancel", None))

    # Button styles
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            _("Shortcut Key"),
            size=18,
            weight=ft.FontWeight.BOLD,
            color=AppColors.get_text_primary(dark_mode),
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    instructions,
                    ft.Container(height=20),
                    ft.Container(
                        content=display_text,
                        padding=ft.padding.all(20),
                        border_radius=10,
                        bgcolor=AppColors.get_bg_secondary(dark_mode),
                        alignment=ft.alignment.center,
                        width=300,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=350,
        ),
        actions=[
            ft.ElevatedButton(
                text=_("Save"),
                style=button_style,
                bgcolor=AppColors.SUCCESS,
                color=AppColors.TEXT_PRIMARY_DARK,
                on_click=on_save,
            ),
            ft.ElevatedButton(
                text=_("Reset"),
                style=button_style,
                bgcolor=AppColors.get_bg_secondary(dark_mode),
                color=AppColors.get_text_primary(dark_mode),
                on_click=on_reset,
            ),
            ft.ElevatedButton(
                text=_("Delete"),
                style=button_style,
                bgcolor=AppColors.ERROR,
                color=AppColors.TEXT_PRIMARY_DARK,
                on_click=on_delete,
            ),
            ft.ElevatedButton(
                text=_("Cancel"),
                style=button_style,
                bgcolor=AppColors.get_bg_secondary(dark_mode),
                color=AppColors.get_text_primary(dark_mode),
                on_click=on_cancel,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=AppColors.get_bg_primary(dark_mode),
    )

    # Start capturing keys when dialog opens
    capture.start_capture(on_key_update)

    page.open(dialog)
    log.debug("Hotkey capture dialog opened")
