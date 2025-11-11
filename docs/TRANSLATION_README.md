# Système de Traduction - Writing Assistant Pro

## Vue d'ensemble

Ce document décrit l'implémentation du système de traduction complet pour l'application Writing Assistant Pro, adapté spécifiquement pour NiceGUI.

## Structure implémentée

### 1. Configuration des langues dans main.py

```python
# Language configuration
LANGUAGE = "en"  # Default language
LANGUAGE_CHOICES = ["en", "fr", "it"]  # Available languages
```

### 2. Module de traduction (translation.py)

- **LanguageManager**: Gestionnaire principal des traductions
- **Support gettext**: Utilisation du standard gettext pour les traductions
- **Callbacks UI**: Système de mise à jour automatique de l'interface
- **Fallback**: Gestion automatique des langues manquantes

### 3. Structure des dossiers

```
locales/
├── en/LC_MESSAGES/
│   └── writing_assistant.po    # English translations
├── fr/LC_MESSAGES/
│   └── writing_assistant.po    # French translations
└── it/LC_MESSAGES/
    └── writing_assistant.po    # Italian translations
```

### 4. Interface utilisateur (ui/**init**.py)

- Sélecteur de langue intégré
- Mise à jour dynamique des textes
- Support des callbacks pour les changements de langue

## Utilisation

### Dans le code Python

```python
from translation import _, change_language, get_current_language

# Traduire du texte
text = _("Hello, this is a real desktop app!")

# Changer de langue
change_language("fr")

# Obtenir la langue actuelle
current_lang = get_current_language()
```

### Dans les templates/markup

```python
ui.label(_('Click me'))
ui.button(_('Click me'), on_click=callback)
```

## Langues supportées

- **Anglais (en)** - Langue par défaut
- **Français (fr)** - Traductions complètes
- **Italien (it)** - Traductions complètes

## Traductions disponibles

### Interface

- "My Application" / "Mon Application" / "La Mia Applicazione"
- "Click me" / "Cliquez-moi" / "Cliccami"
- "Hello, this is a real desktop app!" / "Bonjour, ceci est une vraie app desktop!" / "Ciao, questa è una vera applicazione desktop!"
- "Language" / "Langue" / "Lingua"

### Configuration

- "Configuration: DEBUG=" / "Configuration : DEBUG=" / "Configurazione: DEBUG="
- "Interface created successfully" / "Interface créée avec succès" / "Interfaccia creata con successo"

### Messages système

- "Error" / "Erreur" / "Errore"
- "Success" / "Succès" / "Successo"
- "Warning" / "Avertissement" / "Avviso"
- "Information" / "Information" / "Informazione"

## Compilation des traductions

Pour que les traductions fonctionnent, il faut compiler les fichiers .po en .mo :

```bash
# Utilisation de msgfmt (recommandé)
msgfmt -o locales/fr/LC_MESSAGES/writing_assistant.mo locales/fr/LC_MESSAGES/writing_assistant.po
msgfmt -o locales/it/LC_MESSAGES/writing_assistant.mo locales/it/LC_MESSAGES/writing_assistant.po
msgfmt -o locales/en/LC_MESSAGES/writing_assistant.mo locales/en/LC_MESSAGES/writing_assistant.po

# Ou utilisation du script Python
python compile_translations.py
```

## Tests

Un script de test est fourni pour vérifier le bon fonctionnement :

```bash
python test_translation.py
```

Ce script teste :

- La présence des fichiers de traduction
- Le fonctionnement du LanguageManager
- Le changement de langues
- Les traductions de base
- Les cas d'erreur

## Fonctionnalités avancées

### Callbacks UI

```python
from translation import register_ui_update

def refresh_interface():
    # Code pour actualiser l'interface
    pass

register_ui_update(refresh_interface)
```

### Gestion des langues invalides

Le système gère automatiquement les langues non supportées en revenant à la langue par défaut.

### Extensibilité

Pour ajouter une nouvelle langue :

1. Créer le dossier `locales/[code]/LC_MESSAGES/`
2. Créer le fichier `writing_assistant.po`
3. Ajouter le code à `LANGUAGE_CHOICES` dans `main.py`
4. Ajouter le nom dans `get_language_name()`

## Notes techniques

- Utilise le standard gettext pour la compatibilité
- Support complet des accents et caractères spéciaux
- Fallback automatique en cas d'erreur
- Compatible avec NiceGUI et les interfaces natives
- Support des callbacks pour mise à jour dynamique

## Dépendances

- Python 3.13+
- gettext (inclus avec Python)
- NiceGUI (pour l'application principale)

Le système de traduction est maintenant pleinement intégré et fonctionnel dans l'application Writing Assistant Pro.
