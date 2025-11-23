# Guide de Développement

## 📋 Vue d'ensemble

Ce guide détaille l'environnement de développement, les outils et les workflows pour contribuer au projet Writing Assistant Pro.

## 🛠️ Environnement

### Prérequis

- **Python** : 3.10+
- **UV** : Gestionnaire de paquets et de projet (remplace pip/poetry)
- **VS Code** : Éditeur recommandé (avec extensions Python, Pylance, Ruff)

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-repo/writing-assistant-pro.git
cd writing-assistant-pro

# 2. Synchroniser l'environnement avec UV
uv sync
```

## 🚀 Lancer l'Application

### Mode Développement

C'est le mode standard pour coder. Les logs sont affichés dans la console et sauvegardés dans `logs/run_dev.log`.

```bash
# Lancer le script principal
uv run python scripts/dev_build/run_dev.py
```

### Mode Build (Test)

Pour tester l'application telle qu'elle sera distribuée (mais sans la compiler en un seul fichier).

```bash
# Construire et lancer
uv run python scripts/dev_build/build_dev.py
```

## 🧪 Qualité du Code

Le projet utilise des outils stricts pour maintenir la qualité.

### Linting et Formatage (Ruff)

```bash
# Vérifier et corriger automatiquement
uv run python scripts/quality/run_ruff.py
```

### Vérification de Types (Pyright)

```bash
# Vérifier les types
uv run python scripts/quality/run_pyright.py
```

### Pre-commit Hooks

Ces vérifications sont lancées automatiquement avant chaque commit. Voir [Pre-commit Hooks](./10_PRECOMMIT.md) pour plus de détails.

## 📂 Structure du Projet

```
writing-assistant-pro/
├── src/                  # Code source
│   ├── core/             # Logique métier (Config, Logs, I18n...)
│   ├── ui/               # Interface utilisateur (Flet)
│   └── utils/            # Utilitaires divers
├── assets/               # Ressources (Icônes, Images)
├── scripts/              # Scripts de build et maintenance
├── tests/                # Tests unitaires (pytest)
├── translations/         # Fichiers de traduction (.po/.mo)
└── docs/                 # Documentation
```

## 🔄 Workflow de Développement

1. **Créer une branche** pour votre fonctionnalité (`git checkout -b feature/ma-feature`).
2. **Coder** en respectant les conventions (voir ci-dessous).
3. **Tester** manuellement et via les tests unitaires.
4. **Vérifier** la qualité (`ruff`, `pyright`).
5. **Commiter** (les hooks pre-commit valideront votre code).

## 📝 Conventions de Code

- **Imports** : Tous les fichiers doivent commencer par `from __future__ import annotations`.
- **Style** : Respecter PEP 8 (géré par Ruff).
- **Types** : Tout le code doit être typé (Type Hints).
- **Docstrings** : Documenter les modules, classes et fonctions.
- **Logs** : Utiliser `logger` (Loguru), jamais `print()`.
- **Chemins** : Toujours utiliser `pathlib` et `get_app_root()`.
- **Imports** : Imports absolus préférés (`from src.core.config import ...`).

## 🔧 Débogage

### VS Code

Une configuration de lancement est incluse dans `.vscode/launch.json`.

- **F5** : Lancer en mode debug.
- Points d'arrêt supportés.

### Logs

- **Console** : Niveau DEBUG en mode dev.
- **Fichier** : `logs/run_dev.log` (rotation non implémentée pour l'instant).

## 📦 Ajouter une Dépendance

Avec UV :

```bash
# Ajouter une librairie
uv add nom-librairie

# Ajouter une librairie de dev
uv add --dev nom-librairie
```

## 🔗 Références

- [UV Documentation](https://docs.astral.sh/uv/)
- [Flet Documentation](https://flet.dev/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
