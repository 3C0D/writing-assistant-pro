"""
UI Module - Creates pages and interface components
"""

import logging
from nicegui import ui
from src.core import _, change_language, get_current_language


def create_interface():
    """
    Creates the main user interface.
    """
    logger = logging.getLogger("WritingAssistant.ui")
    
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
    
    def change_language_handler(lang):
        """Handle language change."""
        change_language(lang)
        language_select.set_value(lang)
        update_all_text()
        ui.notify(f"Language changed to {lang}")
    
    # Main interface - Create elements and store references
    with ui.column().classes('gap-4 p-4'):

        # Language selector section
        with ui.row().classes('items-center gap-2'):
            ui_elements['label_lang'] = ui.label(_("Language") + ":")
            language_select = ui.select(
                options={"en": _("English"), "fr": _("Français"), "it": _("Italiano")},
                value=get_current_language(),
                on_change=lambda e: change_language_handler(e.value)
            )

        # Main content section
        with ui.column().classes('gap-2'):
            ui_elements['label_main'] = ui.label(_('Hello, this is a real desktop app!'))
            ui_elements['button_main'] = ui.button(_('Click me'), on_click=on_button_click)
    
    logger.debug("Interface created successfully")