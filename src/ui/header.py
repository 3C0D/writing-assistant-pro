"""
Header component for the application
"""

from loguru import logger
from nicegui import ui


def create_header(config, window_manager):
    """
    Create application header with title and hide button.

    Args:
        config: Application configuration object
        window_manager: WindowManager instance for window control
    """
    log = logger.bind(name="WritingAssistant.ui.header")

    with (
        ui.header()
        .classes("items-center justify-between")
        .style("position: relative; background-color: #1976d2")
    ):
        ui.label("Writing Assistant Pro").classes("text-h6")
        ui.button(
            f"Hide ({config.HOTKEY_COMBINATION})",
            on_click=lambda: window_manager.hide_window(),
            icon="visibility_off",
        ).props("flat dense").style("z-index: 1000")

    log.debug("Header created successfully")
