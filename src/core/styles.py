"""
Theme and style management for the application.
Loads CSS files from the styles/ directory
"""

from pathlib import Path


def get_theme_css_path(dark_mode: bool) -> Path:
    """
    Retourne le chemin du fichier CSS correspondant au thème.
    
    Args:
        dark_mode: True pour le mode sombre, False pour le mode clair
    
    Returns:
        Path vers le fichier CSS
    """
    styles_dir = Path(__file__).parent.parent.parent / 'styles'
    if dark_mode:
        return styles_dir / 'dark.css'
    else:
        return styles_dir / 'light.css'


def apply_theme(dark_mode: bool) -> None:
    """
    Applique le thème à l'application en chargeant le fichier CSS.
    
    Args:
        dark_mode: True pour le mode sombre, False pour le mode clair
    """
    from nicegui import ui
    
    css_path = get_theme_css_path(dark_mode)
    
    # Lire le contenu du fichier CSS
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Ajouter le CSS au head de la page
    ui.add_head_html(f'<style>{css_content}</style>')
    
    if dark_mode:
        print("Dark mode enabled")
    else:
        print("Light mode enabled")
