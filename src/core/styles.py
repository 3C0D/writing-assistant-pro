"""
Theme and style management for the application.
Loads CSS files from the styles/ directory with hot reload support
"""

from __future__ import annotations

import threading
import time
import traceback

# Standard library imports
from pathlib import Path

from loguru import logger

# Third-party imports
from nicegui import ui

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

log = logger.bind(name="WritingAssistant.Styles")


def get_theme_css_path(dark_mode: bool) -> Path:
    """
    Returns the path to the CSS file corresponding to the theme.

    Args:
        dark_mode: True for dark mode, False for light mode

    Returns:
        Path to the CSS file
    """
    styles_dir = Path(__file__).parent.parent.parent / "styles"
    if dark_mode:
        return styles_dir / "dark.css"
    else:
        return styles_dir / "light.css"


def apply_theme(dark_mode: bool) -> None:
    """
    Applies the theme to the application by loading the CSS file.

    Args:
        dark_mode: True for dark mode, False for light mode
    """
    css_path = get_theme_css_path(dark_mode)

    # Read the CSS file content
    with open(css_path, encoding="utf-8") as f:
        css_content = f.read()

    # Add the CSS to the page head with a unique ID for hot reload
    ui.add_head_html(f'<style id="app-theme-styles">{css_content}</style>')

    if dark_mode:
        log.info("Dark mode enabled")
    else:
        log.info("Light mode enabled")


def set_theme(dark_mode: bool) -> None:
    """
    Updates the theme dynamically for connected clients.

    Args:
        dark_mode: True for dark mode, False for light mode
    """
    css_path = get_theme_css_path(dark_mode)

    try:
        with open(css_path, encoding="utf-8") as f:
            css_content = f.read()

        # Escape the CSS content for JavaScript
        css_escaped = css_content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

        js_code = f"""
        (function() {{
            const styleEl = document.getElementById('app-theme-styles');
            if (styleEl) {{
                styleEl.textContent = `{css_escaped}`;
            }} else {{
                // If element doesn't exist (shouldn't happen if apply_theme was called), create it
                const newStyle = document.createElement('style');
                newStyle.id = 'app-theme-styles';
                newStyle.textContent = `{css_escaped}`;
                document.head.appendChild(newStyle);
            }}
        }})();
        """

        ui.run_javascript(js_code)
        log.info(f"Theme updated to {'Dark' if dark_mode else 'Light'}")

    except Exception as e:
        log.error(f"Error setting theme: {e}")


class CSSHotReloader:
    """
    Watches CSS files and reloads them automatically in debug mode.
    Works with native mode (pywebview) by injecting JavaScript.
    """

    def __init__(self, dark_mode: bool, debug: bool = False):
        self.dark_mode = dark_mode
        self.debug = debug
        self.css_path = get_theme_css_path(dark_mode)
        self.last_modified: float | None = None
        self.observer_thread: threading.Thread | None = None
        self.running = False
        self.css_update_pending = False
        self.new_css_content = ""

    def start(self):
        """Start watching CSS files for changes"""
        if not self.debug:
            return

        if not WATCHDOG_AVAILABLE:
            log.warning("⚠️ watchdog not installed - CSS hot reload disabled")
            log.warning("   Install with: pip install watchdog")
            return

        self.running = True
        observer = Observer()
        handler = CSSChangeHandler(self)

        # Watch the styles directory
        styles_dir = self.css_path.parent
        observer.schedule(handler, str(styles_dir), recursive=False)
        observer.start()

        log.info(f"🔥 CSS Hot Reload enabled - watching {styles_dir}")

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
            with open(self.css_path, encoding="utf-8") as f:
                self.new_css_content = f.read()
                self.css_update_pending = True
                log.info(f"🔥 CSS change detected: {self.css_path.name}")
        except Exception as e:
            log.error(f"❌ Error reading CSS file: {e}")

    def check_and_reload_css(self):
        """
        Periodically checks if CSS needs to be reloaded.
        Runs in NiceGUI event loop, so it has proper context.
        """
        if not self.css_update_pending:
            return

        try:
            # Escape the CSS content for JavaScript
            css_escaped = (
                self.new_css_content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
            )

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

            # Execute JavaScript on all connected clients
            # This automatically runs on all clients when called from UI context
            ui.run_javascript(js_code)

            log.info(f"🔥 CSS reloaded: {self.css_path.name}")
            self.css_update_pending = False

        except Exception as e:
            log.error(f"❌ Error reloading CSS: {e}")
            log.error(traceback.format_exc())


class CSSChangeHandler(FileSystemEventHandler):
    """
    File system event handler for CSS file changes.
    """

    def __init__(self, reloader):
        self.reloader = reloader

    def on_modified(self, event):
        if str(event.src_path).endswith(".css"):
            self.reloader.on_css_modified()


# Global reloader instance
_css_reloader: CSSHotReloader | None = None


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
    global _css_reloader

    if _css_reloader:
        _css_reloader.stop()
        _css_reloader = None
