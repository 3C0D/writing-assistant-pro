"""
Theme and style management for the application.
Loads CSS files from the styles/ directory
"""

from pathlib import Path


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
    
    # Add the CSS to the page head
    ui.add_head_html(f'<style>{css_content}</style>')
    
    if dark_mode:
        print("Dark mode enabled")
    else:
        print("Light mode enabled")
