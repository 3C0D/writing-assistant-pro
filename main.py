"""
Application entry point for Writing Assistant Pro
"""

import sys
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
app.native.start_args['debug'] = DEBUG

log.info(f"{_('Configuration: DEBUG=')}{DEBUG}, DARK_MODE={DARK_MODE}")


def main():
    """Lance l'application"""
    # Apply theme
    apply_theme(DARK_MODE)
    
    # Create interface
    create_interface(log)


if __name__ in {'__main__', '__mp_main__'}:
    # Créer l'interface
    main()

    # Launch in NATIVE mode (not in browser!)
    ui.run(
        native=True,
        window_size=(800, 600),
        title=_("Writing Assistant Pro (DEV MODE)") if DEBUG else _("Writing Assistant Pro"),
        reload=True if DEBUG else False  # Hot reload in dev mode
    )
