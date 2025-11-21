# Architecture - Writing Assistant Pro

## 📋 Vue d'ensemble

**writing-assistant-pro** est une application desktop native construite avec :

- **Flet** : Framework UI basé sur Flutter (Python wrapper)
- **Python 3.13+** : Langage principal
- **UV** : Gestionnaire de dépendances
- **PyInstaller** : Packaging pour distribution

L'architecture suit une séparation claire entre le **Core** (logique métier, config) et l'**UI** (interface Flet).

---

## 📁 Structure du projet

```
writing-assistant-pro/
│
├── main.py                      # Point d'entrée principal
├── logs/                        # Logs et fichiers générés (ignoré par git)
│
├── src/                         # Code source
│   ├── core/                    # Logique métier
│   │   ├── config.py            # Configuration & Arguments
│   │   ├── logger.py            # Logging centralisé (Loguru)
│   │   ├── systray_manager.py   # Gestion icône systray (Pystray)
│   │   ├── autostart_manager.py # Gestion démarrage automatique
│   │   └── translation.py       # Module de traduction (gettext)
│   └── ui/                      # Interface utilisateur
│       └── app_flet.py          # Classe principale de l'application Flet
│
├── scripts/                     # Scripts utilitaires
│   ├── run_dev.py               # Lanceur mode dev
│   ├── build_dev.py             # Builder mode dev (--onedir)
│   ├── build_final.py           # Builder production (--onefile)
│   └── translation_management/  # Outils de traduction
│
├── assets/                      # Ressources (icônes, images)
├── styles/                      # Thèmes (non utilisé par Flet directement, mais pour ref)
└── translations/                # Fichiers de traduction (.po/.mo)
```

---

## 🚀 Composants clés

### `main.py` - Point d'entrée

Orchestre le démarrage de l'application :

1. Parse les arguments (`--debug`)
2. Configure le logger via `src.core.logger`
3. Instancie `WritingAssistantFletApp`
4. Lance la boucle Flet

### `src/core/config.py` - Configuration

Gère la configuration globale et l'état :

- Détection du mode (Dev vs Frozen)
- Chemins des ressources (`get_app_root()`)
- Chargement de `config.json`

### `src/core/logger.py` - Logging

Système de logging robuste avec Loguru :

- **Dev (Console)** : Logs colorés dans la console
- **Dev (Windowed)** : Logs dans `logs/debug.log` (ou `dist/dev/debug.log`)
- **Prod (Windowed)** : Logging désactivé (Silent) pour performance

### `src/ui/app_flet.py` - Interface Flet

Contient la classe `WritingAssistantFletApp` qui gère :

- Initialisation de la fenêtre Flet
- Gestion du cycle de vie (on_window_event)
- Intégration du Systray
- Affichage de l'interface

---

## 🛠️ Système de Build

Le projet utilise deux modes de build distincts pour répondre aux besoins de développement et de production.

### 1. Build Développement (`scripts/build_dev.py`)

Conçu pour le débogage et l'itération rapide.

- **Mode PyInstaller** : `--onedir` (Dossier éclaté)
- **Sortie** : `dist/dev/`
- **Console** : Visible par défaut (configurable)
- **Logs** : Activés
- **Structure** :
  ```
  dist/dev/
  ├── Writing Assistant Pro.exe
  ├── _internal/          # Dépendances Python
  ├── assets/             # Ressources copiées
  └── debug.log           # Si console masquée
  ```

### 2. Build Final (`scripts/build_final.py`)

Conçu pour la distribution aux utilisateurs finaux.

- **Mode PyInstaller** : `--onefile` (Fichier unique)
- **Sortie** : `dist/production/`
- **Console** : Masquée (`--windowed`)
- **Logs** : Désactivés
- **Structure** :
  ```
  dist/production/
  └── Writing Assistant Pro.exe  # Autonome
  ```

---

## 🌐 Système de Traduction

Utilise **GNU gettext** via Babel.

1. **Marquage** : Utiliser `_("Texte")` dans le code.
2. **Extraction/Update** : `uv run python scripts/translation_management/update_translations.py`
3. **Compilation** : Automatique via le script ci-dessus.

Les fichiers `.mo` compilés sont chargés au démarrage par `src.core.translation`.

---

## 🔧 Conventions

- **Chemins** : Toujours utiliser `get_app_root()` pour résoudre les chemins de ressources (compatible Dev et Frozen).
- **Logging** : Utiliser `self.log` dans les classes ou `logger` global. Ne jamais utiliser `print()`.
- **Imports** : Imports absolus préférés (`from src.core import ...`).
