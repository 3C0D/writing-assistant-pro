Tu as raison de te poser la question ! Voici comment organiser les logs proprement :

## Le problème actuel

Dans `app.py`, tu as effectivement **deux loggers différents** :

- `self.log` pour les logs de la classe `WritingAssistantApp`
- `main_log` pour les logs de configuration

C'est un peu redondant, mais pas forcément faux. Voici comment améliorer ça :Voilà ! J'ai simplifié en **utilisant uniquement `self.log`** au lieu de créer un `main_log` séparé.

## Pourquoi c'est mieux ainsi ?

### ✅ Organisation propre des logs

```
WritingAssistant.App          ← Classe principale (app.py)
src.core.styles               ← Module styles
src.ui.components             ← Composants UI
...
```

Chaque module/classe a **son propre logger** avec son nom, ce qui permet de :

- Filtrer les logs par module
- Voir clairement d'où vient chaque log
- Garder une hiérarchie cohérente

### 📝 Exemple de logs produits

```
2025-11-12 18:03:14,627 - WritingAssistant.App - INFO - Configuration: DEBUG=True, DARK_MODE=True, LANGUAGE=fr
2025-11-12 18:03:14,628 - src.core.styles - INFO - Dark mode enabled
2025-11-12 18:03:14,630 - WritingAssistant.App - INFO - Starting NiceGUI with hidden window...
```

### 🤔 Faut-il logger la config dans config.py ?

**Non**, c'est mieux dans `app.py` parce que :

- Le module `config.py` est juste des **variables**, pas de la logique
- C'est l'application qui **utilise** la config, donc c'est elle qui log
- Si tu mets un logger dans `config.py`, il va se déclencher à chaque import

## Structure finale recommandée

```python
# config.py - PAS de logging ici
DARK_MODE = True
DEBUG = False
# ...

# app.py - Logging ICI
class WritingAssistantApp:
    def run(self):
        self.log.info(f"Config: DEBUG={config.DEBUG}, DARK_MODE={config.DARK_MODE}")
        # ...
```

Ton organisation actuelle est parfaite maintenant ! 🎉

"""
Main application class for Writing Assistant Pro
Handles window visibility, hotkeys, and application lifecycle
"""

import threading
import time
import logging
import importlib

from nicegui import ui, app

import keyboard
import webview

