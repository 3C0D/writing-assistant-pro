# Writing Assistant Pro - Architecture

## Vue d'ensemble

**Writing Assistant Pro** est une application desktop native construite avec **Flet** (framework Python basé sur Flutter). L'application fonctionne en mode systray avec une fenêtre cachable via hotkey global.

### Technologies principales

- **Framework UI** : Flet (Python + Flutter)
- **Gestionnaire de paquets** : UV
- **Build** : PyInstaller
- **Internationalisation** : gettext/Babel
- **Logging** : Loguru
- **Hotkeys globaux** : keyboard
- **Icône systray** : pystray

---

## Structure du Projet

```
writing-assistant-pro/
├── main.py                      # Point d'entrée principal
├── src/                         # Code source de l'application
│   ├── core/                    # Logique métier et services
│   │   ├── config/              # Configuration
│   │   │   ├── manager.py       # ConfigManager
│   │   │   ├── config.json      # Fichier de configuration
│   │   │   └── icons/           # Icônes de l'application
│   │   ├── managers/            # Gestionnaires
│   │   │   ├── autostart.py     # Gestion démarrage auto
│   │   │   ├── hotkey.py        # Hotkeys globaux
│   │   │   ├── systray.py       # Icône systray
│   │   │   └── window.py        # Gestion fenêtre
│   │   ├── services/            # Services
│   │   │   ├── logger.py        # Système de logging
│   │   │   └── translation.py   # Internationalisation
│   │   └── utils/               # Utilitaires
│   │       ├── paths.py         # Gestion chemins/modes
│   │       └── json_helpers.py  # Fonctions JSON
│   └── ui/                      # Interface utilisateur Flet
│       ├── app.py               # Application principale
│       ├── components/          # Composants réutilisables (futur)
│       └── views/               # Vues principales (futur)
├── scripts/                     # Scripts de développement
│   ├── dev_build/               # Build et développement
│   │   ├── build_utils.py       # Utilitaires de build
│   │   ├── build_dev.py         # Build développement
│   │   ├── build_final.py       # Build production
│   │   ├── run_dev.py           # Lancement dev
│   │   └── verify_autostart.py # Vérification autostart
│   ├── quality/                 # Qualité du code
│   │   ├── run_ruff.py          # Linting/formatage
│   │   └── run_pyright.py       # Vérification types
│   ├── tests/                   # Scripts de test
│   │   └── test_crash.py        # Test crash logging
│   └── translation_management/  # Gestion traductions
├── translations/                # Fichiers de traduction (.po, .mo)
├── dist/                        # Builds générés
│   ├── dev/                     # Build développement
│   └── production/              # Build production
├── logs/                        # Fichiers de log
└── docs/                        # Documentation
```

---

## Architecture Logique

### Séparation des Responsabilités

#### 1. `src/core/` - Logique Métier

**Configuration (`config/`)**
- `manager.py` : Gestion de la configuration avec persistance JSON
- `config.json` : Fichier de configuration par défaut
- `icons/` : Icônes de l'application

**Managers (`managers/`)**
- `autostart.py` : Gestion du démarrage automatique (Windows/Linux)
- `hotkey.py` : Enregistrement et gestion des hotkeys globaux
- `systray.py` : Icône systray et menu contextuel
- `window.py` : Gestion de la visibilité et du cycle de vie de la fenêtre

**Services (`services/`)**
- `logger.py` : Système de logging centralisé avec Loguru
- `translation.py` : Système d'internationalisation avec gettext

**Utilitaires (`utils/`)**
- `paths.py` : Détection du mode (dev/build-dev/build-final) et chemins
- `json_helpers.py` : Fonctions utilitaires pour JSON

#### 2. `src/ui/` - Interface Utilisateur

- `app.py` : Classe principale `WritingAssistantFletApp`
  - Initialise tous les managers
  - Crée l'interface utilisateur
  - Gère les événements UI
  - Navigation, sidebar, settings

#### 3. `scripts/` - Outils de Développement

**Build et Développement (`dev_build/`)**
- Scripts pour build PyInstaller et lancement en mode dev
- Gestion des processus, copie de fichiers, icônes

**Qualité (`quality/`)**
- Scripts de linting (Ruff) et vérification de types (Pyright)

**Tests (`tests/`)**
- Scripts de test et validation

