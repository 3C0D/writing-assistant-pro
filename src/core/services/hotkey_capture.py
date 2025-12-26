"""
Hotkey capture service for Writing Assistant Pro

Provides scancode-based key capture for reliable hotkey detection
across different keyboard layouts (AZERTY, QWERTY, etc.)
"""

from __future__ import annotations

from collections.abc import Callable

import keyboard
from loguru import logger

# Modifier keys that should be handled specially
# Includes English names and French AZERTY names (maj = shift)
MODIFIER_KEYS = {
    "ctrl",
    "shift",
    "alt",
    "windows",
    "left ctrl",
    "right ctrl",
    "left shift",
    "right shift",
    "left alt",
    "right alt",
    "left windows",
    "right windows",
    # French AZERTY keyboards
    "maj",  # Shift on French keyboards
    "left maj",
    "right maj",
    "ctrl gauche",
    "ctrl droite",
    "alt gr",  # AltGr key
}

# Key name normalization map (raw name -> display name)
KEY_NAME_MAP = {
    "decimal": "Decimal",  # Numpad decimal point
    "add": "NumAdd",
    "subtract": "NumSubtract",
    "multiply": "NumMultiply",
    "divide": "NumDivide",
    "numpad 0": "Num0",
    "numpad 1": "Num1",
    "numpad 2": "Num2",
    "numpad 3": "Num3",
    "numpad 4": "Num4",
    "numpad 5": "Num5",
    "numpad 6": "Num6",
    "numpad 7": "Num7",
    "numpad 8": "Num8",
    "numpad 9": "Num9",
    "num lock": "NumLock",
    "page up": "PageUp",
    "page down": "PageDown",
    "caps lock": "CapsLock",
    "scroll lock": "ScrollLock",
    "print screen": "PrintScreen",
    "left": "Left",
    "right": "Right",
    "up": "Up",
    "down": "Down",
    "home": "Home",
    "end": "End",
    "insert": "Insert",
    "delete": "Delete",
    "backspace": "Backspace",
    "tab": "Tab",
    "enter": "Enter",
    "escape": "Escape",
    "space": "Space",
}

# Scancode to base key name mapping (for getting unshifted key name)
# These are standard Windows scancodes
SCANCODE_TO_KEY_NAME = {
    # Numpad keys (these change meaning with Shift/NumLock)
    82: "Num0",  # Numpad 0 / Insert
    79: "Num1",  # Numpad 1 / End
    80: "Num2",  # Numpad 2 / Down
    81: "Num3",  # Numpad 3 / PageDown
    75: "Num4",  # Numpad 4 / Left
    76: "Num5",  # Numpad 5
    77: "Num6",  # Numpad 6 / Right
    71: "Num7",  # Numpad 7 / Home
    72: "Num8",  # Numpad 8 / Up
    73: "Num9",  # Numpad 9 / PageUp
    83: "Decimal",  # Numpad . / Delete <- This is the key you're pressing!
    53: "NumDivide",  # Numpad /
    55: "NumMultiply",  # Numpad *
    74: "NumSubtract",  # Numpad -
    78: "NumAdd",  # Numpad +
    # Function keys
    59: "F1",
    60: "F2",
    61: "F3",
    62: "F4",
    63: "F5",
    64: "F6",
    65: "F7",
    66: "F8",
    67: "F9",
    68: "F10",
    87: "F11",
    88: "F12",
}

# Default hotkey
DEFAULT_HOTKEY = "ctrl+space"


