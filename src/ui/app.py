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
from src.core.services.hotkey_capture import format_hotkey_for_display
from src.core.services.input_source import InputSourceService
from src.ui.components import (
    create_navigation_rail,
    create_sidebar,
    icon_button,
)
from src.ui.components.input.attachment_zone import Attachment
from src.ui.components.input.prompt_bar import PromptBar
from src.ui.design_system import AppColors
from src.ui.dialogs import HotkeyDialogResult, show_hotkey_capture_dialog


class WritingAssistantFletApp:
    """Main Flet application class"""

    def __init__(self, debug: bool = False, version: str = "0.0.0"):
        """
        Initialize the Flet application.

        Args:
            debug: Whether to run in debug mode (passed from main.py)
            version: Application version string
        """
        self.config = ConfigManager()
        # Override DEBUG from config if explicitly passed
        if debug:
            self.config.DEBUG = debug

        # Store version
        self.version = version

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
        self.input_source_service: InputSourceService | None = None
        self.window_manager: WindowManager | None = None
        self.page: ft.Page | None = None
        self.systray_manager: SystrayManager | None = None
        self.file_picker: ft.FilePicker | None = None
        self.prompt_bar: PromptBar | None = None

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

        # Initialize WindowManager with page and on_show callback for refreshing inputs
        self.window_manager = WindowManager(self.config, page, on_show=self._on_window_show)

        # Page configuration
        page.title = (
            f"🔥 Writing Assistant Pro v{self.version} (DEV MODE)"
            if self.config.DEBUG
            else f"Writing Assistant Pro v{self.version}"
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

    def _on_window_show(self) -> None:
        """
        Called when window is shown.
        Refreshes input sources to get fresh clipboard/selection data.
        """
        self.log.debug("Window shown - refreshing input sources")
        if self.prompt_bar:
            # Reinitialize input sources and refresh the prompt bar
            self.input_source_service = InputSourceService()
            self.prompt_bar.input_service = self.input_source_service
            self.prompt_bar.attachments = []  # Clear old attachments
            self.prompt_bar._refresh_sources()

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

        # Reinitialize input source service every time main content is created,when window is opened
        # This ensures fresh data from clipboard and other sources
        self.input_source_service = InputSourceService()
        self.log.info("Input source service reinitialized for fresh data")

        # We need a function to handle submission from the PromptBar
        def handle_submit(text, attachments, sources):
            self.log.info(f"Submit: {text} | Attachments: {len(attachments)} | Sources: {sources}")
            # Here we would send to AI core...
            # For now, just show a snackbar confirmation
            if self.page:
                self.page.open(ft.SnackBar(content=ft.Text(f"Sent: {text}"), action="Undo"))

        # Initialize File Picker first (before prompt_bar)
        def handle_file_result(e: ft.FilePickerResultEvent):
            if e.files and self.prompt_bar:
                new_attachments = []
                for f in e.files:
                    # Convert flet FilePickerResultEvent file to Attachment
                    import uuid

                    att = Attachment(
                        id=str(uuid.uuid4()),
                        type="file",
                        content=f.path,
                        name=f.name,
                        size=str(f.size),
                    )
                    new_attachments.append(att)

                if new_attachments:
                    self.prompt_bar.add_attachments(new_attachments)

        # Create file_picker only once to avoid duplicates in overlay
        if not self.file_picker:
            self.file_picker = ft.FilePicker(on_result=handle_file_result)
            if self.page:
                self.page.overlay.append(self.file_picker)
                self.page.update()

        # Function to trigger file picker
        def trigger_file_picker():
            if self.file_picker:
                self.file_picker.pick_files(
                    allow_multiple=True, dialog_title="Sélectionner des fichiers"
                )

        # Create PromptBar
        self.prompt_bar = PromptBar(
            input_service=self.input_source_service,
            on_submit=handle_submit,
            on_attach_click=trigger_file_picker,
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

        # Main container
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
                    # Spacer to push prompt to center (vertically)
                    ft.Container(expand=True),
                    # Prompt Bar Area
                    ft.Container(
                        content=self.prompt_bar,
                        width=700,  # Constrain width for aesthetic centering
                    ),
                    # Bottom spacer (smaller than top one usually, or equal for true center)
                    ft.Container(expand=True),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
            bgcolor=AppColors.get_bg_primary(self.config.DARK_MODE),
        )

    def on_language_change(self, e):
        """Language change handler"""
        if not self.page:
            return

        new_lang = e.control.value
        change_language(new_lang)

        # Recreate UI to apply new language everywhere
        self._create_ui()

        snack_bar = ft.SnackBar(ft.Text(f"Language changed to {new_lang}"))
        self.page.open(snack_bar)

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

        # Hotkey display (clickable to edit)
        hotkey_display = self._create_hotkey_display()

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
                    hotkey_display,
                    ft.Container(height=20),
                    # Check for updates button
                    ft.ElevatedButton(
                        text=_("Check for Updates"),
                        icon=ft.Icons.SYSTEM_UPDATE,
                        on_click=self.on_check_updates,
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
                self.log.info("Cancel: re-registering original hotkey")
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
        old_hotkey = self.config.HOTKEY_COMBINATION
        self.config.HOTKEY_COMBINATION = new_hotkey or ""

        # Re-register the hotkey (or unregister if None)
        if new_hotkey:
            self.log.info(f"Hotkey changed: {old_hotkey} -> {new_hotkey}")
            if self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
        else:
            self.log.info(f"Hotkey disabled (was: {old_hotkey})")
            # Already unregistered when dialog opened, no need to unregister again

        # Refresh UI to show new hotkey
        self._create_ui()

        # Show confirmation
        if self.page:
            display = format_hotkey_for_display(new_hotkey) if new_hotkey else "None"
            snack_bar = ft.SnackBar(ft.Text(f"Hotkey: {display}"))
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

    def on_check_updates(self, e):
        """Handle check for updates button click"""
        if not self.page:
            return

        from src.core.services.updater import check_for_updates
        from src.ui.dialogs import (
            show_no_update_dialog,
            show_update_dialog,
            show_update_error_dialog,
        )

        # Show loading indication
        self.log.info("Checking for updates...")

        result = check_for_updates()

        if "error" in result:
            show_update_error_dialog(self.page, str(result.get("error", "")), self.config.DARK_MODE)
        elif result.get("available"):
            show_update_dialog(self.page, result, self.config.DARK_MODE)
        else:
            show_no_update_dialog(self.page, self.config.DARK_MODE)
