"""
Main application class for Writing Assistant Pro
Handles window visibility, hotkeys, and application lifecycle
"""

import argparse

from loguru import logger
from nicegui import app, ui


class WritingAssistantApp:
    """
    Application with hidden window that shows/hides on hotkey
    Window close button hides instead of closing
    """

    def __init__(self):
        self.log = logger.bind(name="WritingAssistant.WritingAssistantApp")
        self.hotkey_manager = None

    def run(self, args: argparse.Namespace | None = None) -> None:
        """
        Run the application

        Args:
            args: Command line arguments (optional)
        """
        try:
            print("================ START ================")

            # Import configuration module
            # Core imports
            from src.ui import create_header, create_interface

            from . import (
                ConfigManager,
                HotkeyManager,
                WindowManager,
                _,
                apply_theme,
                init_translation,
                setup_css_hot_reload,
                setup_root_logger,
            )

            self.config = ConfigManager()

            # Apply command line arguments
            if args and hasattr(args, "debug") and args.debug:
                self.config.DEBUG = True

            self.window_manager = WindowManager(self.config)
            self.hotkey_manager = HotkeyManager(self.config)

            # Initialize translation system
            init_translation("writing_assistant", "translations", self.config.LANGUAGE)

            # Setup root logger
            setup_root_logger(debug=self.config.DEBUG)

            # Re-bind logger after setup (in case it was reconfigured)
            self.log = logger.bind(name="WritingAssistant.App")

            self.log.info(
                f"{_('Configuration: DEBUG=')}{self.config.DEBUG}, "
                f"DARK_MODE={self.config.DARK_MODE}, "
                f"LANGUAGE={self.config.LANGUAGE}"
            )

            # Configure native window
            self.window_manager.configure_native_window(app)

            # Apply theme
            apply_theme(self.config.DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(self.config.DARK_MODE, self.config.DEBUG)

            # Create interface
            create_interface()

            # Add header with hide button
            create_header(self.config, self.window_manager)

            # Setup hotkey in background thread
            self.hotkey_manager.register_delayed(self.window_manager.toggle_window)

            # Run NiceGUI - DISABLE reload for native mode (causes multiple instances)
            self.log.info("Starting NiceGUI application...")

            ui.run(
                native=True,
                window_size=(800, 600),
                title="🔥 Writing Assistant Pro (DEV MODE)"
                if self.config.DEBUG
                else _("Writing Assistant Pro"),
                reload=self.config.DEBUG,  # Only reload in debug mode
            )

        except KeyboardInterrupt:
            self.log.info("Application interrupted by user")
        except Exception as e:
            self.log.error(f"Application error: {e}")
            import traceback

            self.log.debug(f"Full traceback: {traceback.format_exc()}")
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources"""
        self.log.info("Cleaning up...")
        try:
            from . import stop_css_hot_reload

            stop_css_hot_reload()  # Stop CSS hot reload
            if self.hotkey_manager:
                self.hotkey_manager.cleanup()  # Clean up hotkeys
        except Exception as e:
            self.log.debug(f"Cleanup error: {e}")
        self.log.info("Application stopped")
