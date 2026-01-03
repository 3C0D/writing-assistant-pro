"""
Settings View for Writing Assistant Pro
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import flet as ft

from src.core import (
    ConfigManager,
    _,
    change_language,
    get_current_language,
    get_language_manager,
)
from src.core.services.hotkey_capture import format_hotkey_for_display
from src.ui.design_system import AppColors
from src.ui.dialogs import HotkeyDialogResult, show_hotkey_capture_dialog

if TYPE_CHECKING:
    from src.core.managers.hotkey import HotkeyManager
    from src.core.managers.window import WindowManager


class SettingsView:
    """Encapsulates the settings view logic."""

    def __init__(
        self,
        config: ConfigManager,
        hotkey_manager: HotkeyManager,
        window_manager: WindowManager | None,
        page: ft.Page,
        on_theme_toggle: Callable,
        on_ui_refresh: Callable,
        on_show_snackbar: Callable,
        on_check_updates: Callable,
    ):
        self.config = config
        self.hotkey_manager = hotkey_manager
        self.window_manager = window_manager
        self.page = page
        self._on_theme_toggle = on_theme_toggle
        self._on_ui_refresh = on_ui_refresh
        self._on_show_snackbar = on_show_snackbar
        self._on_check_updates = on_check_updates
        self.hotkey_initial_value = ""

    def build(self) -> ft.Container:
        """Build and return the settings view container."""
        # Store initial hotkey value for change detection
        self.hotkey_initial_value = self.config.HOTKEY_COMBINATION

        # Language selector
        language_dropdown = ft.Dropdown(
            label=_("Language"),
            options=[
                ft.dropdown.Option(lang, get_language_manager().get_language_name(lang))
                for lang in get_language_manager().get_available_languages()
            ],
            value=get_current_language(),
            on_change=self.on_language_change,
            width=300,
        )

        # Hotkey display (clickable to edit)
        hotkey_display = self._create_hotkey_display()

        # Floating buttons at top right
        from src.ui.components.top_action_bar import create_top_action_bar

        action_bar = create_top_action_bar(
            dark_mode=self.config.DARK_MODE,
            hotkey_combination=self.config.HOTKEY_COMBINATION,
            on_theme_toggle=self._on_theme_toggle,
            on_hide_click=self.on_hide_click,
        )

        return ft.Container(
            content=ft.Column(
                [
                    action_bar,
                    ft.Text(
                        _("Settings"),
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.get_text_primary(self.config.DARK_MODE),
                    ),
                    ft.Divider(),
                    ft.Text(
                        _("General"),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.get_text_primary(self.config.DARK_MODE),
                    ),
                    ft.Divider(),
                    language_dropdown,
                    ft.Container(height=20),
                    hotkey_display,
                    ft.Container(height=20),
                    # Check for updates button
                    ft.ElevatedButton(
                        text=_("Check for Updates"),
                        icon=ft.Icons.SYSTEM_UPDATE,
                        on_click=self._on_check_updates,
                        width=300,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
            bgcolor=AppColors.get_bg_primary(self.config.DARK_MODE),
        )

    def _create_hotkey_display(self) -> ft.Container:
        """Create clickable hotkey display that opens capture dialog."""
        current_hotkey = self.config.HOTKEY_COMBINATION
        display_text = format_hotkey_for_display(current_hotkey)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        _("Shortcut Key"),
                        size=12,
                        color=AppColors.get_text_secondary(self.config.DARK_MODE),
                    ),
                    ft.Container(
                        content=ft.Text(
                            display_text,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.get_text_primary(self.config.DARK_MODE),
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                        border_radius=8,
                        bgcolor=AppColors.get_bg_secondary(self.config.DARK_MODE),
                        border=ft.border.all(
                            1, AppColors.get_text_secondary(self.config.DARK_MODE)
                        ),
                    ),
                ],
                spacing=5,
            ),
            on_click=self._on_hotkey_click,
            width=300,
        )

    def _on_hotkey_click(self, e) -> None:
        """Handle click on hotkey display to open capture dialog."""
        if not self.page:
            return

        show_hotkey_capture_dialog(
            page=self.page,
            current_hotkey=self.config.HOTKEY_COMBINATION,
            dark_mode=self.config.DARK_MODE,
            on_result=self._on_hotkey_dialog_result,
            hotkey_manager=self.hotkey_manager,
        )

    def _on_hotkey_dialog_result(self, result: HotkeyDialogResult) -> None:
        """Handle result from hotkey capture dialog."""
        if result.action == "cancel":
            # Re-register the original hotkey (was unregistered when dialog opened)
            if self.config.HOTKEY_COMBINATION and self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        if result.action == "save":
            new_hotkey = result.hotkey
        else:
            # Unknown action, just re-register original
            if self.config.HOTKEY_COMBINATION and self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        # Update config
        self.config.HOTKEY_COMBINATION = new_hotkey or ""

        # Re-register the hotkey (or unregister if None)
        if new_hotkey:
            if self.window_manager:
                self.hotkey_manager.reregister(self.window_manager.toggle_window)
        # Already unregistered when dialog opened, no need to unregister again

        # Refresh UI to show new hotkey
        self._on_ui_refresh()

        # Show confirmation
        if self.page:
            display = format_hotkey_for_display(new_hotkey) if new_hotkey else _("None")
            self._on_show_snackbar(_("Hotkey: {display}").format(display=display))
            self.page.update()

    def on_language_change(self, e):
        """Language change handler"""
        if not self.page:
            return

        new_lang = e.control.value
        change_language(new_lang)

        # UI recreation is now handled by the event listener for EventType.LANGUAGE_CHANGED

        lang_name = get_language_manager().get_language_name(new_lang)
        self._on_show_snackbar(_("Language changed to {language}").format(language=lang_name))

    def on_hide_click(self, e) -> None:
        """Handle hide button click."""
        if self.window_manager:
            self.window_manager.hide_window()
