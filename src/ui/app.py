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
)
from src.core.managers.systray import SystrayManager
from src.ui.components import (
    create_navigation_rail,
    create_sidebar,
    icon_button,
)
from src.ui.design_system import AppColors


class WritingAssistantFletApp:
    """Main Flet application class"""

    def __init__(self, debug: bool = False):
        """
        Initialize the Flet application.

        Args:
            debug: Whether to run in debug mode (passed from main.py after logging setup)
        """
        self.config = ConfigManager()
        # Override DEBUG from config if explicitly passed
        if debug:
            self.config.DEBUG = debug

        # Get logger instance (logging already configured in main.py)
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

        # UI State
        self.sidebar_visible = False
        self.settings_visible = False
        self.hotkey_initial_value = ""

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

        # No AppBar - using floating buttons and navigation rail instead

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

        # Clear existing content
        if self.page.controls:
            self.page.controls.clear()

        if self.settings_visible:
            # Show settings view with rail
            rail = self._create_navigation_rail()
            settings_content = self._create_settings_view()
            self.page.add(
                ft.Row(
                    [rail, ft.VerticalDivider(width=1), settings_content],
                    spacing=0,
                    expand=True,
                )
            )
        else:
            # Show main view with rail and optional sidebar
            rail = self._create_navigation_rail()
            main_content = self._create_main_content()

            # Create layout: rail + optional sidebar + main content
            components = [rail, ft.VerticalDivider(width=1)]
            if self.sidebar_visible:
                sidebar = self._create_sidebar()
                components.append(sidebar)
                components.append(ft.VerticalDivider(width=1))
            components.append(main_content)

            self.page.add(
                ft.Row(
                    components,
                    spacing=0,
                    expand=True,
                )
            )

        self.page.update()

    def _create_navigation_rail(self):
        """Create the permanent navigation rail on the left"""
        return create_navigation_rail(
            dark_mode=self.config.DARK_MODE,
            on_menu_click=self.toggle_sidebar,
            on_settings_click=lambda _: self.toggle_settings_view(),
        )

    def _create_sidebar(self):
        """Create the collapsible sidebar"""
        return create_sidebar(dark_mode=self.config.DARK_MODE)

    def _create_main_content(self):
        """Create the main content area"""
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
            color=AppColors.get_text_primary(self.config.DARK_MODE),
        )

        self.ui_elements["button_main"] = ft.ElevatedButton(
            _("Click me"),
            on_click=self.on_button_click,
        )

        # Floating buttons at top right
        theme_btn = icon_button(
            icon=(ft.Icons.DARK_MODE if not self.config.DARK_MODE else ft.Icons.LIGHT_MODE),
            tooltip="Toggle Dark/Light Mode",
            dark_mode=self.config.DARK_MODE,
            on_click=self.toggle_theme,
        )

        hide_btn = icon_button(
            icon=ft.Icons.VISIBILITY_OFF,
            tooltip=f"Hide ({self.config.HOTKEY_COMBINATION})",
            dark_mode=self.config.DARK_MODE,
            on_click=lambda _: (self.window_manager.hide_window() if self.window_manager else None),
        )

        # Main container with buttons at top
        return ft.Container(
            content=ft.Column(
                [
                    # Buttons row at top right
                    ft.Row(
                        [
                            ft.Container(expand=True),  # Spacer to push buttons right
                            theme_btn,
                            hide_btn,
                        ],
                        spacing=5,
                    ),
                    # Language selector
                    ft.Row([self.ui_elements["language_select"]]),
                    # Main content
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
            expand=True,
            bgcolor=AppColors.get_bg_primary(self.config.DARK_MODE),
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

        # Recreate UI to apply new colors
        self._create_ui()

    def toggle_sidebar(self, e):
        """Toggle sidebar visibility"""
        self.sidebar_visible = not self.sidebar_visible
        self._create_ui()

    def toggle_settings_view(self):
        """Toggle between main view and settings view"""
        self.settings_visible = not self.settings_visible
        self._create_ui()

    def _create_settings_view(self):
        """Create the settings view (full screen)"""
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

        # Hotkey input
        hotkey_input = ft.TextField(
            label=_("Shortcut Key"),
            value=self.config.HOTKEY_COMBINATION,
            hint_text="e.g., ctrl space, ctrl shift a",
            on_blur=self.on_hotkey_blur,
            width=300,
        )

        # Floating buttons at top right
        theme_btn = icon_button(
            icon=(ft.Icons.DARK_MODE if not self.config.DARK_MODE else ft.Icons.LIGHT_MODE),
            tooltip="Toggle Dark/Light Mode",
            dark_mode=self.config.DARK_MODE,
            on_click=self.toggle_theme,
        )

        hide_btn = icon_button(
            icon=ft.Icons.VISIBILITY_OFF,
            tooltip=f"Hide ({self.config.HOTKEY_COMBINATION})",
            dark_mode=self.config.DARK_MODE,
            on_click=lambda _: (self.window_manager.hide_window() if self.window_manager else None),
        )

        return ft.Container(
            content=ft.Column(
                [
                    # Buttons row at top right
                    ft.Row(
                        [
                            ft.Container(expand=True),  # Spacer
                            theme_btn,
                            hide_btn,
                        ],
                        spacing=5,
                    ),
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
                    hotkey_input,
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            expand=True,
            bgcolor=AppColors.get_bg_primary(self.config.DARK_MODE),
        )

    def on_hotkey_blur(self, e):
        """Handle hotkey input blur event with automatic validation"""
        if not self.page or not e.control:
            return

        new_hotkey = e.control.value.strip()

        # Check if value has changed
        if new_hotkey != self.hotkey_initial_value:
            # Validate and normalize the hotkey
            normalized_hotkey = " ".join(new_hotkey.split()) or "ctrl space"

            # Update config
            self.config.HOTKEY_COMBINATION = normalized_hotkey

            # Re-register the hotkey
            self.log.info(f"Hotkey changed to: {normalized_hotkey}")
            if self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)

            # Update the initial value
            self.hotkey_initial_value = normalized_hotkey

            # Show confirmation
            snack_bar = ft.SnackBar(ft.Text(f"Hotkey updated to: {normalized_hotkey}"))
            self.page.open(snack_bar)
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
