#!/usr/bin/env python3
"""
Interface launcher for Writing Assistant Pro.
This script launches the NiceGUI interface in a separate process.
"""

import sys
import os
from nicegui import ui, app
from src.core import apply_theme, setup_logger, init_translation, _
from src.ui import create_interface

# Language configuration
LANGUAGE = "fr"  # Default language

# Récupère le flag DEBUG depuis les arguments de ligne de commande
DEBUG = '--debug' in sys.argv

# Initialize translation system BEFORE using _()
init_translation("writing_assistant", "translations", LANGUAGE)

# Configurer le logger
log = setup_logger(debug=DEBUG)

# ===== CONFIGURATION DU THÈME =====
DARK_MODE = False  # Mettre à True pour activer le mode sombre

# Configuration de la fenêtre native
app.native.window_args['resizable'] = True
app.native.window_args['frameless'] = False

# IMPORTANT: Always disable debug mode for native window to prevent dev tools window
app.native.start_args['debug'] = False

log.info(f"{_('Configuration: DEBUG=')}{DEBUG}, DARK_MODE={DARK_MODE}")

def main():
    """Launch the interface"""
    try:
        # Apply theme
        apply_theme(DARK_MODE)

        # Create interface
        create_interface(log)

        # Launch in NATIVE mode
        log.info("Launching interface window...")
        ui.run(
            native=True,
            window_size=(800, 600),
            title=_("Writing Assistant Pro (DEV MODE)") if DEBUG else _("Writing Assistant Pro"),
            reload=False,  # Always False to prevent file watching and reloading
            show=False  # Prevent browser window from opening
        )
        log.info("Interface window closed")

    except Exception as e:
        log.error(f"Error in interface launcher: {e}")
        import traceback
        log.debug(f"Full traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ in {"__main__", "__mp_main__"}:
    main()