class WritingAssistantApp:
    """
    Main application class with hidden window that shows/hides on hotkey.
    Window close button hides instead of closing.
    """

    def __init__(self):
        """Initialize the application"""
        self.log = logging.getLogger("WritingAssistant.App")
        self.last_trigger_time = 0.0
        self.trigger_lock = threading.Lock()
        self.window_ref = None
        self.window_visible = False
        self.window_initialized = False
        
        # Configuration will be loaded in run()
        self.config = None
        
        self.log.debug("WritingAssistantApp initialized")

    def on_closing(self):
        """
        Handle window close event - hide instead of closing.
        This prevents the window from being destroyed.
        
        Returns:
            bool: False to prevent actual closing
        """
        def hide_in_thread():
            self.log.info("Window close requested - hiding instead")
            try:
                if self.window_ref:
                    self.window_ref.hide()
                    self.window_visible = False
                    self.log.info(f"Window hidden - Press {self.config.HOTKEY_COMBINATION} to show again")
            except Exception as e:
                self.log.error(f"Error hiding window: {e}")

        # Hide in a separate thread to avoid blocking
        threading.Thread(target=hide_in_thread, daemon=True).start()
        return False

    def toggle_window(self):
        """Toggle window visibility on hotkey press"""
        # Try to acquire lock without blocking
        if not self.trigger_lock.acquire(blocking=False):
            self.log.debug("Hotkey already processing, ignoring")
            return

        try:
            current_time = time.time()

            # Debounce check
            time_since_last = current_time - self.last_trigger_time
            if time_since_last < self.config.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return

            self.last_trigger_time = current_time

            # Toggle visibility
            if not self.window_visible:
                self.show_window()
            else:
                self.hide_window()

        finally:
            self.trigger_lock.release()
            self.log.debug("Lock released")

    def show_window(self):
        """Show the native window"""
        try:
            if webview.windows:
                window = webview.windows[0]
                self.window_ref = window
                
                # Register close handler only once
                if not self.window_initialized:
                    window.events.closing += self.on_closing
                    self.window_initialized = True
                    self.log.info("Window close handler registered")

                self.log.info("Showing window...")
                window.show()
                
                # Set window always on top
                try:
                    window.on_top = True
                    self.log.info("Window shown - set to always on top")
                except Exception:
                    self.log.info("Window shown - Check your screen")
                    
                self.window_visible = True
            else:
                self.log.warning("No webview window found")

        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")

    def hide_window(self):
        """Hide the native window"""
        try:
            if webview.windows:
                window = webview.windows[0]
                
                self.log.info("Hiding window...")
                window.hide()
                self.window_visible = False
                self.log.info(f"Window hidden - {self.config.HOTKEY_COMBINATION} to show")
            else:
                self.log.warning("No webview window found")

        except Exception as e:
            self.log.error(f"Error hiding window: {e}")

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
                self.toggle_window,
                suppress=False
            )
            self.log.info(f"Global hotkey registered: {self.config.HOTKEY_COMBINATION} (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey: {e}")
            return False

    def setup_hotkey_delayed(self):
        """Setup hotkey after a delay to ensure pywebview is initialized"""
        time.sleep(self.config.HOTKEY_SETUP_DELAY)
        success = self.setup_hotkey()

        if success:
            self.log.info(f"Press {self.config.HOTKEY_COMBINATION} to toggle window")
        else:
            self.log.error("Failed to setup hotkey")

    def create_ui(self):
        """Create the user interface"""
        from src.ui import create_interface
        
        # Create main interface
        create_interface()

        # Add header with hide button
        with ui.header().classes('items-center justify-between'):
            ui.label('Writing Assistant Pro').classes('text-h6')
            ui.button(
                f'Hide ({self.config.HOTKEY_COMBINATION})',
                on_click=lambda: self.hide_window(),
                icon='visibility_off'
            ).props('flat dense')

    def run(self):
        """Run the application"""
        try:
            # Import configuration module - will be fresh on reload
            from src.core import config
            self.config = config
            
            # Import other core modules
            from src.core import (
                apply_theme,
                init_translation,
                setup_root_logger,
                _
            )
            from src.core.styles import setup_css_hot_reload, stop_css_hot_reload

            # Initialize translation system
            init_translation("writing_assistant", "translations", config.LANGUAGE)
            
            # Setup root logger
            setup_root_logger(debug=config.DEBUG)
            
            # Re-get logger after setup (in case it was reconfigured)
            self.log = logging.getLogger("WritingAssistant.App")
            
            # Log configuration (use self.log, not a separate logger)
            self.log.info(
                f"{_('Configuration: DEBUG=')}{config.DEBUG}, "
                f"DARK_MODE={config.DARK_MODE}, "
                f"LANGUAGE={config.LANGUAGE}"
            )

            # Configure native window
            app.native.window_args['resizable'] = config.WINDOW_RESIZABLE
            app.native.window_args['frameless'] = config.WINDOW_FRAMELESS
            app.native.window_args['hidden'] = config.WINDOW_START_HIDDEN
            app.native.start_args['debug'] = False

            # Apply theme
            apply_theme(config.DARK_MODE)

            # Setup CSS hot reload in debug mode
            setup_css_hot_reload(config.DARK_MODE, config.DEBUG)

            # Create user interface
            self.create_ui()

            # Setup hotkey in background thread
            threading.Thread(
                target=self.setup_hotkey_delayed,
                daemon=True
            ).start()

            # Run NiceGUI
            self.log.info("Starting NiceGUI with hidden window...")
            self.log.info(f"Window will appear when you press {config.HOTKEY_COMBINATION}")

            ui.run(
                native=True,
                window_size=config.WINDOW_SIZE,
                title="🔥 Writing Assistant Pro (DEV MODE)" if config.DEBUG else _("Writing Assistant Pro"),
                reload=config.DEBUG,
                show=False
            )

        except KeyboardInterrupt:
            self.log.info("Application interrupted by user")
        except Exception as e:
            self.log.error(f"Application error: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.log.info("Cleaning up...")
        try:
            from src.core.styles import stop_css_hot_reload
            stop_css_hot_reload()
            keyboard.unhook_all()
        except Exception as e:
            self.log.debug(f"Cleanup error: {e}")
        self.log.info("Application stopped")
