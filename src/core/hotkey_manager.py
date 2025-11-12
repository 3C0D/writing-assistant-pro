"""
Hotkey management module for Writing Assistant Pro
Handles global hotkey registration and management
"""

import logging

import keyboard


def setup_hotkey(config, toggle_callback):
    """
    Setup global hotkey using 'keyboard' library

    Args:
        config: Configuration object with HOTKEY_COMBINATION
        toggle_callback: Function to call when hotkey is pressed

    Returns:
        bool: True if successful, False otherwise
    """
    log = logging.getLogger("WritingAssistant.HotkeyManager")
    try:
        # Clear all existing hotkeys first to prevent duplicates
        keyboard.unhook_all()

        keyboard.add_hotkey(config.HOTKEY_COMBINATION, toggle_callback, suppress=False)
        log.info(f"Global hotkey registered: {config.HOTKEY_COMBINATION} (toggle window)")
        return True
    except Exception as e:
        log.error(f"Failed to register hotkey: {e}")
        return False
