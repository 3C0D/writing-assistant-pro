Pour la fenêtre, c'est ouverte directement sans lancer le raccourci, puis après en ayant appuyé ce raccourci, elle s'est ouvert 3 fois.

😅 OK, on va reprendre les choses calmement. Le problème c'est que :

1. **NiceGUI en mode native ouvre TOUJOURS une fenêtre** dès le démarrage
2. **La librairie `keyboard` déclenche plusieurs fois** le même événement

Cherchons comment d'autres projets gèrent ça avec des fenêtres natives qui doivent rester cachées :Parfait ! J'ai trouvé comment faire avec pywebview. On peut créer une fenêtre cachée avec `hidden=True` et la montrer avec `window.show()`.

Voici la **vraie solution** qui utilise directement pywebview (que NiceGUI utilise en interne) :Le changement clé c'est :

```python
app.native.window_args['hidden'] = True  # Fenêtre cachée au démarrage
```

Puis on utilise l'API pywebview directement pour afficher la fenêtre :

```python
import webview
if webview.windows:
    window = webview.windows[0]
    window.show()
```

**Installation** :

Si tu veux utiliser la librairie `keyboard` (plus simple mais nécessite admin sur Windows) :
```bash
uv pip install keyboard
```

Sinon, garde `pynput` qui est déjà installé.

**Pour le problème des déclenchements multiples**, j'ai augmenté l'intervalle minimum à **2 secondes** et utilisé un lock thread-safe.

Teste cette version et dis-moi si :
1. La fenêtre reste cachée au démarrage ✅
2. Elle apparaît une seule fois quand tu appuies sur Ctrl+Space ✅
3. Plus de console DOS qui s'ouvre ✅

"""
Application entry point for Writing Assistant Pro
Uses hidden window that shows on Ctrl+Space hotkey
"""

import sys
import threading
import time
from nicegui import ui, app
from src.core import apply_theme, setup_logger, init_translation, _
from src.ui import create_interface

# Try keyboard library first, fallback to pynput
try:
    import keyboard
    USE_KEYBOARD = True
except ImportError:
    from pynput import keyboard as pynput_keyboard
    USE_KEYBOARD = False

# Language configuration
LANGUAGE = "fr"
DEBUG = '--debug' in sys.argv

# Initialize translation system
init_translation("writing_assistant", "translations", LANGUAGE)

# Configure logger
log = setup_logger(debug=DEBUG)

# Theme configuration
DARK_MODE = False

# Native window configuration - START HIDDEN
app.native.window_args['resizable'] = True
app.native.window_args['frameless'] = False
app.native.window_args['hidden'] = True  # THIS IS THE KEY!
app.native.start_args['debug'] = False

log.info(f"{_('Configuration: DEBUG=')}{DEBUG}, DARK_MODE={DARK_MODE}")


class HiddenWindowApp:
    """
    Application with hidden window that shows on hotkey
    """
    
    def __init__(self):
        self.log = setup_logger(debug=DEBUG, name="WritingAssistant")
        self.last_trigger_time = 0.0
        self.MIN_TRIGGER_INTERVAL = 2.0  # 2 seconds debounce
        self.trigger_lock = threading.Lock()
        self.window_ref = None
        
    def on_hotkey(self):
        """Callback when Ctrl+Space is pressed"""
        # Try to acquire lock without blocking
        if not self.trigger_lock.acquire(blocking=False):
            self.log.debug("Hotkey already processing, ignoring")
            return
        
        try:
            current_time = time.time()
            
            # Debounce check
            time_since_last = current_time - self.last_trigger_time
            if time_since_last < self.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return
                
            self.last_trigger_time = current_time
            self.log.info("Hotkey pressed - showing window")
            
            # Show the window
            self.show_window()
                
        finally:
            # Release lock after a delay
            def release_lock():
                time.sleep(0.5)
                self.trigger_lock.release()
                self.log.debug("Lock released")
            
            threading.Thread(target=release_lock, daemon=True).start()
    
    def show_window(self):
        """Show the native window"""
        try:
            # Access the native window through NiceGUI's app object
            # NiceGUI uses pywebview internally
            import webview
            
            # Get the webview window
            if webview.windows:
                window = webview.windows[0]
                self.log.info("Showing window...")
                window.show()
                self.log.info("Window shown")
            else:
                self.log.warning("No webview window found")
                
        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")
    
    def setup_hotkey_with_keyboard_lib(self):
        """Setup hotkey using 'keyboard' library"""
        try:
            keyboard.add_hotkey('ctrl+space', self.on_hotkey, suppress=False)
            self.log.info("Global hotkey registered with 'keyboard' library: Ctrl+Space")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey with keyboard library: {e}")
            return False
    
    def setup_hotkey_with_pynput(self):
        """Setup hotkey using 'pynput' library"""
        def on_press(key):
            try:
                # Check if it's a special key
                if hasattr(key, 'name'):
                    return
                # Check if it's space with ctrl held
                if key == pynput_keyboard.Key.space:
                    # Check if ctrl is held
                    # This is a simplified check - you might need to track ctrl state
                    self.on_hotkey()
            except AttributeError:
                pass
        
        try:
            # Use GlobalHotKeys for simpler management
            from pynput.keyboard import GlobalHotKeys
            
            hotkey = GlobalHotKeys({
                '<ctrl>+<space>': self.on_hotkey
            })
            hotkey.start()
            self.log.info("Global hotkey registered with 'pynput' library: Ctrl+Space")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey with pynput: {e}")
            return False
    
    def run(self):
        """Run the application"""
        try:
            # Apply theme
            apply_theme(DARK_MODE)
            
            # Create interface
            create_interface(log)
            
            # Setup hotkey in a background thread (must be after ui.run starts)
            def setup_hotkey_delayed():
                time.sleep(1)  # Wait for NiceGUI to initialize
                if USE_KEYBOARD:
                    success = self.setup_hotkey_with_keyboard_lib()
                else:
                    success = self.setup_hotkey_with_pynput()
                
                if success:
                    self.log.info("Press Ctrl+Space to show the window")
                else:
                    self.log.error("Failed to setup hotkey")
            
            threading.Thread(target=setup_hotkey_delayed, daemon=True).start()
            
            # Run NiceGUI in native mode with HIDDEN window
            self.log.info("Starting NiceGUI with hidden window...")
            self.log.info("Window will appear when you press Ctrl+Space")
            
            ui.run(
                native=True,
                window_size=(800, 600),
                title=_("Writing Assistant Pro (DEV MODE)") if DEBUG else _("Writing Assistant Pro"),
                reload=DEBUG,
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
        if USE_KEYBOARD:
            try:
                keyboard.remove_hotkey('ctrl+space')
                keyboard.unhook_all()
            except:
                pass
        self.log.info("Application stopped")


def main():
    """Main entry point"""
    app = HiddenWindowApp()
    app.run()


if __name__ in {'__main__', '__mp_main__'}:
    main()