# Gestion des Assets (Ressources)

## 📋 Vue d'ensemble

La gestion des assets concerne principalement les icônes et images utilisées par l'application. Le projet centralise ces ressources dans le dossier `assets/`.

## 🎯 Objectifs

- Centralisation des ressources
- Support des icônes d'application (Barre des tâches, Fenêtre, Exécutable)
- Compatibilité multi-plateforme (PNG supporté)
- Copie automatique lors du build

## 🏗️ Architecture

### Structure des Dossiers

```
assets/
└── icons/
    └── app_icon.png    # Icône principale (haute résolution)
```

### Utilisation dans le Code

Le chemin vers les assets doit toujours être résolu dynamiquement via `get_app_root()` (voir [Configuration](./08_CONFIGURATION.md)).

```python
from src.core.config import get_app_root

icon_path = get_app_root() / "assets" / "icons" / "app_icon.png"
```

## 🔧 Fonctionnalités

### 1. Icône de l'Application

L'icône principale est `app_icon.png`. Elle est utilisée pour :

- L'icône de la fenêtre Flet
- L'icône de la barre des tâches (Systray)
- L'icône de l'exécutable Windows (via PyInstaller)

### 2. Support PyInstaller

PyInstaller gère désormais nativement les fichiers PNG pour les icônes d'exécutables, ce qui évite d'avoir à convertir manuellement en `.ico`.

Dans les scripts de build :

```python
pyinstaller_command = [
    # ...
    f"--icon={icon_path}",
    # ...
]
```

### 3. Copie lors du Build

Les assets sont automatiquement copiés dans le dossier de distribution lors du build (voir `scripts/utils.py`).

- **Build Dev** : `assets/` → `dist/dev/assets/`
- **Build Final** : Les assets sont embarqués dans l'exécutable (mode `--onefile`) ou copiés à côté (mode `--onedir`).

## 🚀 Ajouter une Nouvelle Ressource

1. Placer le fichier dans `assets/` (créer un sous-dossier si nécessaire, ex: `assets/images/`).
2. Dans le code, utiliser `get_app_root()` pour y accéder.

```python
image_path = get_app_root() / "assets" / "images" / "mon_image.png"
ui.image(src=str(image_path))
```

## ⚠️ Bonnes Pratiques

1. **Formats** : Privilégier le PNG pour la transparence.
2. **Résolution** : Utiliser une résolution suffisante (ex: 256x256 ou 512x512) pour l'icône principale.
3. **Chemins** : Ne jamais utiliser de chemins absolus en dur ou de chemins relatifs simples. Toujours passer par `get_app_root()`.

## 🔗 Références

### Code Source

- [`scripts/utils.py`](../scripts/utils.py) - Logique de copie des assets
- [`src/core/systray_manager.py`](../src/core/systray_manager.py) - Utilisation de l'icône
