"""
Main Flet application for Writing Assistant Pro
"""

from __future__ import annotations

import flet as ft
from loguru import logger

from src.core import (
    AppState,
    ConfigManager,
    EventType,
    HotkeyManager,
    UIState,
    WindowManager,
    _,
    emit_event,
    get_event_bus,
    get_icon_path,
    init_translation,
)
from src.core.managers.systray import SystrayManager
from src.core.services.input_source import InputSourceService, InputState
from src.core.services.updater import check_for_updates
from src.ui.components import (
    RAIL_WIDTH,
    create_navigation_rail,
    create_sidebar,
)
from src.ui.components.input.prompt_bar import PromptBar
from src.ui.dialogs import (
    show_no_update_dialog,
    show_update_dialog,
    show_update_error_dialog,
)
from src.ui.services.file_handler import process_picked_files
from src.ui.views import SettingsView, create_about_view, create_main_content


class WritingAssistantFletApp:
    """Main Flet application class"""

    def __init__(self, debug: bool = False, version: str = "0.0.0"):
        """
        Initialize the Flet application.

        Args:
            debug: Whether to run in debug mode (passed from main.py)
            version: Application version string
        """
        self.state = AppState(config=ConfigManager(), input_state=InputState(), ui_state=UIState())
        self.event_bus = get_event_bus()

        # Override DEBUG from config if explicitly passed
        if debug:
            self.state.config.DEBUG = debug

        # Store version
        self.version = version

        # Get logger instance (logging already configured in main.py)
        self.log = logger.bind(name="WritingAssistant.FletApp")

        # Initialize translation
        init_translation(
            "writing_assistant",
            "translations",
            self.state.config.LANGUAGE,
            self.state.config.AVAILABLE_LANGUAGES,
        )

        self.hotkey_manager = HotkeyManager(self.state.config)
        self.input_source_service = InputSourceService(self.state.input_state)
        self.window_manager: WindowManager | None = None
        self.page: ft.Page | None = None
        self.file_picker: ft.FilePicker | None = None
        self.prompt_bar: PromptBar | None = None

        # Persistent view contents
        self.main_content_container: ft.Container | None = None
        self.settings_content_container: ft.Container | None = None
        self.navigation_rail: ft.Container | None = None

        # Initial hotkey value for settings change detection
        self.hotkey_initial_value = ""

        # Setup event listeners
        self._setup_event_listeners()

    def show_snack_bar(self, text: str, action: str | None = None) -> None:
        """
        Show a snack bar with consistent styling and positioning.
        Includes a left margin to avoid overlapping the navigation rail.
        """
        if not self.page:
            return

        # Use RAIL_WIDTH + divider width (1)
        margin_left = RAIL_WIDTH + 1

        snack_bar = ft.SnackBar(
            content=ft.Text(text),
            action=action,
            margin=ft.margin.only(left=margin_left, bottom=10, right=10),
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        self.page.open(snack_bar)

    def main(self, page: ft.Page):
        """Main Flet page setup"""
        self.page = page
        self.log.info("Flet application starting...")

        # Initialize WindowManager with page
        self.window_manager = WindowManager(
            self.state.config,
            page,
        )

        # Page configuration
        self._update_window_title()
        page.window.width = 800
        page.window.height = 600
        # Set both for compatibility: page.window.icon is the new way,
        # but windowIcon is the internal attribute Flet uses
        icon_path = str(get_icon_path())
        self.log.info(f"Setting window icon: {icon_path}")
        page.window.icon = icon_path
        page._set_attr("windowIcon", icon_path)
        page.theme_mode = ft.ThemeMode.DARK if self.state.config.DARK_MODE else ft.ThemeMode.LIGHT
        page.padding = 0

        # Prevent app from closing when window is closed (hide instead)
        page.window.prevent_close = True
        page.window.on_event = self.on_window_event

        # Hide window on start (systray mode)
        page.window.visible = False

        # No AppBar - using floating buttons and navigation rail instead

        # Create UI
        self._create_ui()

        # Setup file picker
        self._setup_file_picker()

        # Setup hotkey for toggle with logging
        self.log.info(f"Registering hotkey: {self.state.config.HOTKEY_COMBINATION}")
        self.hotkey_manager.register_delayed(self.window_manager.toggle_window)

        # Initialize and start systray
        self.systray_manager = SystrayManager(page, on_about=self.show_about, app=self)
        self.systray_manager.run_async()
        self.log.info("Systray manager started")

        page.update()
        self.log.info("Flet application started")

    def _setup_event_listeners(self) -> None:
        """Setup subscribers for the event bus"""
        bus = self.event_bus
        bus.on(EventType.LANGUAGE_CHANGED, self._handle_language_change_event)
        bus.on(EventType.UPDATE_AVAILABLE, self._handle_update_available_event)
        bus.on(EventType.UPDATE_ERROR, self._handle_update_error_event)
        bus.on(EventType.WINDOW_SHOWN, self._handle_window_show_event)
        bus.on(EventType.WINDOW_HIDDEN, self._handle_window_hide_event)
        self.log.debug("Event bus subscribers initialized")

    def _handle_window_show_event(self, data: dict | None = None) -> None:
        """Called when window is shown via Event Bus"""
        self.log.debug("Event: Window shown - refreshing input sources")
        # Logic for refreshing input sources is now in PromptBar itself (autonomous)
        # We can add global app logic here if needed.

    def _handle_window_hide_event(self, data: dict | None = None) -> None:
        """Called when window is hidden via Event Bus"""
        if self.state.ui_state.settings_visible or self.state.ui_state.about_visible:
            self.log.debug("Event: Window hidden - resetting to main view")
            self.state.ui_state.settings_visible = False
            self.state.ui_state.about_visible = False
            self._create_ui()

    def _handle_language_change_event(self, data: dict) -> None:
        """Handle language change event from any source"""
        language = data.get("language", "en")
        self.log.info(f"Event: Language changed to {language}")
        # Reset cached container to force recreation with new translations
        self.main_content_container = None
        # Recreate UI to apply new language everywhere
        self._create_ui()

    def _handle_update_available_event(self, data: dict) -> None:
        """Handle update available event"""
        self.log.info(f"Event: Update available - {data.get('version')}")
        # Note: We don't automatically show dialog here to avoid interrupting user,
        # but we could update a status indicator in the UI.

    def _handle_update_error_event(self, data: dict) -> None:
        """Handle update check error event"""
        self.log.warning(f"Event: Update check failed - {data.get('error')}")

    def on_window_event(self, e):
        """Handle window events"""
        if e.data == "close" and self.window_manager:
            self.window_manager.hide_window()

    def _create_ui(self):
        """Create or update the user interface"""
        if not self.page:
            return

        # Update Window title and Navigation Rail (depends on theme/language)
        self._update_window_title()
        self.navigation_rail = self._create_navigation_rail()

        # Clear existing content if any
        if self.page.controls:
            self.page.controls.clear()

        if self.state.ui_state.about_visible:
            # Show about view (full screen, no rail)
            about_content = self._create_about_view()
            self.page.add(about_content)
        elif self.state.ui_state.settings_visible:
            # Show settings view with rail
            # Settings view is usually recreated as it depends on current config values
            # but we can also optimize it if needed. For now just recreate content.
            settings_content = self._create_settings_view()
            self.page.add(
                ft.Row(
                    [self.navigation_rail, ft.VerticalDivider(width=1), settings_content],
                    spacing=0,
                    expand=True,
                )
            )
        else:
            # Show main view with rail and optional sidebar
            # Reuse main_content_container if it exists to preserve state
            if not self.main_content_container:
                self.main_content_container = self._create_main_content()

            # Ensure prompt_bar inner state is correct for current theme
            # (colors might need updating if they are not using dynamic system)
            # Most components use AppColors which should react if we trigger update

            # Create layout: rail + optional sidebar + main content
            components = [self.navigation_rail, ft.VerticalDivider(width=1)]
            if self.state.ui_state.sidebar_visible:
                sidebar = self._create_sidebar()
                components.append(sidebar)
                components.append(ft.VerticalDivider(width=1))
            components.append(self.main_content_container)

            self.page.add(
                ft.Row(
                    components,
                    spacing=0,
                    expand=True,
                )
            )

        self.page.update()
        self.log.debug("UI updated/recreated")

    def _update_window_title(self) -> None:
        """Update the window title with current language/mode."""
        if not self.page:
            return

        title = (
            f"Writing Assistant Pro v{self.version} ({_('DEV MODE')})"
            if self.state.config.DEBUG
            else f"Writing Assistant Pro v{self.version}"
        )
        self.page.title = title
        self.page.update()

    def _setup_file_picker(self):
        """Initialize and setup the file picker"""

        def handle_file_result(e: ft.FilePickerResultEvent):
            if e.files and self.prompt_bar:
                new_attachments = process_picked_files(e.files)
                if new_attachments:
                    self.prompt_bar.add_attachments(new_attachments)

        self.file_picker = ft.FilePicker(on_result=handle_file_result)
        if self.page:
            self.page.overlay.append(self.file_picker)
            self.page.update()

    def _trigger_file_picker(self, e=None):
        """Trigger the file picker dialog"""
        if self.file_picker:
            self.file_picker.pick_files(allow_multiple=True, dialog_title=_("Select files"))

    def _create_navigation_rail(self):
        """Create the permanent navigation rail on the left"""
        return create_navigation_rail(
            dark_mode=self.state.config.DARK_MODE,
            on_menu_click=self.toggle_sidebar,
            on_settings_click=lambda _: self.toggle_settings_view(),
            show_menu=not self.state.ui_state.settings_visible,
        )

    def _create_sidebar(self):
        """Create the collapsible sidebar"""
        return create_sidebar(dark_mode=self.state.config.DARK_MODE)

    def _create_main_content(self):
        """Create the main content area"""

        # We need a function to handle submission from the PromptBar
        def handle_submit(text, attachments, sources):
            self.log.info(f"Submit: {text} | Attachments: {len(attachments)} | Sources: {sources}")
            # Here we would send to AI core...
            # For now, just show a snackbar confirmation
            if self.page:
                self.show_snack_bar(_("Sent: {text}").format(text=text), action=_("Undo"))

        # Create PromptBar if it doesn't exist
        if not self.prompt_bar:
            self.prompt_bar = PromptBar(
                input_service=self.input_source_service,
                on_submit=handle_submit,
                on_attach_click=self._trigger_file_picker,
            )

        return create_main_content(
            prompt_bar=self.prompt_bar,
            dark_mode=self.state.config.DARK_MODE,
            hotkey_combination=self.state.config.HOTKEY_COMBINATION,
            on_theme_toggle=lambda e: self.toggle_theme(e),
            on_hide_click=lambda e: (
                self.window_manager.hide_window() if self.window_manager else None
            ),
        )

    def toggle_theme(self, e):
        """Toggle dark/light theme"""
        if not self.page:
            return

        new_dark_mode = not self.state.config.DARK_MODE
        self.state.config.DARK_MODE = new_dark_mode
        self.page.theme_mode = ft.ThemeMode.DARK if new_dark_mode else ft.ThemeMode.LIGHT

        # Reset cached container to force recreation with new theme colors
        self.main_content_container = None

        # Update prompt bar theme if it exists (to preserve text state)
        if self.prompt_bar:
            self.prompt_bar.update_theme(new_dark_mode)

        # Recreate UI to apply new colors
        self._create_ui()

    def toggle_sidebar(self, e):
        """Toggle sidebar visibility"""
        self.state.ui_state.sidebar_visible = not self.state.ui_state.sidebar_visible
        self._create_ui()

    def toggle_settings_view(self):
        """Toggle between main view and settings view"""
        self.state.ui_state.settings_visible = not self.state.ui_state.settings_visible
        self.state.ui_state.about_visible = False
        self._create_ui()

    def toggle_about_view(self):
        """Toggle between main view and about view"""
        self.state.ui_state.about_visible = not self.state.ui_state.about_visible
        self.state.ui_state.settings_visible = False
        self._create_ui()

    def _create_settings_view(self):
        """Create the settings view (full screen)"""
        if not self.page:
            return ft.Container()

        settings_view = SettingsView(
            config=self.state.config,
            hotkey_manager=self.hotkey_manager,
            window_manager=self.window_manager,
            page=self.page,
            on_theme_toggle=lambda e: self.toggle_theme(e),
            on_ui_refresh=self._create_ui,
            on_show_snackbar=self.show_snack_bar,
            on_check_updates=self.on_check_updates,
        )
        return settings_view.build()

    def _create_about_view(self):
        """Create the about view (full screen)"""
        return create_about_view(
            version=self.version,
            dark_mode=self.state.config.DARK_MODE,
            hotkey_combination=self.state.config.HOTKEY_COMBINATION,
            on_theme_toggle=lambda e: self.toggle_theme(e),
            on_hide_click=lambda e: (
                self.window_manager.hide_window() if self.window_manager else None
            ),
            on_close_click=lambda e: self.toggle_about_view(),
            on_link_click=lambda url: self.page.launch_url(url) if self.page else None,
        )

    def show_about(self, e=None):
        """Show about window"""
        if not self.page:
            return

        self.log.info("About window requested")
        self.state.ui_state.about_visible = True
        self.state.ui_state.settings_visible = False
        self.page.window.visible = True

        # Sync window manager state
        if self.window_manager:
            self.window_manager.window_visible = True

        emit_event(EventType.WINDOW_SHOWN)
        self._create_ui()

    def on_check_updates(self, e):
        """Handle check for updates button click"""
        if not self.page:
            return

        # Show loading indication
        self.log.info("Checking for updates...")

        result = check_for_updates()

        if "error" in result:
            show_update_error_dialog(
                self.page, str(result.get("error", "")), self.state.config.DARK_MODE
            )
        elif result.get("available"):
            show_update_dialog(self.page, result, self.state.config.DARK_MODE)
        else:
            show_no_update_dialog(self.page, self.state.config.DARK_MODE)
