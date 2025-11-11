# 📁 Structure du projet - Writing Assistant Pro

## Vue d'ensemble

```
writing-assistant-pro/
│
├── main.py                          ← Point d'entrée (simple wrapper)
├── pyproject.toml                   ← Configuration du projet
├── babel.cfg                        ← Configuration Babel (extraction)
├── .babelrc                         ← Configuration Babel (init/update/compile)
│
├── src/                             ← Code source principal
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               ← Configuration app + point d'entrée réel
│   │   ├── logger.py               ← Logging centralisé
│   │   ├── styles.py               ← Gestion des thèmes
│   │   └── translation.py          ← Système de traduction (gettext)
│   └── ui/
│       └── __init__.py             ← Interface utilisateur
│
├── scripts/
│   ├── run_dev.py                  ← Launcher mode développement
│   └── translation_management/
│       ├── GUIDE.md                ← Guide complet des traductions
│       └── update_translations.py  ← Script unifié Babel
│
├── styles/
│   ├── light.css                   ← Thème clair
│   └── dark.css                    ← Thème sombre
│
├── translations/                   ← Fichiers de traduction
│   ├── template.pot                ← Template (source de vérité)
│   ├── en/LC_MESSAGES/
│   │   ├── writing_assistant.po    ← Traductions anglaises
│   │   └── writing_assistant.mo    ← Compilé (binaire)
│   ├── fr/LC_MESSAGES/
│   │   ├── writing_assistant.po    ← Traductions françaises
│   │   └── writing_assistant.mo    ← Compilé (binaire)
│   └── it/LC_MESSAGES/
│       ├── writing_assistant.po    ← Traductions italiennes
│       └── writing_assistant.mo    ← Compilé (binaire)
│
├── docs/
│   ├── CONFIG_BABEL.md             ← Configuration Babel expliquée
│   ├── STRUCTURE.md                ← Ce fichier
│   └── ...
│
├── .vscode/
│   └── settings.json               ← Configuration VS Code
│
├── README.md                        ← Quick start
├── QUICKSTART.md                    ← Guide rapide
├── ARCHITECTURE.md                  ← Architecture globale
│
├── tests/                           ← Tests unitaires (à développer)
└── .venv/                           ← Environnement virtuel (ignoré git)
```

## Explication des rôles

### Racine

- **`main.py`** : Simple wrapper qui importe `src.core.config`
  - Permet à l'utilisateur de faire `python main.py --debug`
  - Tout le vrai code est dans `src/core/config.py`

- **`babel.cfg`** : Configuration Babel pour l'extraction
  - Patterns des fichiers Python à scanner
  - Règles d'extraction

- **`.babelrc`** : Configuration Babel pour init/update/compile
  - Options de traduction
  - Définition du domaine et des chemins

### `src/core/`

**Logique métier et infrastructure**

- **`config.py`** : Point d'entrée réel de l'application
  - Configuration globale (DEBUG, DARK_MODE, LANGUAGE)
  - Initialisation du système (traductions, logger, thème)
  - Appel à `ui.run()`

- **`logger.py`** : Logging centralisé
  - Configuration du logging en DEBUG ou PRODUCTION
  - Réutilisable partout via `from src.core.logger import setup_logger`

- **`styles.py`** : Gestion des thèmes CSS
  - Charge les fichiers CSS selon le mode (light/dark)
  - Injecte le CSS dans NiceGUI

- **`translation.py`** : Système de traduction gettext
  - Classe `LanguageManager` pour gérer les langues
  - Fonctions `_()` pour marquer les textes
  - Fonctions `change_language()` pour changer dynamiquement

### `src/ui/`

**Interface utilisateur**

- **`__init__.py`** : Crée et gère l'interface
  - Éléments NiceGUI (labels, buttons, selects)
  - Mise à jour automatique des traductions
  - Gestion des événements utilisateur

### `scripts/`

**Outils et scripts utilitaires**

- **`run_dev.py`** : Launcher du mode développement
  - Lance `main.py --debug` avec hot reload

- **`translation_management/update_translations.py`** : Script unifié Babel
  - Extraction + Synchronisation + Compilation en une commande
  - Usage : `uv run python scripts/translation_management/update_translations.py`

### `styles/`

**Thèmes CSS**

- **`light.css`** : Thème clair (par défaut)
- **`dark.css`** : Thème sombre

Chargés dynamiquement selon `DARK_MODE` dans `config.py`

### `translations/`

**Fichiers de traduction**

- **`template.pot`** : Template général (généré automatiquement)
- **`xx/LC_MESSAGES/writing_assistant.po`** : Traductions éditables
- **`xx/LC_MESSAGES/writing_assistant.mo`** : Traductions compilées (binaire)

Pour ajouter une langue :

```bash
mkdir -p translations/de/LC_MESSAGES
cp translations/template.pot translations/de/LC_MESSAGES/writing_assistant.po
# Éditer le .po pour ajouter les traductions
uv run python scripts/translation_management/update_translations.py
```

### `docs/`

**Documentation**

- **`STRUCTURE.md`** (ce fichier) : Vue d'ensemble
- **`CONFIG_BABEL.md`** : Explication Babel
- **`ARCHITECTURE.md`** (racine) : Architecture globale
- **`QUICKSTART.md`** (racine) : Guide rapide
- **`README.md`** (racine) : Informations du projet

## Workflow de développement

### 1. Lancer l'app

```bash
uv run python scripts/run_dev.py
```

ou directement :

```bash
uv run python main.py --debug
```

### 2. Ajouter du texte translatable

```python
# Dans src/ui/__init__.py ou autre fichier
from src.core.translation import _

ui.label(_("Texte à traduire"))
```

### 3. Mettre à jour les traductions

```bash
uv run python scripts/translation_management/update_translations.py
```

### 4. Éditer les fichiers .po

```
# Ouvre le fichier et ajoute les traductions
translations/fr/LC_MESSAGES/writing_assistant.po
```

### 5. Relancer l'app

```bash
uv run python scripts/run_dev.py
```

La langue devrait se changer automatiquement via le sélecteur dans l'interface.

## Points clés

✅ **Modularité** : Code bien séparé dans `src/core/` et `src/ui/`  
✅ **Traductions** : Système Babel simples avec une seule commande  
✅ **Thèmes** : CSS externe, facile à modifier  
✅ **Logging** : Centralisé, facile à réutiliser  
✅ **Structure propre** : Fichiers à la bonne place  

## Prochaines étapes

- [ ] Ajouter des pages supplémentaires dans `src/ui/pages/`
- [ ] Créer des tests dans `tests/`
- [ ] Ajouter plus de langues
- [ ] Implémenter la sauvegarde de préférences
- [ ] Créer une CI/CD avec GitHub Actions
