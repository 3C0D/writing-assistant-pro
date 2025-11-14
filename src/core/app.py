"""
Main application class for Writing Assistant Pro
Handles window visibility, hotkeys, and application lifecycle
"""

import logging
import threading
import time

import keyboard
from nicegui import app, ui


class WritingAssistantApp:
    """
    Application with hidden window that shows/hides on hotkey
    Window close button hides instead of closing
    """

    def __init__(self):
        self.log = logging.getLogger("WritingAssistant.WritingAssistantApp")

    def run(self):
        """Run the application"""
        try:
            print("================ START ================")

            # Import configuration module
            # Core imports
            from src.ui import create_header, create_interface

            from . import (
                WindowManager,
                _,
                apply_theme,
                config,
                init_translation,
                setup_css_hot_reload,
                setup_hotkey_delayed,
                setup_root_logger,
            )

            self.config = config
            self.window_manager = WindowManager(config)

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
            app.native.window_args["resizable"] = config.WINDOW_RESIZABLE
            app.native.window_args["frameless"] = config.WINDOW_FRAMELESS
            app.native.start_args["debug"] = False

            # Apply theme
            apply_theme(config.DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(config.DARK_MODE, config.DEBUG)

            # Create interface
            create_interface()

            # Add header with hide button
            create_header(config, self.window_manager)

            # Setup hotkey in background thread
            setup_hotkey_delayed(config, self.window_manager.toggle_window, self.log)

            # Setup window hiding after startup
            def hide_window_on_startup():
                time.sleep(1.0)  # Wait for window to be fully created
                if config.WINDOW_START_HIDDEN:
                    self.window_manager.hide_window()
                    self.log.info("Window hidden on startup - Press Ctrl+Space to show")

            threading.Thread(target=hide_window_on_startup, daemon=True).start()

            # Run NiceGUI - DISABLE reload for native mode (causes multiple instances)
            self.log.info("Starting NiceGUI application...")

            ui.run(
                native=True,
                window_size=(800, 600),
                title="🔥 Writing Assistant Pro (DEV MODE)"
                if config.DEBUG
                else _("Writing Assistant Pro"),
                reload=True,
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
            from . import stop_css_hot_reload

            stop_css_hot_reload()  # Stop CSS hot reload
            keyboard.unhook_all()  # Clear all hotkeys
        except Exception as e:
            self.log.debug(f"Cleanup error: {e}")
        self.log.info("Application stopped")
