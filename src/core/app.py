"""
Main application class for Writing Assistant Pro
Handles window visibility, hotkeys, and application lifecycle
"""

import threading
import time
import logging

from nicegui import ui, app

import keyboard
import webview

# Core imports
from src.core import (
    apply_theme,
    init_translation,
    setup_root_logger,
    setup_css_hot_reload,
    stop_css_hot_reload,
    _
)
from src.ui import create_interface


class WritingAssistantApp:
    """
    Application with hidden window that shows/hides on hotkey
    Window close button hides instead of closing
    """

    def __init__(self):
        self.log = logging.getLogger("WritingAssistant.WritingAssistantApp")
        self.last_trigger_time = 0.0
        self.MIN_TRIGGER_INTERVAL = 1.0  # 1 second debounce (reduced)
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

            # Toggle visibility
            if not self.window_visible:
                self.show_window()
            else:
                self.hide_window()

        finally:
            # Release lock immediately instead of with delay
            self.trigger_lock.release()
            self.log.debug("Lock released")

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
                    window.on_top = True
                    self.log.info("Window shown - set to always on top")
                except Exception:
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

    def setup_hotkey(self):
        """
        Setup global hotkey using 'keyboard' library

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Clear all existing hotkeys first to prevent duplicates
            keyboard.unhook_all()

            keyboard.add_hotkey(
                self.config.HOTKEY_COMBINATION,
                self.toggle_window,
                suppress=False
            )
            self.log.info(f"Global hotkey registered: {self.config.HOTKEY_COMBINATION} (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False

    def run(self):
        """Run the application"""
        try:
            # Import configuration module
            from src.core import config
            self.config = config

            # Initialize translation system
            init_translation("writing_assistant", "translations", config.LANGUAGE)

            # Setup root logger
            setup_root_logger(debug=config.DEBUG)

            # Re-get logger after setup (in case it was reconfigured)
            self.log = logging.getLogger("WritingAssistant.App")

            self.log.info(
                f"{_('Configuration: DEBUG=')}{config.DEBUG}, "
                f"DARK_MODE={config.DARK_MODE}, "
                f"LANGUAGE={config.LANGUAGE}"
            )

            # Configure native window
            app.native.window_args['resizable'] = config.WINDOW_RESIZABLE
            app.native.window_args['frameless'] = config.WINDOW_FRAMELESS
            app.native.window_args['hidden'] = config.WINDOW_START_HIDDEN
            app.native.start_args['debug'] = False

            # Apply theme
            apply_theme(config.DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(config.DARK_MODE, config.DEBUG)

            # Create interface (no need to pass logger anymore)
            create_interface()

            # Add hide button to interface
            with ui.header().classes('items-center justify-between'):
                ui.label('Writing Assistant Pro').classes('text-h6')
                ui.button(f'Hide ({config.HOTKEY_COMBINATION})', on_click=lambda: self.hide_window(), icon='visibility_off').props('flat dense')

            # Setup hotkey in a background thread (must be after ui.run starts)
            def setup_hotkey_delayed():
                time.sleep(self.config.HOTKEY_SETUP_DELAY)  # Wait for pywebview to fully initialize
                success = self.setup_hotkey()

                if success:
                    self.log.info(f"Press {self.config.HOTKEY_COMBINATION} to toggle window")
                else:
                    self.log.error("Failed to setup hotkey")

            threading.Thread(target=setup_hotkey_delayed, daemon=True).start()

            # Run NiceGUI in native mode with HIDDEN window
            self.log.info("Starting NiceGUI with hidden window...")
            self.log.info("Window will appear when you press Ctrl+Space")

            ui.run(
                native=True,
                window_size=(800, 600),
                title="🔥 Writing Assistant Pro (DEV MODE)" if config.DEBUG else _("Writing Assistant Pro"),
                reload=config.DEBUG,
                show=False
            )

        except KeyboardInterrupt:
            self.log.info("Application interrupted by user")
        except Exception as e:
            self.log.error(f"Application error: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.log.info("Cleaning up...")
        try:
            stop_css_hot_reload()  # Stop CSS hot reload
            keyboard.unhook_all()  # Clear all hotkeys
        except Exception as e:
            self.log.debug(f"Cleanup error: {e}")
        self.log.info("Application stopped")