"""
Main application class for Writing Assistant Pro
Handles window visibility, hotkeys, and application lifecycle
"""

import threading
import time
import logging
from nicegui import ui, app
import keyboard


# Core imports
from src.core import (
    apply_theme,
    init_translation,
    setup_root_logger,
    setup_css_hot_reload,
    stop_css_hot_reload,
    _
)
from src.core.hotkey_manager import setup_hotkey
from src.core.window_manager import WindowManager
from src.ui import create_interface, create_header


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
            from src.core import config
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
            app.native.window_args['resizable'] = config.WINDOW_RESIZABLE
            app.native.window_args['frameless'] = config.WINDOW_FRAMELESS
            app.native.start_args['debug'] = False

            # Apply theme
            apply_theme(config.DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(config.DARK_MODE, config.DEBUG)

            # Create interface
            create_interface()

            # Add header with hide button
            create_header(config, self.window_manager)

            # Setup hotkey in background thread
            def setup_hotkey_delayed():
                time.sleep(self.config.HOTKEY_SETUP_DELAY)
                success = setup_hotkey(config, self.window_manager.toggle_window)
                if success:
                    self.log.info(f"Press {self.config.HOTKEY_COMBINATION} to toggle window")
                else:
                    self.log.error("Failed to setup hotkey")

            threading.Thread(target=setup_hotkey_delayed, daemon=True).start()

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
                title="🔥 Writing Assistant Pro (DEV MODE)" if config.DEBUG else _("Writing Assistant Pro"),
                reload=False  # Must be False in native mode to avoid multiple instances
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