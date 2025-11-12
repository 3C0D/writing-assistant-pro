"""
Window management module for Writing Assistant Pro
Handles window visibility, hotkeys, and window lifecycle
"""

import threading
import time
import logging
import webview


class WindowManager:
    """
    Manages window visibility and hotkey handling
    """

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger("WritingAssistant.WindowManager")
        self.last_trigger_time = 0.0
        self.trigger_lock = threading.Lock()  # prevent overlapping triggers. not locked!
        self.window_ref = None
        self.window_visible = False
        self.window_initialized = False  # to register close handler only once

    def on_closing(self):
        """
        Handle window close event - hide instead of closing
        This prevents the window from being destroyed
        """
        def hide_in_thread():
            self.log.info("Window close requested - hiding instead")
            try:
                if self.window_ref:
                    self.window_ref.hide()  # not destroyed
                    self.window_visible = False  # Update state
                    self.log.info("Window hidden - Press Ctrl+Space to show again")
            except Exception as e:
                self.log.error(f"Error hiding window: {e}")

        # Hide in a separate thread to avoid blocking
        threading.Thread(target=hide_in_thread, daemon=True).start()

        # Return False to prevent actual closing
        return False

    def toggle_window(self):
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

    def show_window(self):
        """Show the native window"""
        try:
            if webview.windows:
                window = webview.windows[0]

                # Always store/update the reference to window
                self.window_ref = window

                # Register close handler only once
                if not self.window_initialized:
                    window.events.closing += self.on_closing
                    self.window_initialized = True
                    self.log.info("Window close handler registered")

                self.log.info("Showing window...")
                window.show()

                # Set window always on top
                try:
                    # Force window to front and on top
                    window.show()  # Ensure it's shown
                    window.on_top = True  # Set on top
                    self.log.info("Window shown - set to always on top")
                except Exception as e:
                    self.log.warning(f"Could not set window on top: {e}")
                    self.log.info("Window shown - Check your screen")

                self.window_visible = True
            else:
                self.log.warning("No webview window found")

        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")

    def hide_window(self):
        """Hide the native window"""
        try:
            if webview.windows:
                window = webview.windows[0]

                # Use window reference if available, otherwise use current window
                if self.window_ref:
                    self.log.info("Hiding window...")
                    window.hide()
                else:
                    self.log.info("Hiding window (no ref)...")
                    window.hide()

                self.window_visible = False
                self.log.info("Window hidden - Ctrl+Space to show")
            else:
                self.log.warning("No webview window found")

        except Exception as e:
            self.log.error(f"Error hiding window: {e}")
