import sys
from nicegui import ui, app
from styles import apply_theme
from logger import setup_logger
from ui import create_interface

# Récupère le flag DEBUG depuis les arguments de ligne de commande
# Utilisation: python main.py --debug
DEBUG = '--debug' in sys.argv

# Configurer le logger
log = setup_logger(debug=DEBUG)

# ===== CONFIGURATION DU THÈME =====
DARK_MODE = False  # Mettre à True pour activer le mode sombre

# Configuration de la fenêtre native
app.native.window_args['resizable'] = True
app.native.window_args['frameless'] = False  # True pour sans bordure
app.native.start_args['debug'] = DEBUG

log.info(f"Configuration: DEBUG={DEBUG}, DARK_MODE={DARK_MODE}")


def main():
    """Lance l'application"""
    # Appliquer le thème
    apply_theme(DARK_MODE)
    
    # Créer l'interface
    create_interface(log)


# Créer l'interface
main()

# Lance en mode NATIF (pas dans le navigateur!)
ui.run(
    native=True,           # ← C'EST LE PARAMÈTRE CLÉ
    window_size=(800, 600),
    title=("Mon Application (DEV MODE)" if DEBUG else "Mon Application"),
    reload=True if DEBUG else False  # Rechargement à chaud en mode dev
)