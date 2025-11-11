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

### 2. Global Keyboard Shortcuts with `keyboard` library (Recommended for Desktop)

For desktop applications with system-wide shortcuts, use the `keyboard` library:

```python
import keyboard

class GlobalHotkeyManager:
    def __init__(self):
        self.hotkeys_registered = False
    
    def setup_global_hotkey(self, hotkey_combination, callback, suppress=True):
        """
        Setup a global hotkey
        
        Args:
            hotkey_combination: String like 'ctrl+space' or 'ctrl+shift+a'
            callback: Function to call when hotkey is pressed
            suppress: Whether to suppress the key event (default True)
        """
        try:
            # Clear existing hotkeys to prevent conflicts
            keyboard.unhook_all()
            
            # Register the new hotkey
            keyboard.add_hotkey(hotkey_combination, callback, suppress=suppress)
            self.hotkeys_registered = True
            print(f"Hotkey registered: {hotkey_combination}")
            return True
            
        except Exception as e:
            print(f"Failed to register hotkey {hotkey_combination}: {e}")
            return False
    
    def clear_all_hotkeys(self):
        """Clear all registered hotkeys"""
        try:
            keyboard.unhook_all()
            self.hotkeys_registered = False
            print("All hotkeys cleared")
        except Exception as e:
            print(f"Error clearing hotkeys: {e}")

# Usage
hotkey_manager = GlobalHotkeyManager()

def on_ctrl_space():
    print("Ctrl+Space pressed!")
    # Your window toggle logic here

hotkey_manager.setup_global_hotkey('ctrl+space', on_ctrl_space)
```

### 3. Implementation in main.py

Here's how it's implemented in your Writing Assistant:

```python
import keyboard

class HiddenWindowApp:
    def setup_hotkey(self):
        """Setup hotkey using 'keyboard' library"""
        try:
            # Clear all existing hotkeys first to prevent duplicates
            keyboard.unhook_all()
            
            # Register the global hotkey
            keyboard.add_hotkey('ctrl+space', self.toggle_window, suppress=False)
            self.log.info("Global hotkey registered: Ctrl+Space (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            keyboard.unhook_all()  # Clear all hotkeys
        except Exception:
            pass
```

## Key Points from Your Implementation

### 1. `keyboard.unhook_all()` is Essential

The line `keyboard.unhook_all()` at line 162 is crucial because:

- **Prevents Duplicate Registrations**: Without this, hotkeys can be registered multiple times
- **Avoids Memory Leaks**: Cleans up previous keyboard hooks
- **Prevents Conflicts**: Ensures only your current hotkeys are active

### 2. Best Practices in Your Code

1. **Error Handling**: Always wrap hotkey operations in try-catch
2. **Cleanup**: Call `unhook_all()` on application exit
3. **Suppress Option**: Use `suppress=True` to prevent system from also processing the key
4. **Single Responsibility**: One hotkey registration per setup call

### 3. Advanced keyboard Library Features

```python
# Multiple hotkeys
keyboard.add_hotkey('ctrl+alt+h', show_help)
keyboard.add_hotkey('ctrl+shift+t', show_tools)

# Conditional hotkeys
def conditional_callback():
    if some_condition:
        perform_action()

# Wait for hotkey with timeout
keyboard.wait('ctrl+space', suppress=True, timeout=2.0)

# Remove specific hotkey
keyboard.remove_hotkey(handler_id)

# Hotkey blocking (advanced)
keyboard.block_key('ctrl')  # Block Ctrl key temporarily
```

## Common Issues and Solutions

### Issue 1: Hotkey Not Working

**Problem**: Global shortcut not triggering
**Solutions**:

- Run as administrator/with elevated privileges
- Check if other applications use the same shortcut
- Ensure `keyboard.unhook_all()` is called before registering new hotkeys

### Issue 2: Multiple Triggers

**Problem**: Hotkey fires multiple times
**Solutions**:

- Always call `keyboard.unhook_all()` before new registrations
- Use debouncing logic in your callback
- Check for existing hotkey conflicts

### Issue 3: Insufficient Permissions

**Problem**: Cannot register global shortcuts
**Solutions**:

- Windows: Run as administrator
- macOS: Grant accessibility permissions in System Preferences
- Linux: Check user permissions for input devices

## Security Considerations

1. **Hotkey Capture**: Global shortcuts capture all user input
2. **Permission Requirements**: Some OS require explicit permission
3. **User Experience**: Be careful not to interfere with system shortcuts
4. **Cleanup**: Always clean up hotkeys when your application exits

## Implementation in Writing Assistant

Your current implementation in `main.py` uses the correct approach:

```python
def setup_hotkey(self):
    try:
        # Clear all existing hotkeys first to prevent duplicates
        keyboard.unhook_all()
        
        keyboard.add_hotkey('ctrl+space', self.toggle_window, suppress=False)
        self.log.info("Global hotkey registered: Ctrl+Space (toggle window)")
        return True
    except Exception as e:
        self.log.error(f"Failed to register hotkey: {e}")
        return False
```

This implementation:

- ✅ Uses `keyboard.unhook_all()` to prevent conflicts
- ✅ Has proper error handling
- ✅ Registers only the needed hotkey
- ✅ Cleans up on application exit

## References

- [Keyboard Library Documentation](https://github.com/boppreh/keyboard)
- [NiceGUI Keyboard Documentation](https://nicegui.io/documentation/keyboard)

## Conclusion

For NiceGUI desktop applications, using the `keyboard` library with proper `unhook_all()` calls is the recommended approach. Your current implementation follows best practices and provides reliable global keyboard shortcuts for Windows, Linux, and macOS.
