Voici la refactorisation en classe :

## 1. Nouveau `hotkey_manager.py`## 2. Modifications dans `__init__.py`

**À RETIRER :**
```python
# Import hotkey management system
from .hotkey_manager import setup_hotkey, setup_hotkey_delayed
```

**À AJOUTER :**
```python
# Import hotkey management system
from .hotkey_manager import HotkeyManager
```

**Dans le `__all__` :**
- **Retirer :** `"setup_hotkey"`, `"setup_hotkey_delayed"`
- **Ajouter :** `"HotkeyManager"`

## 3. Modifications dans `app.py`

### Dans `__init__` de la classe `WritingAssistantApp` :
Après la ligne `self.log = logging.getLogger("WritingAssistant.WritingAssistantApp")`, **ajouter :**
```python
self.hotkey_manager = None
```

### Dans la méthode `run()` :

**Partie des imports - remplacer :**
```python
from . import (
    WindowManager,
    _,
    apply_theme,
    config,
    init_translation,
    setup_css_hot_reload,
    setup_hotkey_delayed,  # ← À RETIRER
    setup_root_logger,
)
```

**Par :**
```python
from . import (
    HotkeyManager,  # ← NOUVEAU
    WindowManager,
    _,
    apply_theme,
    config,
    init_translation,
    setup_css_hot_reload,
    setup_root_logger,
)
```

**Après la ligne `self.window_manager = WindowManager(config)`, ajouter :**
```python
self.hotkey_manager = HotkeyManager(config)
```

**Remplacer cette ligne :**
```python
# Setup hotkey in background thread
setup_hotkey_delayed(config, self.window_manager.toggle_window, self.log)
```

**Par :**
```python
# Setup hotkey in background thread
self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
```

### Dans la méthode `cleanup()` :

**Remplacer :**
```python
try:
    from . import stop_css_hot_reload

    stop_css_hot_reload()  # Stop CSS hot reload
    keyboard.unhook_all()  # Clear all hotkeys
except Exception as e:
    self.log.debug(f"Cleanup error: {e}")
```

**Par :**
```python
try:
    from . import stop_css_hot_reload

    stop_css_hot_reload()  # Stop CSS hot reload
    if self.hotkey_manager:
        self.hotkey_manager.cleanup()  # Clean up hotkeys
except Exception as e:
    self.log.debug(f"Cleanup error: {e}")
```

---

## Résumé des changements

1. **`hotkey_manager.py`** : Complètement refactoré en classe (voir artifact)
2. **`__init__.py`** : Import de `HotkeyManager` au lieu des fonctions
3. **`app.py`** : 
   - Instanciation de `HotkeyManager(config)`
   - Appel `self.hotkey_manager.register_delayed(...)`
   - Appel `self.hotkey_manager.cleanup()` dans cleanup

**Plus besoin d'importer `keyboard` dans `app.py`** car tout est géré par la classe maintenant ! 🎯


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
            keyboard.add_hotkey(
                self.config.HOTKEY_COMBINATION, 
                toggle_callback, 
                suppress=False
            )
            
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