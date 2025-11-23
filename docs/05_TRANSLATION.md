# Système de Traduction (i18n)

## 📋 Vue d'ensemble

Le projet utilise **gettext** et **Babel** pour l'internationalisation (i18n). Le système permet de traduire l'interface utilisateur dans plusieurs langues avec un workflow automatisé.

## 🎯 Objectifs

- Support multi-langues (9 langues actuellement)
- Workflow automatisé d'extraction/compilation
- Changement de langue dynamique
- Fallback automatique vers l'anglais
- Gestion centralisée des traductions

## 🏗️ Architecture

### Fichiers Principaux

| Fichier                                                                                                             | Rôle                               |
| ------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| [`src/core/services/translation.py`](../src/core/services/translation.py)                                           | Gestionnaire de traductions        |
| [`babel.cfg`](../babel.cfg)                                                                                         | Configuration Babel                |
| [`scripts/translation_management/update_translations.py`](../scripts/translation_management/update_translations.py) | Script de mise à jour              |
| `translations/`                                                                                                     | Dossier des fichiers de traduction |

### Structure des Traductions

```
translations/
├── template.pot              # Template (source de vérité)
├── en/LC_MESSAGES/
│   ├── writing_assistant.po  # Fichier éditable (anglais)
│   └── writing_assistant.mo  # Fichier compilé (binaire)
├── fr/LC_MESSAGES/
│   ├── writing_assistant.po  # Fichier éditable (français)
│   └── writing_assistant.mo  # Fichier compilé (binaire)
└── [autres langues...]
```

## 🌍 Langues Supportées

| Code | Langue    | Nom Local |
| ---- | --------- | --------- |
| `en` | Anglais   | English   |
| `fr` | Français  | Français  |
| `it` | Italien   | Italiano  |
| `es` | Espagnol  | Español   |
| `de` | Allemand  | Deutsch   |
| `pt` | Portugais | Português |
| `ru` | Russe     | Русский   |
| `zh` | Chinois   | 中文      |
| `ja` | Japonais  | 日本語    |

## 🔧 Utilisation

### Dans le Code

#### Marquer les Chaînes à Traduire

```python
from src.core.translation import _

# Texte simple
label = _("Hello, World!")

# Texte avec variables (f-string APRÈS traduction)
name = "John"
message = _("Welcome, {name}").format(name=name)

# Ou avec %
message = _("Welcome, %s") % name
```

#### Initialiser le Système

```python
from src.core.translation import init_translation

# Au démarrage de l'application
lang_manager = init_translation(
    app_name="writing_assistant",
    locales_dir="translations",
    default_language="en",
    available_languages=["en", "fr", "it"]
)
```

#### Changer de Langue

```python
from src.core.translation import change_language

# Changer vers le français
change_language("fr")

# L'UI se met à jour automatiquement
```

#### Obtenir la Langue Actuelle

```python
from src.core.translation import get_current_language

current = get_current_language()
print(f"Current language: {current}")  # "fr"
```

## 📝 Workflow de Traduction

### 1. Marquer les Textes dans le Code

```python
# ❌ Mauvais
ui.label("Welcome")

# ✅ Bon
ui.label(_("Welcome"))
```

### 2. Extraire les Chaînes

```bash
uv run python scripts/translation_management/update_translations.py
```

**Ce que fait le script** :

1. ✅ Extrait toutes les chaînes marquées `_("")`
2. ✅ Met à jour `template.pot`
3. ✅ Met à jour tous les fichiers `.po`
4. ✅ Compile les fichiers `.mo`

### 3. Éditer les Traductions

Ouvrir les fichiers `.po` et ajouter les traductions :

```po
# translations/fr/LC_MESSAGES/writing_assistant.po

#: src/ui/app.py:45
msgid "Welcome"
msgstr "Bienvenue"

#: src/ui/app.py:67
msgid "Settings"
msgstr "Paramètres"
```

### 4. Recompiler

```bash
uv run python scripts/translation_management/update_translations.py
```

### 5. Redémarrer l'Application

```bash
uv run python scripts/dev_build/run_dev.py
```

## ⚙️ Configuration

### babel.cfg

```ini
[python: **.py]
encoding = utf-8
```

**Explication** :

- `[python: **.py]` : Extraire de tous les fichiers `.py`
- `encoding = utf-8` : Encodage UTF-8

### Langues Disponibles

Modifier dans `src/core/services/translation.py` :

```python
available_languages = ["en", "fr", "it", "es", "de"]
```

## 🚀 Exemples Concrets

### Exemple 1 : Texte Simple

```python
from src.core.translation import _

# Dans le code
ui.label(_("Hello"))

# Dans translations/fr/LC_MESSAGES/writing_assistant.po
msgid "Hello"
msgstr "Bonjour"
```

### Exemple 2 : Texte avec Variables

```python
from src.core.translation import _

# Dans le code
name = "Marie"
ui.label(_("Welcome, {name}").format(name=name))

# Dans translations/fr/LC_MESSAGES/writing_assistant.po
msgid "Welcome, {name}"
msgstr "Bienvenue, {name}"
```

### Exemple 3 : Pluriels (Non Implémenté)

