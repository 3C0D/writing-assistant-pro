"""
Window management module for Writing Assistant Pro
Handles window visibility, hotkeys, and window lifecycle
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from loguru import logger


class WindowManager:
    """
    Manages window visibility and hotkey handling
    """

    def __init__(
        self,
        config,
        page=None,
        on_show: Callable[[], None] | None = None,
        on_hide: Callable[[], None] | None = None,
    ):
        self.config = config
        self.page = page  # Flet page reference
        self.on_show = on_show  # Callback when window is shown
        self.on_hide = on_hide  # Callback when window is hidden
        self.log = logger.bind(name="WritingAssistant.WindowManager")
        self.last_trigger_time = 0.0
        self.trigger_lock = threading.Lock()  # Prevent overlapping triggers
        self.window_visible = False

    def set_page(self, page):
        """Set the Flet page reference"""
        self.page = page

    def toggle_window(self) -> None:
        """Toggle window visibility on hotkey press"""

        # Check if lock is already acquired (another hotkey trigger is processing)
        if not self.trigger_lock.acquire(blocking=False):
            self.log.debug("Hotkey already processing, ignoring")
            return

        try:
            # Use monotonic clock to avoid system time shift issues
            current_time = time.monotonic()

            # Debounce check - prevent rapid successive triggers
            time_since_last = current_time - self.last_trigger_time

            if time_since_last < self.config.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return

            self.last_trigger_time = current_time

            # Toggle window visibility based on current state
            self.log.info(f"Toggle window - current state: visible={self.window_visible}")

            if self.window_visible:
                self.hide_window()
            else:
                self.show_window()

        except Exception as e:
            self.log.error(f"Error in toggle_window: {e}")
        finally:
            # Always release the lock to allow future hotkey triggers
            self.trigger_lock.release()

    def show_window(self) -> None:
        """Show the native window"""
        try:
            if self.page:
                self.log.info("Showing window...")

                # Call on_show callback BEFORE showing window
                # This allows capturing selection from the app that currently has focus
                if self.on_show:
                    try:
                        self.on_show()
                    except Exception as e:
                        self.log.error(f"Error in on_show callback: {e}")

                # Flet specific window management
                self.page.window.visible = True
                self.page.window.to_front()
                self.page.update()

                self.window_visible = True
                self.log.info("Window shown")
            else:
                self.log.warning("No Flet page found during show_window")

        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback

            self.log.debug(f"Full traceback: {traceback.format_exc()}")

    def hide_window(self) -> None:
        """Hide the native window"""
        try:
            if self.page:
                self.log.info("Hiding window...")

                # Flet specific window management
                self.page.window.visible = False
                self.page.update()

                self.window_visible = False

                if self.on_hide:
                    try:
                        self.on_hide()
                    except Exception as e:
                        self.log.error(f"Error in on_hide callback: {e}")

                self.log.info("Window hidden - ctrl+space to show")
            else:
                self.log.warning("No Flet page found during hide_window")

        except Exception as e:
            self.log.error(f"Error hiding window: {e}")
