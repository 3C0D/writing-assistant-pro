"""
Window management module for Writing Assistant Pro
Handles window visibility, hotkeys, and window lifecycle
"""

from __future__ import annotations

import threading
import time

from loguru import logger

from ..enums import EventType
from ..error_handler import UIError, handle_error
from ..event_bus import emit_event


class WindowManager:
    """
    Manages window visibility and hotkey handling
    """

    def __init__(
        self,
        config,
        page,
    ):
        self.config = config
        self.page = page  # Flet page reference
        self.log = logger.bind(name="WritingAssistant.WindowManager")
        self.last_trigger_time = 0.0
        self.trigger_lock = threading.Lock()  # Prevent overlapping triggers
        self.window_visible = False

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

            if self.window_visible and self.page:
                if not self.page.window.minimized:
                    self.hide_window()
                else:
                    self.page.window.minimized = False
                    self.page.window.to_front()
                    self.page.update()
            else:
                self.show_window()

        except Exception as e:
            handle_error(e, error_type=UIError, context="toggle_window", logger_instance=self.log)
        finally:
            # Always release the lock to allow future hotkey triggers
            self.trigger_lock.release()

    def show_window(self) -> None:
        """Show the native window"""
        try:
            if self.page:
                self.log.info("Showing window...")

                # Emit PRE_SHOW event BEFORE taking focus - allows selection capture
                emit_event(EventType.WINDOW_PRE_SHOW)

                # Flet specific window management
                self.page.window.visible = True
                self.page.window.to_front()
                self.page.update()

                self.window_visible = True
                self.log.info("Window shown")

                # Emit event for window shown (AFTER focus)
                emit_event(EventType.WINDOW_SHOWN)
            else:
                self.log.warning("No Flet page found during show_window")

        except Exception as e:
            handle_error(e, error_type=UIError, context="show_window", logger_instance=self.log)

    def hide_window(self) -> None:
        """Hide the native window"""
        try:
            if self.page:
                self.log.info("Hiding window...")

                # Flet specific window management
                self.page.window.visible = False
                self.page.update()

                self.window_visible = False

                self.log.info("Window hidden - ctrl+space to show")

                # Emit event for window hidden
                emit_event(EventType.WINDOW_HIDDEN)
            else:
                self.log.warning(" No Flet page found during hide_window")

        except Exception as e:
            handle_error(e, error_type=UIError, context="hide_window", logger_instance=self.log)