---

## Flux d'Exécution

### Démarrage de l'Application

1. **`main.py`**
   - Parse les arguments (`--debug`, `--log-file`)
   - Configure le logger racine
   - Configure le gestionnaire d'exceptions (crash logging)
   - Initialise et lance `WritingAssistantFletApp`

2. **`WritingAssistantFletApp.__init__()`**
   - Charge la configuration (`ConfigManager`)
   - Initialise le système de traduction
   - Crée les managers (Hotkey, Window)

3. **`WritingAssistantFletApp.main(page)`**
   - Configure la page Flet
   - Crée l'interface utilisateur
   - Enregistre le hotkey global
   - Lance le systray en thread séparé
   - Cache la fenêtre (mode systray)

### Gestion de la Fenêtre

- **Hotkey** : `keyboard` détecte le hotkey → `WindowManager.toggle_window()`
- **Systray** : `pystray` gère l'icône et le menu
- **Fermeture** : Interceptée pour cacher au lieu de quitter

---

## Modes d'Exécution

L'application supporte 3 modes détectés automatiquement:

| Mode | Description | Exécutable | Config |
|------|-------------|-----------|--------|
| **dev** | Développement avec Python | `python main.py` | `dist/dev/config.json` |
| **build-dev** | Build développement PyInstaller | `dist/dev/Writing Assistant Pro.exe` | `dist/dev/config.json` |
| **build-final** | Build production PyInstaller | `dist/production/Writing Assistant Pro.exe` | À côté de l'exe |

**Détection** : `src/core/utils/paths.py` → `get_mode()`

---

## Logging

**Fichier** : `src/core/services/logger.py`

### Fichiers de Log

| Mode | Log Normal | Crash Log |
|------|-----------|-----------|
| **dev** | `logs/run_dev.log` | `logs/crash_run_dev.log` |
| **build-dev** | `logs/build_dev.log` | `logs/crash_build_dev.log` |
| **build-final** | À côté de l'exe | `crash.log` à côté de l'exe |

**Rotation** : Automatique, 3 fichiers maximum par type
**Niveau** : INFO par défaut, DEBUG si `--debug`

---

## Build System

**Fichiers** : `scripts/dev_build/build_dev.py`, `scripts/dev_build/build_final.py`

### Build Développement

```bash
uv run python scripts/dev_build/build_dev.py --console
```

- PyInstaller `--onedir`
- Mode console ou windowed
- Output : `dist/dev/`
- Fichiers copiés : config, icons, translations, styles

### Build Production

```bash
uv run python scripts/dev_build/build_final.py
```

- PyInstaller `--onefile`
- Mode windowed uniquement
- Output : `dist/production/`

---

## Scripts Principaux

| Script | Commande | Description |
|--------|----------|-------------|
| **Run Dev** | `uv run python scripts/dev_build/run_dev.py` | Lance en mode développement |
| **Build Dev** | `uv run python scripts/dev_build/build_dev.py` | Build développement |
| **Build Final** | `uv run python scripts/dev_build/build_final.py` | Build production |
| **Ruff** | `uv run python scripts/quality/run_ruff.py` | Linting et formatage |
| **Pyright** | `uv run python scripts/quality/run_pyright.py` | Vérification de types |

---

## Internationalisation

**Système** : gettext/Babel
**Fichier** : `src/core/services/translation.py`
**Dossier** : `translations/`

**Langues supportées** : EN, FR, IT
**Format** : `.po` (sources), `.mo` (compilés)

---

## Configuration

**Fichier par défaut** : `src/core/config/config.json`
**Class** : `src/core/config/manager.py` → `ConfigManager`

### Paramètres Principaux

- `language` : Langue de l'interface
- `dark_mode` : Thème sombre/clair
- `hotkey_combination` : Hotkey global (ex: "ctrl space")
- `start_on_boot` : Démarrage automatique
- `debug` : Mode debug

---

## Points d'Extension Futurs

### UI Modulaire

Les dossiers `src/ui/components/` et `src/ui/views/` sont préparés pour une future division de `app.py` en:
- Composants réutilisables (navigation, sidebar, settings)
- Vues principales (main content, dialogs)

### Tests Automatisés

Le dossier `scripts/tests/` est prêt pour l'ajout de tests unitaires et d'intégration avec pytest.
