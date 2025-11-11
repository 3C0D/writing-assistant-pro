"""
UI Module - Creates pages and interface components
"""

from nicegui import ui
from src.core.translation import _, change_language, get_current_language


def create_interface(logger):
    """
    Creates the main user interface.
    
    Args:
        logger: Logger instance for displaying logs
    """
    
    # Store references to UI elements that need updating
    ui_elements = {}
    
    def on_button_click():
        """Button click callback."""
        logger.debug("Button clicked!")
        ui.notify(_('Clicked!!!'))
    
    def update_all_text():
        """Update all text elements with new translations."""
        ui_elements['label_main'].text = _('Hello, this is a real desktop app!')
        ui_elements['button_main'].text = _('Click me')
        ui_elements['label_lang'].text = _("Language") + ":"
    
    # Language selector
    with ui.row():
        ui_elements['label_lang'] = ui.label(_("Language") + ":")
        language_select = ui.select(
            options={"en": _("English"), "fr": _("Français"), "it": _("Italiano")},
            value=get_current_language(),
            on_change=lambda e: change_language_handler(e.value)
        )
    
    def change_language_handler(lang):
        """Handle language change."""
        change_language(lang)
        language_select.set_value(lang)
        update_all_text()
        ui.notify(f"Language changed to {lang}")
    
    # Main interface
    ui_elements['label_main'] = ui.label(_('Hello, this is a real desktop app!'))
    ui_elements['button_main'] = ui.button(_('Click me'), on_click=on_button_click)
    
    logger.debug(_("Interface created successfully"))
