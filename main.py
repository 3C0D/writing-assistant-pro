"""
Application entry point for Writing Assistant Pro
Properly handles window hide/show with Ctrl+Space and prevents closing
"""

import threading
import time
import argparse
from nicegui import ui, app
from src.core import apply_theme, setup_logger, init_translation, _
from src.core.styles import setup_css_hot_reload, stop_css_hot_reload
from src.ui import create_interface

import keyboard
import webview

# Language configuration
LANGUAGE = "fr"
DEBUG = False

# Parse command line arguments
def parse_arguments():
    global DEBUG
    parser = argparse.ArgumentParser(description="Writing Assistant Pro")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    DEBUG = args.debug
    return args

parse_arguments()

# Initialize translation system
init_translation("writing_assistant", "translations", LANGUAGE)

# Configure logger
log = setup_logger(debug=DEBUG)

# Theme configuration
DARK_MODE = False

# Native window configuration - START HIDDEN
app.native.window_args['resizable'] = True
app.native.window_args['frameless'] = False
app.native.window_args['hidden'] = True  # Start hidden
app.native.start_args['debug'] = False

log.info(f"{_('Configuration: DEBUG=')}{DEBUG}, DARK_MODE={DARK_MODE}")

class HiddenWindowApp:
    """
    Application with hidden window that shows/hides on hotkey
    Window close button hides instead of closing
    """

    def __init__(self):
        self.log = setup_logger(debug=DEBUG, name="WritingAssistant")
        self.last_trigger_time = 0.0
        self.MIN_TRIGGER_INTERVAL = 1.0  # 1 second debounce (reduced)
        self.trigger_lock = threading.Lock() # prevent overlapping triggers. not locked!
        self.window_ref = None
        self.window_visible = False
        self.window_initialized = False # to register close handler only once

    def on_closing(self):
        """
        Handle window close event - hide instead of closing
        This prevents the window from being destroyed
        """
        def hide_in_thread():
            self.log.info("Window close requested - hiding instead")
            try:
                if self.window_ref:
                    self.window_ref.hide() # not destroyed
                    self.window_visible = False # Update state
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
            if time_since_last < self.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return

            self.last_trigger_time = current_time

            # Simpler logic - always show window if not visible, hide if visible
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
        """Setup hotkey using 'keyboard' library"""
        try:
            # Clear all existing hotkeys first to prevent duplicates
            keyboard.unhook_all()
            
            keyboard.add_hotkey('ctrl+space', self.toggle_window, suppress=False)
            self.log.info("Global hotkey registered: Ctrl+Space (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False

    def run(self):
        """Run the application"""
        try:
            # Apply theme
            apply_theme(DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(DARK_MODE, DEBUG)

            # Create interface
            create_interface(log)

            # Add hide button to interface
            with ui.header().classes('items-center justify-between'):
                ui.label('Writing Assistant Pro').classes('text-h6')
                ui.button('Hide (Ctrl+Space)', on_click=lambda: self.hide_window(), icon='visibility_off').props('flat dense')

            # Setup hotkey in a background thread (must be after ui.run starts)
            def setup_hotkey_delayed():
                time.sleep(2.0)  # Wait for pywebview to fully initialize
                success = self.setup_hotkey()

                if success:
                    self.log.info("Press Ctrl+Space to toggle window")
                else:
                    self.log.error("Failed to setup hotkey")

            threading.Thread(target=setup_hotkey_delayed, daemon=True).start()

            # Run NiceGUI in native mode with HIDDEN window
            self.log.info("Starting NiceGUI with hidden window...")
            self.log.info("Window will appear when you press Ctrl+Space")

            ui.run(
                native=True,
                window_size=(800, 600),
                title="🔥 Writing Assistant Pro (DEV MODE)" if DEBUG else _("Writing Assistant Pro"),
                reload=DEBUG,
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
        except Exception:
            pass
        self.log.info("Application stopped")

def main():
    """Main entry point"""
    app = HiddenWindowApp()
    app.run()

if __name__ in {'__main__', '__mp_main__'}:
    main()
