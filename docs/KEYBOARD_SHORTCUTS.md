# Keyboard Shortcuts with NiceGUI

This document explains how to implement global keyboard shortcuts in a NiceGUI application.

## Overview

NiceGUI provides built-in keyboard event handling through `ui.keyboard()`, but for global desktop shortcuts (like Ctrl+Space to show/hide windows), you need to combine NiceGUI with system-level keyboard libraries.

## Approaches

### 1. NiceGUI Native Keyboard (Browser-based)

For web-based interfaces where shortcuts only work within the browser:

```python
from nicegui import ui

def handle_keyboard_event(e):
    print(f"Key pressed: {e.key}")

# Enable global keyboard tracking
ui.keyboard(on_key=handle_keyboard_event)
```

**Limitations:**

- Only works when the browser tab is focused
- Cannot capture system-wide shortcuts
- Limited key support (Space and arrow keys have known issues)

### 2. Global Keyboard Shortcuts (Recommended for Desktop)

For desktop applications with system-wide shortcuts, use `pynput`:

```python
from pynput import keyboard as pynput_keyboard
from pynput.keyboard import Key, Listener

class GlobalHotkeyManager:
    def __init__(self):
        self.current_keys = set()
        self.listener = None
        self.on_hotkey = None
    
    def on_press(self, key):
        try:
            self.current_keys.add(key)
            
            # Check for Ctrl+Space
            if (key == pynput_keyboard.Key.space and 
                (pynput_keyboard.Key.ctrl_l in self.current_keys or 
                 pynput_keyboard.Key.ctrl_r in self.current_keys)):
                if self.on_hotkey:
                    self.on_hotkey()
                    
        except AttributeError:
            pass
    
    def on_release(self, key):
        if key in self.current_keys:
            self.current_keys.discard(key)
    
    def start(self):
        self.listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
    
    def stop(self):
        if self.listener:
            self.listener.stop()

# Usage
hotkey_manager = GlobalHotkeyManager()
hotkey_manager.on_hotkey = lambda: print("Global shortcut triggered!")
hotkey_manager.start()
```

### 3. Combining Both Approaches (Hybrid)

For maximum flexibility, use both methods:

```python
from nicegui import ui
from pynput import keyboard as pynput_keyboard

def setup_keyboard_shortcuts(app_window_toggle):
    # Global system shortcuts (works everywhere)
    global_hotkey = GlobalHotkeyManager()
    global_hotkey.on_hotkey = app_window_toggle
    global_hotkey.start()
    
    # NiceGUI browser shortcuts (works in web interface)
    def handle_web_shortcut(e):
        if e.key.ctrl and e.key.name == 'space':
            app_window_toggle()
    
    ui.keyboard(on_key=handle_web_shortcut)
    
    return global_hotkey
```

## Best Practices

### 1. Debouncing and Spam Protection

Prevent multiple rapid triggers:

```python
import time
import threading

class SpamProtectedHotkey:
    def __init__(self, min_interval=1.0):
        self.last_trigger = 0.0
        self.min_interval = min_interval
        self.is_processing = False
        self.lock = threading.Lock()
    
    def should_trigger(self):
        now = time.time()
        if now - self.last_trigger < self.min_interval:
            return False
        if not self.lock.acquire(blocking=False):
            return False
        
        self.last_trigger = now
        return True
    
    def release(self):
        self.lock.release()
```

### 2. Cleanup and Resource Management

Always clean up keyboard listeners:

```python
import atexit

class Application:
    def __init__(self):
        self.hotkey_manager = GlobalHotkeyManager()
        atexit.register(self.cleanup)
    
    def cleanup(self):
        if self.hotkey_manager:
            self.hotkey_manager.stop()
```

### 3. Cross-Platform Compatibility

Handle different keyboard layouts and OS variations:

```python
def get_ctrl_key():
    import platform
    if platform.system() == 'Darwin':  # macOS
        return Key.cmd  # Command key instead of Ctrl
    else:
        return Key.ctrl_l  # Ctrl on Windows/Linux

def on_press(self, key):
    ctrl_key = get_ctrl_key()
    if key == Key.space and ctrl_key in self.current_keys:
        # Handle shortcut
        pass
```

## Implementation in Writing Assistant

The current implementation in this project uses the `HotkeyManager` class in `src/core/hotkey_manager.py`:

```python
from src.core.hotkey_manager import HotkeyManager

class Application:
    def __init__(self):
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.set_callback(self.toggle_window)
        
    def start(self):
        self.hotkey_manager.start()
        
    def toggle_window(self):
        # Toggle window visibility
        pass
```

### Key Features of Current Implementation

1. **Spam Protection**: Minimum interval between triggers
2. **Thread Safety**: Uses locks to prevent concurrent processing
3. **Resource Management**: Proper cleanup on application exit
4. **Cross-Platform**: Works on Windows, Linux, and macOS

## Common Issues and Solutions

### Issue 1: Keyboard Library Conflicts

**Problem**: Multiple keyboard libraries interfering
**Solution**: Use only one keyboard library per application

### Issue 2: Insufficient Permissions

**Problem**: Cannot register global shortcuts
**Solution**:

- Run as administrator on Windows
- Check macOS accessibility permissions
- Verify Linux user permissions

### Issue 3: Key State Conflicts

**Problem**: Keys remain "pressed" in internal state
**Solution**: Reset key state on application focus changes

## Security Considerations

1. **Hotkey Capture**: Be aware that global shortcuts can capture user input
2. **Permission Requests**: Some operating systems require explicit permission
3. **Privacy**: Consider the implications of global keyboard monitoring

## References

- [NiceGUI Keyboard Documentation](https://nicegui.io/documentation/keyboard)
- [pynput Documentation](https://pynput.readthedocs.io/)
- [Keyboard Library (Alternative)](https://github.com/boppreh/keyboard)

## Conclusion

For desktop applications using NiceGUI, the recommended approach is to:

1. Use `pynput` for global system shortcuts
2. Use NiceGUI's `ui.keyboard()` for browser-based shortcuts
3. Implement proper debouncing and cleanup
4. Handle cross-platform differences appropriately

The `HotkeyManager` class in this project demonstrates best practices for implementing global keyboard shortcuts with NiceGUI applications.
