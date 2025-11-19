"""
Window management module for Writing Assistant Pro
Handles window visibility, hotkeys, and window lifecycle
"""

import threading
import time

import webview
from loguru import logger


class WindowManager:
    """
    Manages window visibility and hotkey handling
    """

    def __init__(self, config):
        self.config = config
        self.log = logger.bind(name="WritingAssistant.WindowManager")
        self.last_trigger_time = 0.0
        self.trigger_lock = threading.Lock()  # Prevent overlapping triggers
        self.window_ref = None
        self.window_visible = False
        self.window_initialized = False  # to register close handler only once
        self._startup_hide_thread = None  # Thread for startup hide functionality

    def configure_native_window(self, app):
        """
        Configure native window arguments before UI creation

        Args:
            app: NiceGUI app instance
        """
        app.native.window_args["resizable"] = self.config.WINDOW_RESIZABLE
        app.native.window_args["frameless"] = self.config.WINDOW_FRAMELESS
        # Start hidden if configured
        if self.config.WINDOW_START_HIDDEN:
            app.native.window_args["hidden"] = True

        app.native.start_args["debug"] = False
        self.log.debug(
            f"Native window configured: resizable={self.config.WINDOW_RESIZABLE}, "
            f"frameless={self.config.WINDOW_FRAMELESS}, "
            f"hidden={self.config.WINDOW_START_HIDDEN}"
        )

    def get_window(self) -> webview.Window | None:
        """
        Retrieve the webview window instance with retries.

        Returns:
            webview.Window: The window instance or None if not found
        """
        if self.window_ref:
            return self.window_ref

        # Try to find window in webview.windows
        if webview.windows:
            self.window_ref = webview.windows[0]
            return self.window_ref

        return None

    def on_closing(self) -> bool:
        """
        Handle window close event - hide instead of closing
        This prevents the window from being destroyed
        """

        def hide_in_thread():
            self.log.info("Window close requested - hiding instead")
            try:
                self.hide_window()
            except Exception as e:
                self.log.error(f"Error hiding window: {e}")

        # Hide in a separate thread to avoid blocking
        threading.Thread(target=hide_in_thread, daemon=True).start()

        # Return False to prevent actual closing
        return False

    def toggle_window(self) -> None:
        """Toggle window visibility on hotkey press"""
        # Try to acquire lock without blocking
        if not self.trigger_lock.acquire(blocking=False):
            self.log.debug("Hotkey already processing, ignoring")
            return

        try:
            current_time = time.time()

            # Debounce check
            time_since_last = current_time - self.last_trigger_time
            if time_since_last < self.config.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return

            self.last_trigger_time = current_time

            # Simple toggle based on current state
            self.log.info(f"Toggle window - current state: visible={self.window_visible}")

            if self.window_visible:
                self.hide_window()
            else:
                self.show_window()

        except Exception as e:
            self.log.error(f"Error in toggle_window: {e}")
        finally:
            self.trigger_lock.release()

    def show_window(self) -> None:
        """Show the native window"""
        try:
            window = self.get_window()
            if window:
                # Register close handler only once
                if not self.window_initialized:
                    window.events.closing += self.on_closing
                    self.window_initialized = True
                    self.log.info("Window close handler registered")

                self.log.info("Showing window...")

                # Restore if minimized (though hide usually just hides)
                window.restore()
                window.show()

                # Set window always on top
                try:
                    window.on_top = True  # Set on top
                    self.log.info("Window shown - set to always on top")
                except Exception as e:
                    self.log.warning(f"Could not set window on top: {e}")

                self.window_visible = True
            else:
                self.log.warning("No webview window found during show_window")

        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback

            self.log.debug(f"Full traceback: {traceback.format_exc()}")

    def hide_window(self) -> None:
        """Hide the native window"""
        try:
            window = self.get_window()
            if window:
                self.log.info("Hiding window...")
                window.hide()
                self.window_visible = False
                self.log.info("Window hidden - ctrl+. to show")
            else:
                self.log.warning("No webview window found during hide_window")

        except Exception as e:
            self.log.error(f"Error hiding window: {e}")
