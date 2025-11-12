"""
Header component for the application
"""

import logging
from nicegui import ui


def create_header(config, window_manager):
    """
    Create application header with title and hide button.
    
    Args:
        config: Application configuration object
        window_manager: WindowManager instance for window control
    """
    logger = logging.getLogger("WritingAssistant.ui.header")
    
    with ui.header().classes('items-center justify-between'):
        ui.label('Writing Assistant Pro').classes('text-h6')
        ui.button(
            f'Hide ({config.HOTKEY_COMBINATION})', 
            on_click=lambda: window_manager.hide_window(), 
            icon='visibility_off'
        ).props('flat dense')
    
    logger.debug("Header created successfully")