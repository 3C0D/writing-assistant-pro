# ✍️ Writing Assistant Pro

Une application desktop moderne pour l'édition de texte construite avec **Flet** (Flutter pour Python) et **Python 3.13+**.

## 🚀 Démarrage rapide

### Prérequis

- Python 3.13+
- [UV](https://docs.astral.sh/uv/) (gestionnaire de dépendances rapide)

### Installation

```bash
# Cloner le projet
git clone <repo>
cd writing-assistant-pro

# Installer les dépendances
uv sync
```

### Lancer l'application

**Mode développement (recommandé) :**

```bash
uv run python scripts/run_dev.py
```

_Lance l'application avec console visible et logs détaillés._

**Mode production (simulation) :**

```bash
uv run python main.py
```

## 🛠️ Build & Packaging

Le projet dispose de deux modes de build distincts :

### 1. Build Développement (`dist/dev/`)

```bash
uv run python scripts/build_dev.py
```

- **Format** : Dossier (`--onedir`) avec dossier `_internal` visible.
- **Console** : Visible par défaut (pour le débogage).
- **Logs** :
  - Console visible : Logs dans la console.
  - Console masquée : Logs dans `dist/dev/debug.log`.
- **Usage** : Pour tester le packaging et déboguer l'exécutable.

### 2. Build Final (`dist/production/`)

```bash
uv run python scripts/build_final.py
```

- **Format** : Fichier unique (`--onefile`).
- **Console** : Masquée (Windowed mode).
- **Logs** : Désactivés (Silencieux) pour la performance et la propreté.
- **Usage** : Version finale à distribuer aux utilisateurs.

## 📁 Organisation des Fichiers

```
writing-assistant-pro/
├── main.py                      # Point d'entrée
├── logs/                        # Logs et fichiers générés (ignoré par git)
├── src/                         # Code source
│   ├── core/                    # Logique métier
│   │   ├── config.py            # Configuration & Arguments
│   │   ├── logger.py            # Logging centralisé (Loguru)
│   │   ├── systray_manager.py   # Gestion icône systray
│   │   └── ...
│   └── ui/                      # Interface utilisateur (Flet)
│       ├── app_flet.py          # Classe principale App
│       └── ...
├── scripts/                     # Scripts utilitaires
│   ├── run_dev.py               # Lanceur dev
│   ├── build_dev.py             # Builder dev
│   ├── build_final.py           # Builder production
│   └── translation_management/  # Outils traduction
├── assets/                      # Ressources (icônes, images)
├── styles/                      # Thèmes
└── translations/                # Fichiers .po/.mo
```

## 🔧 Développement

### Architecture Flet

L'application utilise Flet pour l'UI. Le point d'entrée est `src/ui/app_flet.py`.
Les composants UI sont modulaires et réactifs.

### Logging

- En développement : Les logs sont écrits dans le dossier `logs/` à la racine du projet.
- En production (frozen) : Pas de logs fichiers par défaut.

### Traductions

Le système utilise `gettext` et `babel`.
Pour mettre à jour les traductions après modification du code :

```bash
uv run python scripts/translation_management/update_translations.py
```

## 📚 Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) : Détails techniques et architecture.
- [docs/](./docs/) : Documentation approfondie (Structure, Babel, etc.).
