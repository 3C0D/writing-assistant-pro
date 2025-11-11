# Translation Management System - Writing Assistant Pro

This folder contains all the tools needed to manage translations for the Writing Assistant Pro application, adapted for UV and the current project structure.

## 📋 Overview

The translation system uses gettext and supports multiple languages. Translations are automatically extracted from Python code, translated, then compiled for runtime use.

## 🗂️ Files

### Main Scripts
- `extract_translations.py` - Extract translatable strings from codebase
- `sync_translations.py` - Sync all .po files from template.pot
- `compile_translations.py` - Compile .po files to .mo format

### Translation Files Structure
```
translations/
├── template.pot          # Translation template
├── en/LC_MESSAGES/
│   ├── writing_assistant.po/.mo   # English (reference)
├── fr/LC_MESSAGES/
│   └── writing_assistant.po/.mo   # French
└── it/LC_MESSAGES/
    └── writing_assistant.po/.mo   # Italian
```

## 🚀 Complete Workflow

### 1. Extract Strings
```bash
uv run python scripts/translation_management/extract_translations.py
```
Scans all `src/` code and finds `_()` calls. Updates `translations/template.pot`.

### 2. Add New Language
```bash
# Create directory
mkdir -p translations/zh/LC_MESSAGES

# Copy template
cp translations/template.pot translations/zh/LC_MESSAGES/writing_assistant.po
```

### 3. Sync .po Files from Template
```bash
# Automatically syncs all .po files from template.pot
uv run python scripts/translation_management/sync_translations.py
```

### 4. Translate New Strings
Edit the `.po` files manually or use translation tools. The sync process preserves existing translations.

### 5. Compile
```bash
# Compile specific language
uv run python scripts/translation_management/compile_translations.py fr

# Compile all languages
uv run python scripts/translation_management/compile_translations.py

# List available languages
uv run python scripts/translation_management/compile_translations.py --list
```

## 🔧 Script Details

### extract_translations.py
- **Role**: Automatic scan of Python code
- **Input**: `src/` directory
- **Output**: `translations/template.pot`
- **Utility**: Essential for Windows (replaces xgettext)

### sync_translations.py
- **Role**: Syncs all .po files from template.pot
- **Input**: `translations/template.pot`
- **Output**: Updates all `translations/*/LC_MESSAGES/writing_assistant.po`
- **Utility**: Keeps existing translations, adds/removes automatically

### compile_translations.py
- **Role**: Compile .po → .mo (binary format)
- **Utility**: .mo files are used by Python gettext
- **Fallback**: Manual implementation if msgfmt not available

## 🔄 Maintenance

### Adding New Strings:
1. Add `_()` calls in code
2. `extract_translations.py` → updates .pot
3. `sync_translations.py` → syncs all .po files
4. Translate new strings in .po files
5. `compile_translations.py`

### New Language:
1. Create `translations/xx/LC_MESSAGES/` directory
2. Copy `template.pot` → `writing_assistant.po`
3. `sync_translations.py` → syncs automatically
4. Translate the strings
5. `compile_translations.py`

## ⚠️ Important Notes

- **Backups**: Always backup custom translations before modifications
- **Context**: Automatic translations may lack UI context
- **Length**: Check that translations don't exceed UI space
- **Terminology**: Adapt to each language's conventions
- **Testing**: Test language changes in the application

## 🏗️ Technical Details

### Dependencies
- Python 3.8+ (with UV)
- gettext support (included with Python)
- Optional: `msgfmt` for faster compilation

### Project Structure
- Uses `translations/` directory (not `locales/`)
- Template file: `template.pot` (not `messages.pot`)
- Adapted for UV execution
- Compatible with current project architecture

### UV Integration
All scripts are designed to work with UV:
```bash
# Use UV to run scripts
uv run python scripts/translation_management/extract_translations.py
uv run python scripts/translation_management/sync_translations.py
uv run python scripts/translation_management/compile_translations.py
```

## 🔄 Migration from Old System

The new system replaces `scripts/compile_translations_final.py` with a complete workflow:
- **Old**: Single compilation script
- **New**: Complete extraction, sync, and compilation workflow
- **Benefits**: Better maintainability, UV compatibility, and workflow integration

## 📖 Usage Examples

### Quick Start
```bash
# 1. Extract all translatable strings
uv run python scripts/translation_management/extract_translations.py

# 2. Sync existing language files
uv run python scripts/translation_management/sync_translations.py

# 3. Compile for all languages
uv run python scripts/translation_management/compile_translations.py
```

### Language Management
```bash
# Add German support
mkdir -p translations/de/LC_MESSAGES
cp translations/template.pot translations/de/LC_MESSAGES/writing_assistant.po

# Sync and compile
uv run python scripts/translation_management/sync_translations.py
uv run python scripts/translation_management/compile_translations.py de
```

This system provides a complete, maintainable translation workflow adapted for modern development with UV.