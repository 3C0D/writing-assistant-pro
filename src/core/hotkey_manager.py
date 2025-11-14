"""
Hotkey management module for Writing Assistant Pro
Handles global hotkey registration and management
"""

import logging
import threading
import time

import keyboard


class HotkeyManager:
    """
    Manages global hotkey registration and lifecycle

    Handles hotkey registration with optional delay to avoid startup conflicts,
    and proper cleanup of keyboard hooks.
    """

    def __init__(self, config):
        """
        Initialize HotkeyManager

        Args:
            config: Configuration object with HOTKEY_COMBINATION and HOTKEY_SETUP_DELAY
        """
        self.config = config
        self.log = logging.getLogger("WritingAssistant.HotkeyManager")
        self._hotkey_hook = None
        self._setup_thread = None
        self._toggle_callback = None

    def register(self, toggle_callback):
        """
        Register global hotkey immediately

        Args:
            toggle_callback: Function to call when hotkey is pressed

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Clear all existing hotkeys first to prevent duplicates
            keyboard.unhook_all()
            self._hotkey_hook = None

            # Register new hotkey
            self._toggle_callback = toggle_callback
            keyboard.add_hotkey(self.config.HOTKEY_COMBINATION, toggle_callback, suppress=False)

            self._hotkey_hook = self.config.HOTKEY_COMBINATION
            self.log.info(
                f"Global hotkey registered: {self.config.HOTKEY_COMBINATION} (toggle window)"
            )
            return True

        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False

    def register_delayed(self, toggle_callback):
        """
        Register global hotkey with delay to avoid startup conflicts

        Args:
            toggle_callback: Function to call when hotkey is pressed
        """

        def delayed_setup():
            time.sleep(self.config.HOTKEY_SETUP_DELAY)
            success = self.register(toggle_callback)
            if success:
                self.log.info(f"Press {self.config.HOTKEY_COMBINATION} to toggle window")
            else:
                self.log.error("Failed to setup hotkey")

        self._setup_thread = threading.Thread(target=delayed_setup, daemon=True)
        self._setup_thread.start()

    def unregister(self):
        """
        Unregister the current hotkey

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self._hotkey_hook:
                keyboard.remove_hotkey(self._hotkey_hook)
                self.log.info(f"Hotkey unregistered: {self._hotkey_hook}")
                self._hotkey_hook = None
                self._toggle_callback = None
                return True
            return False
        except Exception as e:
            self.log.error(f"Failed to unregister hotkey: {e}")
            return False

    def cleanup(self):
        """
        Full cleanup of all hotkey resources
        """
        try:
            keyboard.unhook_all()
            self._hotkey_hook = None
            self._toggle_callback = None
            self.log.debug("HotkeyManager cleaned up")
        except Exception as e:
            self.log.debug(f"HotkeyManager cleanup error: {e}")
