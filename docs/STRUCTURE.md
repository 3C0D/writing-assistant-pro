# 📁 Structure du projet - Writing Assistant Pro

## Vue d'ensemble

```
writing-assistant-pro/
│
├── main.py                          ← Point d'entrée (wrapper)
├── logs/                            ← Logs et fichiers générés (ignoré git)
├── pyproject.toml                   ← Configuration du projet
├── babel.cfg                        ← Configuration Babel (extraction)
│
├── src/                             ← Code source principal
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               ← Configuration app + point d'entrée réel
│   │   ├── logger.py               ← Logging centralisé
│   │   ├── systray_manager.py      ← Gestion icône systray
│   │   ├── autostart_manager.py    ← Gestion démarrage auto
│   │   └── translation.py          ← Système de traduction (gettext)
│   └── ui/
│       ├── __init__.py
│       └── app_flet.py             ← Classe principale Flet App
│
├── scripts/
│   ├── run_dev.py                  ← Launcher mode développement
│   ├── build_dev.py                ← Builder mode développement
│   ├── build_final.py              ← Builder mode production
│   └── translation_management/
│       └── update_translations.py  ← Script unifié Babel
│
├── assets/                         ← Ressources (icônes, images)
│
├── styles/                         ← Thèmes (Référence)
│
├── translations/                   ← Fichiers de traduction
│   ├── template.pot                ← Template (source de vérité)
│   └── xx/LC_MESSAGES/             ← Dossiers par langue
│
├── docs/                           ← Documentation
│   ├── DEVELOPMENT.md              ← Guide développement
│   ├── STRUCTURE.md                ← Ce fichier
│   └── ...
│
├── .vscode/
│   ├── settings.json               ← Configuration VS Code
│   └── tasks.json                  ← Tâches VS Code
│
└── README.md                        ← Quick start
```

## Explication des rôles

### Racine

- **`main.py`** : Point d'entrée. Parse les arguments et lance l'application via `src.ui.app_flet`.
- **`logs/`** : Dossier pour les logs de développement et fichiers temporaires.

### `src/core/`

**Logique métier et infrastructure**

- **`config.py`** : Configuration globale (DEBUG, Chemins).
- **`logger.py`** : Logging centralisé (Loguru).
- **`systray_manager.py`** : Gestion de l'icône dans la barre des tâches (Pystray).
- **`translation.py`** : Système de traduction gettext.

### `src/ui/`

**Interface utilisateur (Flet)**

- **`app_flet.py`** : Contient la classe `WritingAssistantFletApp`.
  - Initialise Flet.
  - Gère la fenêtre principale.
  - Intègre le systray.

### `scripts/`

**Outils et scripts utilitaires**

- **`run_dev.py`** : Lance l'application en mode dev (logs console).
- **`build_dev.py`** : Crée un build de développement (`dist/dev/`) avec console et logs.
- **`build_final.py`** : Crée un build de production (`dist/production/`) optimisé et silencieux.

### `translations/`

**Fichiers de traduction**

- **`template.pot`** : Template général.
- **`.po`** : Fichiers éditables.
- **`.mo`** : Fichiers compilés (binaires).

### `docs/`

**Documentation**

- **`DEVELOPMENT.md`** : Guide complet des scripts et workflows.
- **`ARCHITECTURE.md`** : Architecture technique.
- **`STRUCTURE.md`** : Organisation des fichiers.
