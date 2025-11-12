"""
Hotkey management module for Writing Assistant Pro
Handles global hotkey registration and management
"""

import logging

import keyboard


class HotkeyManager:
    """
    Manages global hotkey registration
    """

    def __init__(self, config, toggle_callback):
        self.config = config
        self.toggle_callback = toggle_callback
        self.log = logging.getLogger("WritingAssistant.HotkeyManager")

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
                self.toggle_callback,
                suppress=False
            )
            self.log.info(f"Global hotkey registered: {self.config.HOTKEY_COMBINATION} (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False