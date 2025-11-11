"""
Module UI - Crée les pages et composants de l'interface
"""

from nicegui import ui


def create_interface(logger):
    """
    Crée l'interface utilisateur principale.
    
    Args:
        logger: Instance du logger pour afficher les logs
    """
    
    def on_button_click():
        """Callback pour le bouton."""
        logger.debug("Bouton cliqué!")
        ui.notify('Clicked!!!')
    
    # Ton interface
    ui.label('Hello, ceci est une vraie app desktop!')
    ui.button('Click me', on_click=on_button_click)
    
    logger.debug("Interface créée avec succès")
