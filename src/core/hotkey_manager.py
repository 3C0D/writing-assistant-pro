"""
Hotkey Manager - Handles global hotkey registration and management.

This module contains the logic for managing global hotkeys, keyboard listeners,
and signal handling for the Writing Assistant application.
"""

import logging
import signal
import time
import threading
from typing import Optional, Callable

from pynput import keyboard as keyboard
from pynput.keyboard import Key, KeyCode, Listener

from .logger import setup_logger


class HotkeyManager:
    """
    Manages global hotkey registration, keyboard listeners, and spam protection.
    """

    def __init__(self):
        self._logger = setup_logger(False, "HotkeyManager")

        # Hotkey system attributes
        self.hotkey_listener: Optional[Listener] = None
        self.is_running = False
        self._current_pressed_keys: set = set()

        # Enhanced spam protection attributes
        self.last_trigger_time = 0.0
        self.MIN_TRIGGER_INTERVAL = 1.0  # Minimum time between triggers in seconds
        self.hotkey_processing = threading.Lock()  # Use lock instead of boolean
        self.cooldown_timer: Optional[threading.Timer] = None

        # Callback for when hotkey is triggered
        self.on_hotkey_callback: Optional[Callable] = None

        # Track if Ctrl+Space was already triggered this press cycle
        self.trigger_fired_for_current_press = False

    def on_key_press(self, key) -> None:
        """
        Handle key press events.
        """
        try:
            # Track currently pressed keys
            self._current_pressed_keys.add(key)

            # Check for Control + Space combination
            if key == Key.space:
                if Key.ctrl_l in self._current_pressed_keys or Key.ctrl_r in self._current_pressed_keys:
                    # Only trigger once per press cycle
                    if not self.trigger_fired_for_current_press:
                        self.trigger_fired_for_current_press = True
                        self._handle_hotkey_trigger()

        except AttributeError:
            # Handle special keys
            pass

    def on_key_release(self, key) -> None:
        """
        Handle key release events to track currently pressed keys.
        """
        if hasattr(self, '_current_pressed_keys'):
            if key in self._current_pressed_keys:
                self._current_pressed_keys.discard(key)

            # Reset trigger flag when Space or Ctrl is released
            if key == Key.space or key == Key.ctrl_l or key == Key.ctrl_r:
                self.trigger_fired_for_current_press = False

    def _handle_hotkey_trigger(self) -> None:
        """
        Handle the hotkey trigger event with improved debouncing.
        """
        current_time = time.time()

        # Try to acquire the lock without blocking
        if not self.hotkey_processing.acquire(blocking=False):
            self._logger.debug("Hotkey already processing, ignoring duplicate trigger")
            return

        try:
            # Check minimum interval between triggers
            time_since_last = current_time - self.last_trigger_time
            if time_since_last < self.MIN_TRIGGER_INTERVAL:
                self._logger.debug(f"Ignoring hotkey trigger - too soon after last trigger ({time_since_last:.2f}s)")
                return

            # Update last trigger time
            self.last_trigger_time = current_time
            self._logger.info("Hotkey triggered - executing callback")

            # Log system info for debugging
            import platform
            self._logger.debug(f"Platform: {platform.system()} {platform.release()}")
            self._logger.debug(f"Python executable: {__import__('sys').executable}")
            self._logger.debug(f"Process ID: {__import__('os').getpid()}")

            # Call the callback if set
            if self.on_hotkey_callback:
                try:
                    self._logger.debug("Calling hotkey callback function")
                    self.on_hotkey_callback()
                    self._logger.debug("Hotkey callback completed successfully")
                except Exception as e:
                    self._logger.error(f"Error in hotkey callback: {e}")
                    import traceback
                    self._logger.debug(f"Callback traceback: {traceback.format_exc()}")

        finally:
            # Schedule lock release after cooldown period
            def release_lock():
                time.sleep(0.5)  # Additional cooldown
                self.hotkey_processing.release()
                self._logger.debug("Hotkey processing lock released")

            threading.Thread(target=release_lock, daemon=True).start()

    def start(self) -> bool:
        """
        Start the hotkey listener.

        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            if self.hotkey_listener is not None:
                self.stop()

            self._logger.info("Starting global hotkey listener for Ctrl+Space")

            # Reset state
            self._current_pressed_keys = set()
            self.trigger_fired_for_current_press = False

            # Create listener
            self.hotkey_listener = Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )

            # Start the listener
            self.hotkey_listener.start()
            self.is_running = True

            self._logger.info("Hotkey listener started successfully")
            return True

        except Exception as e:
            self._logger.error(f"Failed to start hotkey listener: {e}")
            return False

    def stop(self) -> None:
        """
        Stop the hotkey listener.
        """
        self._logger.info("Stopping hotkey listener")

        if self.hotkey_listener is not None:
            self.hotkey_listener.stop()
            self.hotkey_listener = None

        # Cancel any pending cooldown timer
        if self.cooldown_timer is not None:
            self.cooldown_timer.cancel()
            self.cooldown_timer = None

        self.is_running = False
        self._logger.info("Hotkey listener stopped")

    def set_callback(self, callback: Callable) -> None:
        """
        Set the callback function to call when hotkey is triggered.

        Args:
            callback: Function to call when hotkey is pressed
        """
        self.on_hotkey_callback = callback

    def cleanup(self) -> None:
        """
        Clean up hotkey resources when the application exits.
        """
        self._logger.debug("Cleaning up hotkey manager")
        self.stop()