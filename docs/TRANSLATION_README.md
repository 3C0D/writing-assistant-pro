# Translation System - Writing Assistant Pro

## Overview

This document describes the complete implementation of the translation system for the Writing Assistant Pro application, specifically adapted for NiceGUI.

## Implemented Structure

### 1. Language Configuration in main.py

```python
# Language configuration
LANGUAGE = "en"  # Default language
LANGUAGE_CHOICES = ["en", "fr", "it"]  # Available languages
```

### 2. Translation Module (translation.py)

- **LanguageManager**: Main translation manager
- **Gettext Support**: Use of the gettext standard for translations
- **UI Callbacks**: Automatic UI update system
- **Fallback**: Automatic handling of missing languages

### 3. Directory Structure

```
translations/
├── en/LC_MESSAGES/
│   └── writing_assistant.mo    # English compiled translations
├── fr/LC_MESSAGES/
│   └── writing_assistant.mo    # French compiled translations
└── it/LC_MESSAGES/
    └── writing_assistant.mo    # Italian compiled translations
```

### 4. User Interface (ui/**init**.py)

- Integrated language selector
- Dynamic text updates
- Support for callbacks for language changes

## Usage

### In Python Code

```python
from translation import _, change_language, get_current_language

# Translate text
text = _("Hello, this is a real desktop app!")

# Change language
change_language("fr")

# Get current language
current_lang = get_current_language()
```

### In Templates/Markup

```python
ui.label(_('Click me'))
ui.button(_('Click me'), on_click=callback)
```

## Supported Languages

- **English (en)** - Default language
- **French (fr)** - Complete translations
- **Italian (it)** - Complete translations

## Available Translations

### Interface

- "My Application" / "Mon Application" / "La Mia Applicazione"
- "Click me" / "Cliquez-moi" / "Cliccami"
- "Hello, this is a real desktop app!" / "Bonjour, ceci est une vraie app desktop!" / "Ciao, questa è una vera applicazione desktop!"
- "Language" / "Langue" / "Lingua"

### Configuration

- "Configuration: DEBUG=" / "Configuration : DEBUG=" / "Configurazione: DEBUG="
- "Interface created successfully" / "Interface créée avec succès" / "Interfaccia creata con successo"

### System Messages

- "Error" / "Erreur" / "Errore"
- "Success" / "Succès" / "Successo"
- "Warning" / "Avertissement" / "Avviso"
- "Information" / "Information" / "Informazione"

## Compiling Translations

To make translations work, you need to run the update script which extracts, updates, and compiles the translation files:

```bash
uv run python scripts/translation_management/update_translations.py
```

This script:

1. Extracts translatable strings from the source code
2. Updates or initializes translation files (.po)
3. Compiles to binary format (.mo)

## Advanced Features

### UI Callbacks

```python
from translation import register_ui_update

def refresh_interface():
    # Code to refresh the interface
    pass

register_ui_update(refresh_interface)
```

### Invalid Language Handling

The system automatically handles unsupported languages by falling back to the default language.

### Extensibility

To add a new language:

1. First, run the update script to ensure the template.pot is up to date with all current translatable strings:
   `uv run python scripts/translation_management/update_translations.py`
2. Modify the script to add the new language code to the `languages` list (e.g., add "es" for Spanish)
3. Run the update script again to initialize the new language files
4. Edit the generated .po file in the new language directory to add translations
5. Add the language code to `LANGUAGE_CHOICES` in `main.py`
6. Add the language name in `get_language_name()` in `translation.py`

## Technical Notes

- Uses the gettext standard for compatibility
- Full support for accents and special characters
- Automatic fallback in case of errors
- Compatible with NiceGUI and native interfaces
- Support for callbacks for dynamic updates

## Dependencies

- Python 3.13+
- Babel (for translation management)
- Gettext (included with Python)
- NiceGUI (for the main application)

The translation system is now fully integrated and functional in the Writing Assistant Pro application.
