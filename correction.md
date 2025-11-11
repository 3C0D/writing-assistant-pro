Je vois le problème. Quand tu fermes la fenêtre avec la croix ou Ctrl+Space, elle est **détruite** et non pas cachée. Et la "barre bleue" que tu vois c'est probablement une notification NiceGUI.

Le problème c'est que **pywebview ne permet pas vraiment d'empêcher la fermeture d'une fenêtre native**. Il faut une approche différente.

Cherchons comment d'autres projets gèrent ce problème :Parfait ! J'ai trouvé la solution ! Il faut utiliser `window.events.closing` pour intercepter la fermeture et retourner `False` pour empêcher la fermeture, puis cacher la fenêtre dans un thread séparé.

Voici la solution complète qui fonctionne :## Les changements clés

1. **`window.events.closing += self.on_closing`** : Intercepte l'événement de fermeture
2. **`on_closing()` retourne `False`** : Empêche la fermeture réelle de la fenêtre
3. **Hide dans un thread** : Évite le freeze mentionné dans le bug pywebview
4. **Initialisation unique** : Le handler de fermeture n'est enregistré qu'une seule fois

## Comportement attendu maintenant

- ✅ Démarrage : fenêtre cachée
- ✅ Ctrl+Space : fenêtre apparaît
- ✅ Cliquer sur la croix (X) : fenêtre se **cache** au lieu de se fermer
- ✅ Ctrl+Space à nouveau : fenêtre réapparaît
- ✅ Bouton "Hide" dans l'interface : cache la fenêtre
- ✅ Peut répéter le cycle indéfiniment

Teste cette version et dis-moi si maintenant la fenêtre se cache correctement au lieu de se fermer ! 🎯

"""
Application entry point for Writing Assistant Pro
Properly handles window hide/show with Ctrl+Space and prevents closing
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
    from pynput.keyboard import GlobalHotKeys
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
app.native.window_args['hidden'] = True
app.native.start_args['debug'] = False

log.info(f"{_('Configuration: DEBUG=')}{DEBUG}, DARK_MODE={DARK_MODE}")


class HiddenWindowApp:
    """
    Application with hidden window that shows/hides on hotkey
    Window close button hides instead of closing
    """
    
    def __init__(self):
        self.log = setup_logger(debug=DEBUG, name="WritingAssistant")
        self.last_trigger_time = 0.0
        self.MIN_TRIGGER_INTERVAL = 1.0
        self.trigger_lock = threading.Lock()
        self.window_ref = None
        self.window_visible = False
        self.window_initialized = False
        self.hotkey_handler = None
        
    def on_closing(self):
        """
        Handle window close event - hide instead of closing
        This prevents the window from being destroyed
        """
        def hide_in_thread():
            self.log.info("Window close requested - hiding instead")
            try:
                if self.window_ref:
                    self.window_ref.hide()
                    self.window_visible = False
                    self.log.info("Window hidden - Press Ctrl+Space to show again")
            except Exception as e:
                self.log.error(f"Error hiding window: {e}")
        
        # Hide in a separate thread to avoid blocking
        threading.Thread(target=hide_in_thread, daemon=True).start()
        
        # Return False to prevent actual closing
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
            if time_since_last < self.MIN_TRIGGER_INTERVAL:
                self.log.debug(f"Ignoring hotkey - too soon ({time_since_last:.2f}s)")
                return
                
            self.last_trigger_time = current_time
            
            # Toggle visibility
            if self.window_visible:
                self.hide_window()
            else:
                self.show_window()
                
        finally:
            # Release lock after a short delay
            def release_lock():
                time.sleep(0.3)
                self.trigger_lock.release()
                self.log.debug("Lock released")
            
            threading.Thread(target=release_lock, daemon=True).start()
    
    def show_window(self):
        """Show the native window"""
        try:
            import webview
            
            if webview.windows:
                window = webview.windows[0]
                
                # Store reference and setup close handler on first show
                if not self.window_initialized:
                    self.window_ref = window
                    self.window_initialized = True
                    
                    # CRITICAL: Register the closing event handler
                    window.events.closing += self.on_closing
                    self.log.info("Window close handler registered")
                
                self.log.info("Showing window...")
                window.show()
                self.window_visible = True
                self.log.info("Window shown - Close button or Ctrl+Space will hide it")
            else:
                self.log.warning("No webview window found")
                
        except Exception as e:
            self.log.error(f"Error showing window: {e}")
            import traceback
            self.log.debug(f"Full traceback: {traceback.format_exc()}")
    
    def hide_window(self):
        """Hide the native window"""
        try:
            if self.window_ref:
                self.log.info("Hiding window...")
                self.window_ref.hide()
                self.window_visible = False
                self.log.info("Window hidden - Press Ctrl+Space to show again")
            else:
                self.log.warning("No window reference available")
                
        except Exception as e:
            self.log.error(f"Error hiding window: {e}")
    
    def setup_hotkey_with_keyboard_lib(self):
        """Setup hotkey using 'keyboard' library"""
        try:
            keyboard.add_hotkey('ctrl+space', self.toggle_window, suppress=False)
            self.log.info("Global hotkey registered: Ctrl+Space (toggle window)")
            return True
        except Exception as e:
            self.log.error(f"Failed to register hotkey with keyboard library: {e}")
            return False
    
    def setup_hotkey_with_pynput(self):
        """Setup hotkey using 'pynput' library"""
        try:
            self.hotkey_handler = GlobalHotKeys({
                '<ctrl>+<space>': self.toggle_window
            })
            self.hotkey_handler.start()
            self.log.info("Global hotkey registered: Ctrl+Space (toggle window)")
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
            
            # Add hide button to interface header
            with ui.header().classes('items-center justify-between'):
                ui.label('Writing Assistant Pro').classes('text-h6')
                ui.button('Hide (Ctrl+Space)', 
                         on_click=lambda: self.hide_window(),
                         icon='visibility_off').props('flat dense')
            
            # Setup hotkey in a background thread
            def setup_hotkey_delayed():
                time.sleep(1.5)  # Wait for NiceGUI and pywebview to fully initialize
                if USE_KEYBOARD:
                    success = self.setup_hotkey_with_keyboard_lib()
                else:
                    success = self.setup_hotkey_with_pynput()
                
                if success:
                    self.log.info("Press Ctrl+Space to toggle window visibility")
                else:
                    self.log.error("Failed to setup hotkey")
            
            threading.Thread(target=setup_hotkey_delayed, daemon=True).start()
            
            # Run NiceGUI in native mode with HIDDEN window
            self.log.info("Starting NiceGUI with hidden window...")
            self.log.info("Press Ctrl+Space to show the window")
            
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
        else:
            if self.hotkey_handler:
                try:
                    self.hotkey_handler.stop()
                except:
                    pass
        self.log.info("Application stopped")


def main():
    """Main entry point"""
    app = HiddenWindowApp()
    app.run()


if __name__ in {'__main__', '__mp_main__'}:
    main()
    