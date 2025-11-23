"""
Systray Manager for Writing Assistant Pro

Manages the system tray icon and its context menu using pystray.
Provides integration with the Flet application.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from PIL import Image
from pystray import Icon, Menu, MenuItem

from ..utils.paths import get_app_root
from .autostart import AutostartManager

if TYPE_CHECKING:
    import flet as ft

logger = logging.getLogger(__name__)


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

    def create_icon(self) -> None:
        """
        Create and display the system tray icon.
        """
        try:
            # Load icon image
            icon_path = self._get_icon_path()
            if not icon_path.exists():
                logger.warning(f"Icon not found at {icon_path}, using default")
                image = self._create_default_icon()
            else:
                image = Image.open(icon_path)

            # Create menu
            menu = self._create_menu()

            # Create icon
            self.icon = Icon("WritingAssistantPro", image, "Writing Assistant Pro", menu)

            logger.info("Systray icon created successfully")

        except Exception as e:
            logger.exception(f"Error creating systray icon: {e}")

    def run(self) -> None:
        """
        Run the systray icon (blocking call).
        Should be called in a separate thread.
        """
        if self.icon is None:
            self.create_icon()

        if self.icon:
            logger.info("Starting systray icon...")
            self.icon.run()

    def run_async(self) -> None:
        """
        Run the systray icon in a separate thread (non-blocking).
        """
        if self._icon_thread and self._icon_thread.is_alive():
            logger.warning("Systray icon thread already running")
            return

        self._icon_thread = threading.Thread(target=self.run, daemon=True)
        self._icon_thread.start()
        logger.info("Systray icon thread started")

    def stop(self) -> None:
        """
        Stop the systray icon.
        """
        if self.icon:
            logger.info("Stopping systray icon...")
            self.icon.stop()
            self.icon = None

    def _get_icon_path(self) -> Path:
        """
        Get the path to the application icon.

        Returns:
            Path to the icon file
        """
        # Use get_app_root() to find the correct root directory in both
        # dev and frozen modes
        app_root = get_app_root()

        # In frozen mode (PyInstaller), assets are usually in the root
        # or _internal
        # In dev mode, they are in src/core/config/icons/

        # Check common locations
        possible_paths = [
            # Dev structure - NEW LOCATION after refactoring
            app_root / "src" / "core" / "config" / "icons" / "app_icon.png",
            # Flat structure (if copied to root during build)
            app_root / "app_icon.png",
            # Old dev structure (fallback)
            app_root / "assets" / "icons" / "app_icon.png",
        ]

        for path in possible_paths:
            if path.exists():
                return path

        # Fallback to dev path relative to this file if get_app_root
        # fails or structure is weird
        project_root = Path(__file__).parent.parent.parent.parent
        return project_root / "src" / "core" / "config" / "icons" / "app_icon.png"

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
            MenuItem("About", self._on_about_click),
            Menu.SEPARATOR,
            MenuItem(
                "Run on Startup",
                self._on_autostart_click,
                checked=lambda item: AutostartManager.check_autostart(),
            ),
            Menu.SEPARATOR,
            MenuItem("Quit", self._on_quit_click),
        )

    def _on_about_click(self, icon: Any, item: Any) -> None:
        """
        Handle About menu item click.
        """
        logger.debug("About menu item clicked")
        if self.on_about:
            self.on_about()

    def _on_autostart_click(self, icon: Any, item: Any) -> None:
        """
        Handle Run on Startup menu item click.
        """
        new_state = not item.checked
        logger.info(f"Toggling autostart to {new_state}")

        if self.app and hasattr(self.app, "config"):
            success = AutostartManager.set_autostart_with_sync(new_state, self.app.config)
            if success:
                logger.info("Autostart setting updated successfully")
            else:
                logger.error("Failed to update autostart setting")
        else:
            logger.warning("App config not available, setting system autostart only")
            AutostartManager.set_autostart(new_state)

    def _on_quit_click(self, icon: Any, item: Any) -> None:
        """
        Handle Quit menu item click.
        Properly cleanup all resources before exiting.
        """
        logger.debug("Quit menu item clicked")

        # Cleanup hotkey manager if app is available
        if self.app and hasattr(self.app, "hotkey_manager"):
            logger.info("Cleaning up hotkey manager...")
            self.app.hotkey_manager.cleanup()

        # Hide Flet window if it exists to avoid orphaned process
        try:
            if self.page and self.page.window:
                logger.info("Hiding Flet window...")
                self.page.window.visible = False
                self.page.update()
        except Exception as e:
            logger.warning(f"Error hiding window: {e}")

        # Stop systray icon
        self.stop()

        # Force exit - os._exit avoids SystemExit exception in pystray thread
        logger.info("Application terminated")
        time.sleep(0.1)  # Give time for logs to flush
        os._exit(0)