class HotkeyCapture:
    """
    Captures keyboard input using scancodes for reliable hotkey detection.

    This class hooks into keyboard events and records the actual physical keys
    pressed, resolving issues with different keyboard layouts (AZERTY/QWERTY)
    and differentiating numpad keys from main keyboard keys.
    """

    def __init__(self):
        """Initialize the hotkey capture service."""
        self.log = logger.bind(name="WritingAssistant.HotkeyCapture")
        self._hook = None
        self._current_keys: set[str] = set()
        self._modifiers: set[str] = set()
        self._main_key: str | None = None
        self._on_update: Callable[[str], None] | None = None
        self._is_capturing = False

    def start_capture(self, on_update: Callable[[str], None]) -> None:
        """
        Start capturing keyboard input.

        Args:
            on_update: Callback called with formatted hotkey string on each key event
        """
        if self._is_capturing:
            self.log.warning("Already capturing, stopping previous capture first")
            self.stop_capture()

        self._on_update = on_update
        self._current_keys.clear()
        self._modifiers.clear()
        self._main_key = None
        self._is_capturing = True

        # Hook all keyboard events
        self._hook = keyboard.hook(self._on_key_event, suppress=True)
        self.log.debug("Started keyboard capture")

    def stop_capture(self) -> str:
        """
        Stop capturing keyboard input.

        Returns:
            The final captured hotkey string (storage format with +)
        """
        if self._hook:
            keyboard.unhook(self._hook)
            self._hook = None

        self._is_capturing = False
        result = self.get_current_hotkey()
        self.log.debug(f"Stopped keyboard capture, result: {result}")

        # Clear state
        self._current_keys.clear()
        self._modifiers.clear()
        self._main_key = None
        self._on_update = None

        return result

    def _on_key_event(self, event: keyboard.KeyboardEvent) -> None:
        """Handle keyboard events."""
        if not self._is_capturing:
            return

        key_name = event.name.lower() if event.name else ""

        if event.event_type == "down":
            is_mod = self._is_modifier(key_name)
            self.log.debug(f"Key DOWN: '{key_name}' (scan={event.scan_code}, is_mod={is_mod})")

            # Determine if this is a modifier or main key
            if is_mod:
                # Normalize modifier name
                normalized = self._normalize_modifier(key_name)
                self._modifiers.add(normalized)
                self.log.debug(f"  -> Modifier added: {normalized}, mods={self._modifiers}")
            else:
                # This is the main key (non-modifier)
                # Use scancode lookup first to get base key name (bypasses Shift for numpad)
                scancode = event.scan_code
                if scancode in SCANCODE_TO_KEY_NAME:
                    self._main_key = SCANCODE_TO_KEY_NAME[scancode]
                    self.log.debug(f"  -> Main key (scancode {scancode}): {self._main_key}")
                else:
                    # Fallback to key name (may be shifted on regular keyboard)
                    self._main_key = self._normalize_key_name(key_name)
                    self.log.debug(f"  -> Main key (name): {self._main_key}")

            self._current_keys.add(key_name)

            # Notify listener of current state
            if self._on_update:
                self._on_update(self.get_display_hotkey())

        elif event.event_type == "up":
            self.log.debug(f"Key UP: '{key_name}'")
            self._current_keys.discard(key_name)

            # Also remove from modifiers if it was a modifier
            if self._is_modifier(key_name):
                normalized = self._normalize_modifier(key_name)
                self._modifiers.discard(normalized)

    def _is_modifier(self, key_name: str) -> bool:
        """Check if a key is a modifier key."""
        return key_name in MODIFIER_KEYS

    def _normalize_modifier(self, key_name: str) -> str:
        """Normalize modifier key names."""
        # Remove left/right prefix first
        if key_name.startswith("left "):
            key_name = key_name[5:]
        elif key_name.startswith("right "):
            key_name = key_name[6:]

        # Normalize French names to standard names
        french_to_standard = {
            "maj": "shift",
            "alt gr": "alt",
            "ctrl gauche": "ctrl",
            "ctrl droite": "ctrl",
        }

        return french_to_standard.get(key_name, key_name)

    def _normalize_key_name(self, key_name: str) -> str:
        """Normalize key name for display."""
        # Check the mapping table
        if key_name in KEY_NAME_MAP:
            return KEY_NAME_MAP[key_name]
        # Capitalize single characters
        if len(key_name) == 1:
            return key_name.upper()
        # Return as-is for function keys etc.
        return key_name.capitalize()

    def get_current_hotkey(self) -> str:
        """
        Get the current hotkey in storage format.

        Returns:
            Hotkey string with + separator (e.g., "ctrl+shift+a")
        """
        if not self._modifiers and not self._main_key:
            return ""

        parts = []

        # Add modifiers in consistent order
        if "ctrl" in self._modifiers:
            parts.append("ctrl")
        if "alt" in self._modifiers:
            parts.append("alt")
        if "shift" in self._modifiers:
            parts.append("shift")
        if "windows" in self._modifiers:
            parts.append("win")

        # Add main key
        if self._main_key:
            parts.append(self._main_key.lower())

        return "+".join(parts)

    def get_display_hotkey(self) -> str:
        """
        Get the current hotkey in display format.

        Returns:
            Hotkey string with spaced separators (e.g., "Ctrl + Shift + A")
        """
        if not self._modifiers and not self._main_key:
            return "None"

        parts = []

        # Add modifiers in consistent order (capitalized for display)
        if "ctrl" in self._modifiers:
            parts.append("Ctrl")
        if "alt" in self._modifiers:
            parts.append("Alt")
        if "shift" in self._modifiers:
            parts.append("Shift")
        if "windows" in self._modifiers:
            parts.append("Win")

        # Add main key
        if self._main_key:
            parts.append(self._main_key)

        return " + ".join(parts)


def format_hotkey_for_display(hotkey: str | None) -> str:
    """
    Convert storage format hotkey to display format.

    Args:
        hotkey: Hotkey in storage format (e.g., "ctrl+shift+a") or None

    Returns:
        Display format string (e.g., "Ctrl + Shift + A") or "None"
    """
    if not hotkey:
        return "None"

    parts = hotkey.split("+")
    display_parts = []

    for part in parts:
        part = part.strip().lower()
        if part in ("ctrl", "alt", "shift", "win", "windows"):
            display_parts.append(part.capitalize())
        elif part in KEY_NAME_MAP:
            display_parts.append(KEY_NAME_MAP[part])
        elif len(part) == 1:
            display_parts.append(part.upper())
        else:
            display_parts.append(part.capitalize())

    return " + ".join(display_parts)


# not used
def format_hotkey_for_storage(display_hotkey: str) -> str:
    """
    Convert display format hotkey to storage format.

    Args:
        display_hotkey: Display format string (e.g., "Ctrl + Shift + A")

    Returns:
        Storage format string (e.g., "ctrl+shift+a")
    """
    if not display_hotkey or display_hotkey == "None":
        return ""

    # Split by " + " and lowercase everything
    parts = [p.strip().lower() for p in display_hotkey.split(" + ")]
    return "+ ".join(parts)
