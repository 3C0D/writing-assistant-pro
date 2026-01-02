"""
Main Flet application for Writing Assistant Pro
"""

from __future__ import annotations

import flet as ft
from loguru import logger

from src.core import (
    AppState,
    AttachmentType,
    ConfigManager,
    EventType,
    HotkeyManager,
    UIState,
    WindowManager,
    _,
    change_language,
    get_current_language,
    get_event_bus,
    get_icon_path,
    get_language_manager,
    init_translation,
)
from src.core.managers.systray import SystrayManager
from src.core.services.hotkey_capture import format_hotkey_for_display
from src.core.services.input_source import InputSourceService, InputState
from src.ui.components import (
    RAIL_WIDTH,
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
        self.state = AppState(
            config=ConfigManager(),
            input_state=InputState(),
            ui_state=UIState(),
            attachments=[],
        )
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

        # UI Elements references for updates
        self.ui_elements = {}

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
        page.title = (
            f"Writing Assistant Pro v{self.version} (DEV MODE)"
            if self.state.config.DEBUG
            else f"Writing Assistant Pro v{self.version}"
        )
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
        if self.state.ui_state.settings_visible:
            self.log.debug("Event: Window hidden - resetting to main view")
            self.state.ui_state.settings_visible = False
            self._create_ui()

    def _handle_language_change_event(self, data: dict) -> None:
        """Handle language change event from any source"""
        language = data.get("language", "en")
        self.log.info(f"Event: Language changed to {language}")
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

        # Initialize File Picker once if not exists
        if not self.file_picker:
            self._setup_file_picker()

        # Update Navigation Rail (depends on theme)
        self.navigation_rail = self._create_navigation_rail()

        # Clear existing content if any
        if self.page.controls:
            self.page.controls.clear()

        if self.state.ui_state.settings_visible:
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

    def _setup_file_picker(self):
        """Initialize and setup the file picker"""

        def handle_file_result(e: ft.FilePickerResultEvent):
            if e.files and self.prompt_bar:
                new_attachments = []
                import uuid

                from PIL import Image

                from src.ui.components.input.prompt_bar import PromptBar

                IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"}
                TEXT_EXT = {
                    ".txt",
                    ".md",
                    ".py",
                    ".js",
                    ".ts",
                    ".html",
                    ".css",
                    ".json",
                    ".xml",
                    ".yaml",
                    ".toml",
                    ".c",
                    ".cpp",
                    ".h",
                }

                for f in e.files:
                    if not f.path:
                        continue

                    if not PromptBar.is_file_supported(f.name):
                        self.log.warning(f"Skipping unsupported file: {f.name}")
                        continue

                    ext = f.path.lower()[f.path.rfind(".") :] if "." in f.path else ""

                    try:
                        if ext in IMAGE_EXT:
                            img = Image.open(f.path)
                            att_type = AttachmentType.IMAGE
                            content = img
                        elif ext in TEXT_EXT:
                            with open(f.path, encoding="utf-8", errors="ignore") as file:
                                content = file.read()
                            att_type = AttachmentType.TEXT
                        else:
                            att_type = AttachmentType.FILE
                            content = f.path

                        att = Attachment(
                            id=str(uuid.uuid4()),
                            type=att_type,
                            content=content,
                            name=f.name,
                            size=str(f.size),
                        )
                        new_attachments.append(att)
                    except Exception as ex:
                        self.log.error(f"Error loading file {f.name}: {ex}")

                if new_attachments:
                    self.prompt_bar.add_attachments(new_attachments)

        self.file_picker = ft.FilePicker(on_result=handle_file_result)
        if self.page:
            self.page.overlay.append(self.file_picker)
            self.page.update()

    def _trigger_file_picker(self, e=None):
        """Trigger the file picker dialog"""
        if self.file_picker:
            self.file_picker.pick_files(
                allow_multiple=True, dialog_title="Sélectionner des fichiers"
            )

    def _create_navigation_rail(self):
        """Create the permanent navigation rail on the left"""
        return create_navigation_rail(
            dark_mode=self.state.config.DARK_MODE,
            on_menu_click=self.toggle_sidebar,
            on_settings_click=lambda _: self.toggle_settings_view(),
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
                self.show_snack_bar(f"Sent: {text}", action="Undo")

        # Create PromptBar if it doesn't exist
        if not self.prompt_bar:
            self.prompt_bar = PromptBar(
                input_service=self.input_source_service,
                on_submit=handle_submit,
                on_attach_click=self._trigger_file_picker,
            )

        # Floating buttons at top right
        theme_btn = icon_button(
            icon=(ft.Icons.DARK_MODE if not self.state.config.DARK_MODE else ft.Icons.LIGHT_MODE),
            tooltip="Toggle Dark/Light Mode",
            dark_mode=self.state.config.DARK_MODE,
            on_click=self.toggle_theme,
        )

        hide_btn = icon_button(
            icon=ft.Icons.VISIBILITY_OFF,
            tooltip=f"Hide ({self.state.config.HOTKEY_COMBINATION})",
            dark_mode=self.state.config.DARK_MODE,
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
            bgcolor=AppColors.get_bg_primary(self.state.config.DARK_MODE),
        )

    def on_language_change(self, e):
        """Language change handler"""
        if not self.page:
            return

        new_lang = e.control.value
        change_language(new_lang)

        # UI recreation is now handled by the event listener for EventType.LANGUAGE_CHANGED

        self.show_snack_bar(f"Language changed to {new_lang}")

    def toggle_theme(self, e):
        """Toggle dark/light theme"""
        if not self.page:
            return

        new_dark_mode = not self.state.config.DARK_MODE
        self.state.config.DARK_MODE = new_dark_mode
        self.page.theme_mode = ft.ThemeMode.DARK if new_dark_mode else ft.ThemeMode.LIGHT

        # Recreate UI to apply new colors
        self._create_ui()

    def toggle_sidebar(self, e):
        """Toggle sidebar visibility"""
        self.state.ui_state.sidebar_visible = not self.state.ui_state.sidebar_visible
        self._create_ui()

    def toggle_settings_view(self):
        """Toggle between main view and settings view"""
        self.state.ui_state.settings_visible = not self.state.ui_state.settings_visible
        self._create_ui()

    def _create_settings_view(self):
        """Create the settings view (full screen)"""
        # Store initial hotkey value for change detection
        self.hotkey_initial_value = self.state.config.HOTKEY_COMBINATION

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
            icon=(ft.Icons.DARK_MODE if not self.state.config.DARK_MODE else ft.Icons.LIGHT_MODE),
            tooltip="Toggle Dark/Light Mode",
            dark_mode=self.state.config.DARK_MODE,
            on_click=self.toggle_theme,
        )

        hide_btn = icon_button(
            icon=ft.Icons.VISIBILITY_OFF,
            tooltip=f"Hide ({self.state.config.HOTKEY_COMBINATION})",
            dark_mode=self.state.config.DARK_MODE,
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
                        color=AppColors.get_text_primary(self.state.config.DARK_MODE),
                    ),
                    ft.Divider(),
                    ft.Text(
                        _("General"),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.get_text_primary(self.state.config.DARK_MODE),
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
            bgcolor=AppColors.get_bg_primary(self.state.config.DARK_MODE),
        )

    def _create_hotkey_display(self) -> ft.Container:
        """Create clickable hotkey display that opens capture dialog."""
        current_hotkey = self.state.config.HOTKEY_COMBINATION
        display_text = format_hotkey_for_display(current_hotkey)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        _("Shortcut Key"),
                        size=12,
                        color=AppColors.get_text_secondary(self.state.config.DARK_MODE),
                    ),
                    ft.Container(
                        content=ft.Text(
                            display_text,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.get_text_primary(self.state.config.DARK_MODE),
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                        border_radius=8,
                        bgcolor=AppColors.get_bg_secondary(self.state.config.DARK_MODE),
                        border=ft.border.all(
                            1, AppColors.get_text_secondary(self.state.config.DARK_MODE)
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
            current_hotkey=self.state.config.HOTKEY_COMBINATION,
            dark_mode=self.state.config.DARK_MODE,
            on_result=self._on_hotkey_dialog_result,
            hotkey_manager=self.hotkey_manager,
        )

    def _on_hotkey_dialog_result(self, result: HotkeyDialogResult) -> None:
        """Handle result from hotkey capture dialog."""
        if result.action == "cancel":
            # Re-register the original hotkey (was unregistered when dialog opened)
            if self.state.config.HOTKEY_COMBINATION and self.window_manager:
                self.log.info("Cancel: re-registering original hotkey")
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        if result.action == "save":
            new_hotkey = result.hotkey
        else:
            # Unknown action, just re-register original
            if self.state.config.HOTKEY_COMBINATION and self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        # Update config
        old_hotkey = self.state.config.HOTKEY_COMBINATION
        self.state.config.HOTKEY_COMBINATION = new_hotkey or ""

        # Re-register the hotkey (or unregister if None)
        if new_hotkey:
            self.log.info(f"Hotkey changed: {old_hotkey} -> {new_hotkey}")
            if self.window_manager:
                self.hotkey_manager.reregister(self.window_manager.toggle_window)
        else:
            self.log.info(f"Hotkey disabled (was: {old_hotkey})")
            # Already unregistered when dialog opened, no need to unregister again

        # Refresh UI to show new hotkey
        self._create_ui()

        # Show confirmation
        if self.page:
            display = format_hotkey_for_display(new_hotkey) if new_hotkey else "None"
            self.show_snack_bar(f"Hotkey: {display}")
            self.page.update()

    def show_about(self):
        """Show about window (placeholder for now)"""
        if not self.page:
            return

        self.log.info("About window requested (not implemented yet)")
        # Show window and display a simple message
        self.page.window.visible = True
        self.show_snack_bar(_("About window - Coming soon!"))
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
            show_update_error_dialog(
                self.page, str(result.get("error", "")), self.state.config.DARK_MODE
            )
        elif result.get("available"):
            show_update_dialog(self.page, result, self.state.config.DARK_MODE)
        else:
            show_no_update_dialog(self.page, self.state.config.DARK_MODE)