```python
# Futur : Support des pluriels
# ngettext("1 file", "{n} files", count).format(n=count)
```

### Exemple 4 : Changement de Langue Dynamique

```python
from src.core.translation import change_language, _

# Créer un sélecteur de langue
def on_language_change(lang):
    change_language(lang)
    # L'UI se met à jour automatiquement

ui.select(
    options=["en", "fr", "it"],
    value="en",
    on_change=lambda e: on_language_change(e.value)
)
```

## 🔍 Commandes Babel

### Extraction Manuelle

```bash
uv run pybabel extract -F babel.cfg -k _ -o translations/template.pot src/
```

### Initialiser une Nouvelle Langue

```bash
uv run pybabel init -d translations -i translations/template.pot -l es -D writing_assistant
```

### Mettre à Jour une Langue Existante

```bash
uv run pybabel update -d translations -i translations/template.pot -l fr -D writing_assistant
```

### Compiler les Traductions

```bash
uv run pybabel compile -d translations -D writing_assistant
```

## 📊 Détection Automatique

### Chemins Relatifs/Absolus

```python
# Le système détecte automatiquement si le chemin est absolu
path = Path(locales_dir)
if not path.is_absolute():
    self.locales_dir = get_app_root() / path
else:
    self.locales_dir = path
```

### Fallback Automatique

```python
# Si la langue n'existe pas, fallback vers "en"
if language not in self.available_languages:
    language = "en"
```

### Fichiers Manquants

```python
# Si les fichiers .mo n'existent pas, utilise NullTranslations
if locale_path.exists():
    translation = gettext.translation(...)
else:
    self._translations[language] = gettext.NullTranslations()
```

## ⚠️ Bonnes Pratiques

### 1. Toujours Utiliser `_()`

```python
# ❌ Mauvais
ui.label("Settings")

# ✅ Bon
ui.label(_("Settings"))
```

### 2. Variables Après Traduction

```python
# ❌ Mauvais
ui.label(_(f"Welcome, {name}"))

# ✅ Bon
ui.label(_("Welcome, {name}").format(name=name))
```

### 3. Contexte pour les Traducteurs

```python
# Ajouter des commentaires pour les traducteurs
# TRANSLATORS: This is the main welcome message
ui.label(_("Welcome"))
```

### 4. Éviter les Chaînes Dynamiques

```python
# ❌ Mauvais (ne sera pas extrait)
key = "welcome"
ui.label(_(key))

# ✅ Bon
ui.label(_("Welcome"))
```

### 5. Tester Toutes les Langues

```python
# Tester le changement de langue
for lang in ["en", "fr", "it"]:
    change_language(lang)
    # Vérifier l'UI
```

## 🔧 Dépannage

### Les Traductions n'Apparaissent Pas

**Vérifier** :

1. Les fichiers `.mo` sont compilés
2. La langue est bien dans `available_languages`
3. Le chemin `translations/` est correct
4. Les chaînes sont marquées avec `_()`

**Solution** :

```bash
# Recompiler les traductions
uv run python scripts/translation_management/update_translations.py

# Vérifier les fichiers .mo
ls translations/fr/LC_MESSAGES/
```

### Nouvelles Chaînes Non Traduites

**Cause** : Fichiers `.po` pas à jour

**Solution** :

```bash
# Mettre à jour les traductions
uv run python scripts/translation_management/update_translations.py

# Éditer les .po
# Recompiler
```

### Erreur "Translation not found"

**Cause** : Fichiers `.mo` manquants ou corrompus

**Solution** :

```bash
# Supprimer les .mo
find translations -name "*.mo" -delete

# Recompiler
uv run python scripts/translation_management/update_translations.py
```

## 📝 Format des Fichiers .po

### Structure

```po
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: 1.0\n"
"Language: fr\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/ui/app_flet.py:45
msgid "Welcome"
msgstr "Bienvenue"

#: src/ui/app_flet.py:67
msgid "Settings"
msgstr "Paramètres"
```

### Éléments

- `#:` : Emplacement dans le code source
- `msgid` : Texte original (anglais)
- `msgstr` : Traduction

## 🔗 Références

### Code Source

- [`src/core/services/translation.py`](../src/core/services/translation.py) - Gestionnaire de traductions
- [`scripts/translation_management/update_translations.py`](../scripts/translation_management/update_translations.py) - Script de mise à jour
- [`babel.cfg`](../babel.cfg) - Configuration Babel

### Documentation Externe

- [GNU gettext](https://www.gnu.org/software/gettext/)
- [Babel Documentation](https://babel.pocoo.org/)
- [Python gettext Module](https://docs.python.org/3/library/gettext.html)

## 🚧 Améliorations Futures

### Support des Pluriels

Implémenter `ngettext()` pour gérer les formes plurielles.

### Détection Automatique de la Langue

Détecter la langue du système au démarrage.

### Traductions Contextuelles

Utiliser `pgettext()` pour les traductions dépendant du contexte.

### Validation des Traductions

Vérifier que toutes les chaînes sont traduites.

### Interface de Traduction

Créer une UI pour éditer les traductions sans toucher aux fichiers `.po`.
