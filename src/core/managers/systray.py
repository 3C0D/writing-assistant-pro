"""
Systray Manager for Writing Assistant Pro

Manages the system tray icon and its context menu using pystray.
Provides integration with the Flet application.
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from loguru import logger
from PIL import Image
from pystray import Icon, Menu, MenuItem

from ..enums import EventType
from ..error_handler import UIError, handle_error
from ..event_bus import emit_event, get_event_bus
from ..services.translation import _
from ..utils.paths import get_icon_path
from .autostart import AutostartManager

if TYPE_CHECKING:
    import flet as ft


class SystrayManager:
    """
    Manages the system tray icon and menu for the application.
    """

    def __init__(
        self,
        page: ft.Page,
        on_about: Callable | None = None,
        app: Any | None = None,
    ):
        """
        Initialize the systray manager.

        Args:
            page: The Flet page instance
            on_about: Callback function to show about window
            app: The main application instance (for cleanup)
        """
        self.page = page
        self.on_about = on_about
        self.app = app
        self.icon: Any | None = None
        self._icon_thread: threading.Thread | None = None
        self.log = logger.bind(name="WritingAssistant.SystrayManager")

        # Subscribe to language changes to refresh menu labels
        get_event_bus().on(EventType.LANGUAGE_CHANGED, self._on_language_changed)

    def create_icon(self) -> None:
        """
        Create and display the system tray icon.
        """
        try:
            # Load icon image
            icon_path = get_icon_path()
            if not icon_path.exists():
                self.log.warning(f"Icon not found at {icon_path}, using default")
                image = self._create_default_icon()
            else:
                image = Image.open(icon_path)

            # Create menu
            menu = self._create_menu()

            # Create icon
            self.icon = Icon("WritingAssistantPro", image, "Writing Assistant Pro", menu)

            self.log.info("Systray icon created successfully")

        except Exception as e:
            handle_error(
                e, error_type=UIError, context="systray_create_icon", logger_instance=self.log
            )

    def run(self) -> None:
        """
        Run the systray icon (blocking call).
        Should be called in a separate thread.
        """
        if self.icon is None:
            self.create_icon()

        if self.icon:
            self.log.info("Starting systray icon...")
            self.icon.run()

    def run_async(self) -> None:
        """
        Run the systray icon in a separate thread (non-blocking).
        """
        if self._icon_thread and self._icon_thread.is_alive():
            self.log.warning("Systray icon thread already running")
            return

        self._icon_thread = threading.Thread(target=self.run, daemon=True)
        self._icon_thread.start()
        self.log.info("Systray icon thread started")

    def stop(self) -> None:
        """
        Stop the systray icon.
        """
        if self.icon:
            self.log.info("Stopping systray icon...")
            self.icon.stop()
            self.icon = None

    def _on_language_changed(self, data: dict) -> None:
        """
        Handle language change event.
        Updates the menu labels with the new language.
        """
        self.log.info("Language changed event detected, refreshing systray menu")
        if self.icon:
            # Re-create menu to apply new translations
            self.icon.menu = self._create_menu()
            # Update info text (tooltip) if pystray supports it dynamically
            # For pystray, we often just update the menu
            self.log.debug("Systray menu labels updated")

    def _create_default_icon(self) -> Image.Image:
        """
        Create a simple default icon if the icon file is not found.

        Returns:
            PIL Image object
        """
        # Create a simple 64x64 colored square as fallback
        image = Image.new("RGB", (64, 64), color=(76, 175, 80))
        return image

    def _create_menu(self) -> Any:
        """
        Create the context menu for the systray icon.

        Returns:
            pystray.Menu object
        """
        return Menu(
            MenuItem(_("About"), self._on_about_click),
            MenuItem(_("Settings"), self._on_settings_click),
            Menu.SEPARATOR,
            MenuItem(
                _("Run on Startup"),
                self._on_autostart_click,
                checked=lambda item: AutostartManager.check_autostart(),
            ),
            Menu.SEPARATOR,
            MenuItem(_("Quit"), self._on_quit_click),
        )

    def _on_about_click(self, icon: Any, item: Any) -> None:
        """
        Handle About menu item click.
        """
        self.log.debug("About menu item clicked")
        if self.on_about:
            self.on_about()

    def _on_settings_click(self, icon: Any, item: Any) -> None:
        """
        Handle Settings menu item click.
        Opens the main window with settings view visible.
        """
        self.log.debug("Settings menu item clicked")
        try:
            # Show the window
            if self.page and not self.page.window.visible:
                self.page.window.visible = True
                emit_event(EventType.WINDOW_SHOWN)
            # Not working
            # elif self.page and self.page.window.minimized:
            #     self.page.window.minimized = False
            #     self.page.window.to_front()
            #     self.page.update()

            # Open settings view if app is available
            if self.app and hasattr(self.app, "toggle_settings_view"):
                # Check if settings are already visible in UI state
                settings_visible = False
                if hasattr(self.app, "state") and hasattr(self.app.state, "ui_state"):
                    settings_visible = self.app.state.ui_state.settings_visible

                if not settings_visible:
                    self.app.toggle_settings_view()
        except Exception as e:
            handle_error(
                e, error_type=UIError, context="systray_on_settings_click", logger_instance=self.log
            )

    def _on_autostart_click(self, icon: Any, item: Any) -> None:
        """
        Handle Run on Startup menu item click.
        """
        new_state = not item.checked
        self.log.info(f"Toggling autostart to {new_state}")

        if self.app and hasattr(self.app, "config"):
            success = AutostartManager.set_autostart_with_sync(new_state, self.app.config)
            if success:
                self.log.info("Autostart setting updated successfully")
            else:
                self.log.error("Failed to update autostart setting")
        else:
            self.log.warning("App config not available, setting system autostart only")
            AutostartManager.set_autostart(new_state)

    def _on_quit_click(self, icon: Any, item: Any) -> None:
        """
        Handle Quit menu item click.
        Properly cleanup all resources before exiting.
        """
        self.log.debug("Quit menu item clicked")

        # Cleanup hotkey manager if app is available
        if self.app and hasattr(self.app, "hotkey_manager"):
            self.log.info("Cleaning up hotkey manager...")
            self.app.hotkey_manager.cleanup()

        # Hide Flet window if it exists to avoid orphaned process
        try:
            if self.page and self.page.window:
                self.log.info("Hiding Flet window...")
                self.page.window.visible = False
                self.page.update()
        except Exception as e:
            handle_error(e, context="systray_hide_window_on_quit", logger_instance=self.log)

        # Stop systray icon
        self.stop()

        # Force exit - os._exit avoids SystemExit exception in pystray thread
        self.log.info("Application terminated")
        time.sleep(0.1)  # Give time for logs to flush
        os._exit(0)
