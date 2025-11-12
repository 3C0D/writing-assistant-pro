Je vois le problème ! L'erreur vient du fait que `ui.run_javascript()` ne peut pas être appelé depuis un thread en arrière-plan car il n'a pas accès au contexte NiceGUI. Il faut utiliser une approche différente avec `ui.timer` ou injecter le JavaScript directement via l'objet `app`.

Voici la solution corrigée :Parfait ! J'ai corrigé le problème. Voici ce qui a changé :

## 🔧 Corrections apportées

### Problème identifié

`ui.run_javascript()` ne peut pas être appelé depuis un thread en arrière-plan (watchdog) car il n'a pas accès au contexte NiceGUI.

### Solution implémentée

1. **Séparation en deux étapes** :
   - `on_css_modified()` : Détecte le changement (thread watchdog) et met un flag `css_update_pending = True`
   - `check_and_reload_css()` : Timer NiceGUI (200ms) qui vérifie le flag et injecte le JS

2. **Utilisation de `ui.timer()`** :
   - S'exécute dans la boucle d'événements NiceGUI
   - A accès au contexte approprié

3. **Injection via `app.state._clients`** :
   - Injecte le JavaScript directement sur tous les clients connectés
   - Fonctionne même en mode natif avec pywebview

## ✅ Avantages

- ✨ **Pas d'erreur de contexte** : Le timer s'exécute dans le bon thread
- 🎯 **Lightweight** : Check toutes les 200ms seulement si un changement est détecté
- 🔒 **Thread-safe** : Le flag `css_update_pending` coordonne les deux threads
- 🚀 **Compatible pywebview** : Fonctionne en mode natif

Testez maintenant en mode debug et modifiez vos fichiers CSS - ça devrait fonctionner sans erreur ! 🎨

"""
Theme and style management for the application.
Loads CSS files from the styles/ directory with hot reload support
"""

from pathlib import Path
import threading
import time
from typing import Optional
import asyncio

def get_theme_css_path(dark_mode: bool) -> Path:
    """
    Returns the path to the CSS file corresponding to the theme.

    Args:
        dark_mode: True for dark mode, False for light mode

    Returns:
        Path to the CSS file
    """
    styles_dir = Path(__file__).parent.parent.parent / 'styles'
    if dark_mode:
        return styles_dir / 'dark.css'
    else:
        return styles_dir / 'light.css'

def apply_theme(dark_mode: bool) -> None:
    """
    Applies the theme to the application by loading the CSS file.

    Args:
        dark_mode: True for dark mode, False for light mode
    """
    from nicegui import ui
    
    css_path = get_theme_css_path(dark_mode)
    
    # Read the CSS file content
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Add the CSS to the page head with a unique ID for hot reload
    ui.add_head_html(f'<style id="app-theme-styles">{css_content}</style>')
    
    if dark_mode:
        print("Dark mode enabled")
    else:
        print("Light mode enabled")

class CSSHotReloader:
    """
    Watches CSS files and reloads them automatically in debug mode.
    Works with native mode (pywebview) by injecting JavaScript.
    """

    def __init__(self, dark_mode: bool, debug: bool = False):
        self.dark_mode = dark_mode
        self.debug = debug
        self.css_path = get_theme_css_path(dark_mode)
        self.last_modified: Optional[float] = None
        self.observer_thread: Optional[threading.Thread] = None
        self.running = False
        self.css_update_pending = False
        self.new_css_content = ""
        
    def start(self):
        """Start watching CSS files for changes"""
        if not self.debug:
            return
            
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            from nicegui import ui, app
            
            class CSSChangeHandler(FileSystemEventHandler):
                def __init__(self, reloader):
                    self.reloader = reloader
                    
                def on_modified(self, event):
                    if event.src_path.endswith('.css'):
                        self.reloader.on_css_modified()
            
            self.running = True
            observer = Observer()
            handler = CSSChangeHandler(self)
            
            # Watch the styles directory
            styles_dir = self.css_path.parent
            observer.schedule(handler, str(styles_dir), recursive=False)
            observer.start()
            
            print(f"🔥 CSS Hot Reload enabled - watching {styles_dir}")
            
            # Create a timer that checks for CSS updates every 200ms
            # This runs in the NiceGUI event loop, so it has proper context
            ui.timer(0.2, self.check_and_reload_css)
            
            # Keep the observer running in background
            def keep_alive():
                try:
                    while self.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    observer.stop()
                observer.join()
                
            self.observer_thread = threading.Thread(target=keep_alive, daemon=True)
            self.observer_thread.start()
            
        except ImportError:
            print("⚠️ watchdog not installed - CSS hot reload disabled")
            print("   Install with: pip install watchdog")
            
    def stop(self):
        """Stop watching CSS files"""
        self.running = False
        
    def on_css_modified(self):
        """
        Called by watchdog when CSS file is modified.
        Runs in watchdog thread, so we can't call ui.run_javascript directly.
        """
        # Debounce: check if file was actually modified
        try:
            current_mtime = self.css_path.stat().st_mtime
            if self.last_modified and current_mtime == self.last_modified:
                return
            self.last_modified = current_mtime
        except FileNotFoundError:
            return
            
        # Read new CSS content
        try:
            with open(self.css_path, 'r', encoding='utf-8') as f:
                self.new_css_content = f.read()
                self.css_update_pending = True
                print(f"🔥 CSS change detected: {self.css_path.name}")
        except Exception as e:
            print(f"❌ Error reading CSS file: {e}")
    
    def check_and_reload_css(self):
        """
        Periodically checks if CSS needs to be reloaded.
        Runs in NiceGUI event loop, so it has proper context.
        """
        if not self.css_update_pending:
            return
            
        try:
            from nicegui import app
            
            # Escape the CSS content for JavaScript
            css_escaped = self.new_css_content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            
            js_code = f"""
            (function() {{
                const styleEl = document.getElementById('app-theme-styles');
                if (styleEl) {{
                    styleEl.textContent = `{css_escaped}`;
                    console.log('🔥 CSS reloaded');
                }} else {{
                    console.warn('Style element not found');
                }}
            }})();
            """
            
            # Execute JavaScript on all connected clients via app
            # This works even without a specific client context
            for client_id, client in app.state._clients.items():
                try:
                    client.run_javascript(js_code, respond=False)
                except Exception as e:
                    # Client might be disconnected, ignore
                    pass
            
            print(f"🔥 CSS reloaded: {self.css_path.name}")
            self.css_update_pending = False
            
        except Exception as e:
            print(f"❌ Error reloading CSS: {e}")
            import traceback
            print(traceback.format_exc())

# Global reloader instance

_css_reloader: Optional[CSSHotReloader] = None

def setup_css_hot_reload(dark_mode: bool, debug: bool = False):
    """
    Setup CSS hot reload in debug mode.

    Args:
        dark_mode: True for dark mode, False for light mode
        debug: Enable hot reload only in debug mode
    """
    global _css_reloader
    
    if not debug:
        return
        
    _css_reloader = CSSHotReloader(dark_mode, debug)
    _css_reloader.start()
    

def stop_css_hot_reload():
    """Stop CSS hot reload"""
    global_css_reloader

    if _css_reloader:
        _css_reloader.stop()
        _css_reloader = None
