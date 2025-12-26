"""
Hotkey management module for Writing Assistant Pro
Handles global hotkey registration and management
"""

from __future__ import annotations

import threading
import time

import keyboard
from loguru import logger


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
        self.log = logger.bind(name="WritingAssistant.HotkeyManager")
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
        hotkey = self.config.HOTKEY_COMBINATION

        # Check if hotkey is disabled (None or empty)
        if not hotkey:
            self.log.info("Hotkey is disabled (None or empty), skipping registration")
            self.cleanup()
            return False

        try:
            # Clear all existing hotkeys first to prevent duplicates
            self.log.debug("Clearing all existing keyboard hooks...")
            keyboard.unhook_all()
            self._hotkey_hook = None

            # Register new hotkey
            self._toggle_callback = toggle_callback
            self.log.debug(f"Adding hotkey: {hotkey} (suppress=True)")
            keyboard.add_hotkey(hotkey, toggle_callback, suppress=True)

            self._hotkey_hook = hotkey
            self.log.info(f"Global hotkey registered: {hotkey} (toggle window)")
            return True

        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            import traceback

            self.log.error(f"Traceback: {traceback.format_exc()}")
            return False

    def register_delayed(self, toggle_callback):
        """
        Register global hotkey with delay to avoid startup conflicts

        Args:
            toggle_callback: Function to call when hotkey is pressed
        """

        def delayed_setup():
            self.log.info(f"Waiting {self.config.HOTKEY_SETUP_DELAY}s before registering hotkey...")
            time.sleep(self.config.HOTKEY_SETUP_DELAY)
            self.log.info(f"Attempting to register hotkey: {self.config.HOTKEY_COMBINATION}")
            success = self.register(toggle_callback)
            if success:
                self.log.info(
                    f"✓ Hotkey ready! Press {self.config.HOTKEY_COMBINATION} to toggle window"
                )
            else:
                self.log.error("✗ Failed to setup hotkey - please check logs")

        self._setup_thread = threading.Thread(target=delayed_setup, daemon=True)
        self._setup_thread.start()
        self.log.debug("Hotkey registration thread started")

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
