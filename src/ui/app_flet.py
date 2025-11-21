"""
Main Flet application for Writing Assistant Pro
"""

from __future__ import annotations

import flet as ft
from loguru import logger

from src.core import (
    ConfigManager,
    HotkeyManager,
    WindowManager,
    _,
    change_language,
    get_current_language,
    get_language_manager,
    init_translation,
    setup_root_logger,
)
from src.core.systray_manager import SystrayManager


class WritingAssistantFletApp:
    """Main Flet application class"""

    def __init__(self):
        self.config = ConfigManager()

        # Setup logging
        setup_root_logger(debug=self.config.DEBUG)
        self.log = logger.bind(name="WritingAssistant.FletApp")

        # Initialize translation
        init_translation(
            "writing_assistant",
            "translations",
            self.config.LANGUAGE,
            self.config.AVAILABLE_LANGUAGES,
        )

        self.hotkey_manager = HotkeyManager(self.config)
        self.window_manager: WindowManager | None = None
        self.page: ft.Page | None = None
        self.systray_manager: SystrayManager | None = None

        # UI Elements references for updates
        self.ui_elements = {}

    def main(self, page: ft.Page):
        """Main Flet page setup"""
        self.page = page
        self.log.info("Flet application starting...")

        # Initialize WindowManager with page
        self.window_manager = WindowManager(self.config, page)

        # Page configuration
        page.title = (
            "🔥 Writing Assistant Pro (DEV MODE)" if self.config.DEBUG else "Writing Assistant Pro"
        )
        page.window.width = 800
        page.window.height = 600
        page.theme_mode = ft.ThemeMode.DARK if self.config.DARK_MODE else ft.ThemeMode.LIGHT
        page.padding = 0

        # Prevent app from closing when window is closed (hide instead)
        page.window.prevent_close = True
        page.window.on_event = self.on_window_event

        # Hide window on start (systray mode)
        page.window.visible = False

        # Create UI
        self._create_ui()

        # Setup hotkey for toggle with logging
        self.log.info(f"Registering hotkey: {self.config.HOTKEY_COMBINATION}")
        self.hotkey_manager.register_delayed(self.window_manager.toggle_window)

        # Initialize and start systray
        self.systray_manager = SystrayManager(page, on_about=self.show_about, app=self)
        self.systray_manager.run_async()
        self.log.info("Systray manager started")

        page.update()
        self.log.info("Flet application started")

    def on_window_event(self, e):
        """Handle window events"""
        if e.data == "close" and self.window_manager:
            self.window_manager.hide_window()

    def _create_ui(self):
        """Create the user interface"""
        if not self.page:
            return

        # AppBar (header)
        self.page.appbar = ft.AppBar(
            title=ft.Text("Writing Assistant Pro", color=ft.Colors.WHITE),
            center_title=False,
            bgcolor=ft.Colors.BLUE_600,
            actions=[
                ft.IconButton(
                    icon=(ft.Icons.DARK_MODE if not self.config.DARK_MODE else ft.Icons.LIGHT_MODE),
                    icon_color=ft.Colors.WHITE,
                    tooltip="Toggle Dark/Light Mode",
                    on_click=self.toggle_theme,
                    data="theme_btn",
                ),
                ft.IconButton(
                    icon=ft.Icons.VISIBILITY_OFF,
                    icon_color=ft.Colors.WHITE,
                    tooltip=f"Hide ({self.config.HOTKEY_COMBINATION})",
                    on_click=lambda _: self.window_manager.hide_window()
                    if self.window_manager
                    else None,
                ),
            ],
        )

        # Language selector
        self.ui_elements["language_select"] = ft.Dropdown(
            label=_("Language"),
            options=[
                ft.dropdown.Option(lang, get_language_manager().get_language_name(lang))
                for lang in get_language_manager().get_available_languages()
            ],
            value=get_current_language(),
            on_change=self.on_language_change,
            width=150,
        )

        # Main content
        self.ui_elements["label_main"] = ft.Text(
            _("Hello, this is a real desktop app!"),
            size=18,
        )

        self.ui_elements["button_main"] = ft.ElevatedButton(
            _("Click me"),
            on_click=self.on_button_click,
        )

        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.ui_elements["language_select"]]),
                        ft.Column(
                            [
                                self.ui_elements["label_main"],
                                self.ui_elements["button_main"],
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=20,
                ),
                padding=20,
            )
        )

    def on_button_click(self, e):
        """Button click handler"""
        if not self.page:
            return

        snack_bar = ft.SnackBar(ft.Text(_("Clicked!!!")))
        self.page.open(snack_bar)

    def on_language_change(self, e):
        """Language change handler"""
        if not self.page:
            return

        new_lang = e.control.value
        change_language(new_lang)

        # Update all text
        self.ui_elements["label_main"].value = _("Hello, this is a real desktop app!")
        self.ui_elements["button_main"].text = _("Click me")
        self.ui_elements["language_select"].label = _("Language")

        # Update dropdown options
        self.ui_elements["language_select"].options = [
            ft.dropdown.Option(lang, get_language_manager().get_language_name(lang))
            for lang in get_language_manager().get_available_languages()
        ]

        snack_bar = ft.SnackBar(ft.Text(f"Language changed to {new_lang}"))
        self.page.open(snack_bar)
        self.page.update()

    def toggle_theme(self, e):
        """Toggle dark/light theme"""
        if not self.page:
            return

        new_dark_mode = not self.config.DARK_MODE
        self.config.DARK_MODE = new_dark_mode
        self.page.theme_mode = ft.ThemeMode.DARK if new_dark_mode else ft.ThemeMode.LIGHT

        # Safely update icon if appbar exists and is of correct type
        if (
            self.page.appbar
            and isinstance(self.page.appbar, ft.AppBar)
            and self.page.appbar.actions
        ):
            self.page.appbar.actions[0].icon = (  # type: ignore[union-attr]
                ft.Icons.DARK_MODE if not new_dark_mode else ft.Icons.LIGHT_MODE
            )
        self.page.update()

    def show_about(self):
        """Show about window (placeholder for now)"""
        if not self.page:
            return

        self.log.info("About window requested (not implemented yet)")
        # Show window and display a simple message
        self.page.window.visible = True
        snack_bar = ft.SnackBar(ft.Text(_("About window - Coming soon!")))
        self.page.open(snack_bar)
        self.page.update()
