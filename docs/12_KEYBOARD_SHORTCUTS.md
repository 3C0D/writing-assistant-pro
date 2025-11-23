# Raccourcis Clavier Globaux

## 📋 Vue d'ensemble

L'application utilise la librairie `keyboard` pour gérer des raccourcis clavier globaux, permettant de contrôler l'application même lorsqu'elle n'a pas le focus (ex: afficher/masquer la fenêtre).

## 🎯 Objectifs

- Contrôle global (System-wide)
- Afficher/Masquer la fenêtre rapidement
- Gestion robuste (conflits, nettoyage)
- Enregistrement différé au démarrage

## 🏗️ Architecture

### Fichier Principal

- [`src/core/hotkey_manager.py`](../src/core/hotkey_manager.py)

### Dépendances

- **keyboard** : Librairie pour les hooks clavier système.

## 🔧 Fonctionnalités

### 1. Raccourci Principal

Le raccourci par défaut est défini dans la configuration (généralement `ctrl+.`).
Il permet de basculer la visibilité de la fenêtre principale.

### 2. Enregistrement Différé (`register_delayed`)

Pour éviter les conflits au démarrage de l'application (notamment lors d'un redémarrage automatique), l'enregistrement du raccourci est effectué après un court délai (configurable, ex: 2 secondes).

```python
def register_delayed(self, toggle_callback):
    # Thread séparé -> Attente -> Enregistrement
```

### 3. Nettoyage Automatique

Avant d'enregistrer un nouveau raccourci, le gestionnaire nettoie systématiquement les anciens hooks (`keyboard.unhook_all()`) pour éviter les doublons et les fuites de mémoire.

## 🚀 Utilisation

### Initialisation

```python
from src.core.hotkey_manager import HotkeyManager

# Dans l'initialisation de l'app
self.hotkey_manager = HotkeyManager(self.config)
self.hotkey_manager.register_delayed(self.toggle_window_visibility)
```

### Configuration

Les paramètres sont dans `config.json` :

```json
{
  "hotkey_combination": "ctrl+.",
  "hotkey_setup_delay": 2.0
}
```

## ⚠️ Dépannage

### Le raccourci ne fonctionne pas

1. **Permissions** : Sur certains systèmes (Linux/macOS), l'accès aux périphériques d'entrée nécessite des droits `root` ou des permissions d'accessibilité.
2. **Conflits** : Une autre application utilise peut-être déjà ce raccourci.
3. **Logs** : Vérifiez `logs/run_dev.log` pour voir si l'enregistrement a réussi ("Global hotkey registered").

### Le raccourci déclenche plusieurs fois

Cela arrive si `unhook_all()` n'est pas appelé correctement. Le `HotkeyManager` gère cela automatiquement, mais assurez-vous de ne pas instancier plusieurs gestionnaires.

## 🔗 Références

### Code Source

- [`src/core/hotkey_manager.py`](../src/core/hotkey_manager.py)

### Documentation Externe

- [Keyboard Library](https://github.com/boppreh/keyboard)
