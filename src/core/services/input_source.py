from __future__ import annotations

import platform
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pyperclip
from loguru import logger
from PIL import Image, ImageGrab
from pynput import keyboard

if TYPE_CHECKING:
    from PIL.Image import Image as PILImage


@dataclass
class InputState:
    """Represents the state of available input sources."""

    clipboard_text: str | None = None
    clipboard_image: PILImage | None = None
    selection_text: str | None = None

    @property
    def has_clipboard_content(self) -> bool:
        return bool(self.clipboard_text or self.clipboard_image)

    @property
    def has_selection(self) -> bool:
        return bool(self.selection_text)

    @property
    def has_clipboard_text(self) -> bool:
        return bool(self.clipboard_text)

    @property
    def has_clipboard_image(self) -> bool:
        return self.clipboard_image is not None


class InputSourceService:
    """Service for detecting and managing input sources (clipboard, selection)."""

    def __init__(self):
        self._last_state = InputState()
        self.log = logger.bind(name="WritingAssistant.Services.InputSource")
        self._keyboard = keyboard.Controller()

    # =========================================================================
    # Clipboard Management
    # =========================================================================

    def get_clipboard_text(self) -> str | None:
        """Get text content from clipboard."""
        try:
            text = pyperclip.paste()
            return text.strip() if text and text.strip() else None
        except Exception as e:
            self.log.error(f"Failed to get clipboard text: {e}")
            return None

    def get_clipboard_image(self) -> PILImage | None:
        """Get image content from clipboard."""
        try:
            content = ImageGrab.grabclipboard()

            if isinstance(content, Image.Image):
                return content

            # Handle list of file paths - not considered as clipboard image
            return None

        except Exception as e:
            self.log.error(f"Failed to get clipboard image: {e}")
            return None

    def backup_clipboard(self) -> str | None:
        """Backup current clipboard text content."""
        try:
            return pyperclip.paste()
        except Exception as e:
            self.log.debug(f"Failed to backup clipboard: {e}")
            return None

    def restore_clipboard(self, content: str) -> None:
        """Restore clipboard content."""
        try:
            pyperclip.copy(content)
        except Exception as e:
            self.log.debug(f"Failed to restore clipboard: {e}")

    def clear_clipboard(self) -> None:
        """Clear the clipboard."""
        try:
            pyperclip.copy("")
        except Exception as e:
            self.log.debug(f"Failed to clear clipboard: {e}")

    # =========================================================================
    # Selection Capture (Windows)
    # =========================================================================

    def _simulate_ctrl_c(self) -> None:
        """Simulate Ctrl+C key press to copy selected text."""
        try:
            with self._keyboard.pressed(keyboard.Key.ctrl):
                time.sleep(0.05)  # Wait for Ctrl to register
                self._keyboard.press("c")
                time.sleep(0.05)  # Hold 'c' briefly
                self._keyboard.release("c")
                time.sleep(0.05)  # Wait before releasing Ctrl
        except Exception as e:
            self.log.error(f"Failed to simulate Ctrl+C: {e}")

    def _is_file_path(self, text: str) -> bool:
        """Check if text looks like a file path (from file/icon selection)."""
        try:
            from pathlib import Path

            path = Path(text)
            return path.exists() and path.is_file()
        except Exception:
            return False

    def get_selection_text(
        self,
        sleep_duration: float = 0.25,
        max_retries: int = 3,
        retry_delay: float = 0.15,
    ) -> str | None:
        """
        Get currently selected text by simulating Ctrl+C.

        This method:
        1. Backs up current clipboard content
        2. Clears clipboard
        3. Simulates Ctrl+C to copy selection
        4. Retrieves the new clipboard content (= selection)
        5. Restores original clipboard

        Args:
            sleep_duration: Time to wait after Ctrl+C for clipboard to update
            max_retries: Number of retry attempts
            retry_delay: Delay between retries

        Returns:
            Selected text or None if no selection
        """
        # Only works on Windows for now
        if platform.system() != "Windows":
            self.log.debug("Selection capture only supported on Windows")
            return None

        self.log.debug("Getting selected text via Ctrl+C simulation")

        # Backup current clipboard
        clipboard_backup = self.backup_clipboard()
        self.log.debug(
            f"Clipboard backed up: {clipboard_backup[:30] if clipboard_backup else 'Empty'}..."
        )

        selected_text: str | None = None

        # Give 200ms for user to release hotkey modifiers (e.g. Alt)
        # Otherwise we might send Ctrl+Alt+C instead of Ctrl+C
        time.sleep(0.2)

        for attempt in range(max_retries):
            self.log.debug(f"Ctrl+C attempt {attempt + 1}/{max_retries}")

            # Clear clipboard before attempt
            self.clear_clipboard()

            # Simulate Ctrl+C
            self._simulate_ctrl_c()

            # Wait for clipboard to update
            time.sleep(sleep_duration)

            # Check clipboard content
            current_clipboard = self.backup_clipboard()

            if current_clipboard and current_clipboard.strip():
                # Check if it's a file path (e.g., from file explorer selection)
                if self._is_file_path(current_clipboard.strip()):
                    self.log.debug(
                        f"Detected file path, treating as no selection: {current_clipboard[:50]}"
                    )
                    selected_text = None
                    break
                else:
                    selected_text = current_clipboard.strip()
                    self.log.debug(
                        f"Ctrl+C successful: {selected_text[:30] if selected_text else ''}..."
                    )
                    break
            else:
                if attempt < max_retries - 1:
                    self.log.debug(f"Ctrl+C failed, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                else:
                    self.log.debug("No selection detected after all attempts")

        # Restore original clipboard
        if clipboard_backup:
            self.restore_clipboard(clipboard_backup)
            self.log.debug("Clipboard restored")
        else:
            self.clear_clipboard()

        return selected_text

    # =========================================================================
    # Main Detection
    # =========================================================================

    def detect_sources(self) -> InputState:
        """
        Detect all available input sources.

        Priority: Selection > Clipboard
        If both selection and clipboard have content, selection takes priority.
        """
        # First, try to get selection (this will backup/restore clipboard)
        selection_text = self.get_selection_text()

        # Then get clipboard content (after selection capture restored it)
        clipboard_text = self.get_clipboard_text()
        clipboard_image = self.get_clipboard_image()

        state = InputState(
            clipboard_text=clipboard_text,
            clipboard_image=clipboard_image,
            selection_text=selection_text,
        )

        self._last_state = state
        self.log.debug(
            f"Detected sources - Selection: {bool(selection_text)}, "
            f"Clipboard text: {bool(clipboard_text)}, "
            f"Clipboard image: {bool(clipboard_image)}"
        )

        return state
