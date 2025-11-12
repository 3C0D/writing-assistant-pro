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
from src.ui import create_interface


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
                ui.button(f'Hide ({config.HOTKEY_COMBINATION})', on_click=lambda: self.window_manager.hide_window(), icon='visibility_off').props('flat dense')

            # Setup hotkey in a background thread (must be after ui.run starts)
            def setup_hotkey_delayed():
                time.sleep(self.config.HOTKEY_SETUP_DELAY)  # Wait for pywebview to fully initialize
                success = setup_hotkey(config, self.window_manager.toggle_window)

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