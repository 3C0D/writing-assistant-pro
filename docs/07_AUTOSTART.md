# Système de Démarrage Automatique (Autostart)

## 📋 Vue d'ensemble

Le gestionnaire de démarrage automatique (`AutostartManager`) permet à l'application de se lancer automatiquement à l'ouverture de session de l'utilisateur. Il supporte Windows (via le Registre) et Linux (via les fichiers `.desktop`).

## 🎯 Objectifs

- Lancement automatique au démarrage du système
- Support multi-plateforme (Windows & Linux)
- Gestion des modes Développement et Production
- Synchronisation avec les paramètres de l'application

## 🏗️ Architecture

### Fichier Principal

- [`src/core/autostart_manager.py`](../src/core/autostart_manager.py)

### Mécanismes Utilisés

| Plateforme  | Méthode          | Emplacement                                          |
| ----------- | ---------------- | ---------------------------------------------------- |
| **Windows** | Registre         | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` |
| **Linux**   | Fichier .desktop | `~/.config/autostart/writing-tools.desktop`          |

## 🔧 Fonctionnalités

### 1. Détection du Mode d'Exécution

Le gestionnaire détecte si l'application tourne depuis le code source (Dev) ou depuis un exécutable compilé (Frozen).

```python
@staticmethod
def is_compiled() -> bool:
    return hasattr(sys, "frozen") and hasattr(sys, "_MEIPASS")
```

Cela détermine quelle commande lancer au démarrage :

- **Compilé** : Chemin direct vers l'exécutable (`.exe`).
- **Dev** : Commande Python pour lancer le script (`python main.py`).

### 2. Gestion Windows

Sur Windows, deux clés de registre distinctes sont utilisées pour éviter les conflits :

- `WritingTools` : Pour la version production (compilée).
- `WritingToolsDevStartup` : Pour la version développement.

Lors de l'activation d'un mode, l'autre est automatiquement désactivé pour garantir qu'une seule version se lance.

### 3. Gestion Linux

Sur Linux, un fichier standard `.desktop` est créé dans le dossier d'autostart de l'utilisateur.

**Template du fichier .desktop :**

```ini
[Desktop Entry]
Type=Application
Name=Writing Tools
Exec={exec_path}
Icon=writing-tools
Terminal=false
X-GNOME-Autostart-enabled=true
```

### 4. Synchronisation

La méthode `sync_with_settings` assure que l'état du système (activé/désactivé) correspond à la configuration de l'application (`config.json`). Si une différence est détectée, la configuration est mise à jour pour refléter la réalité du système.

## 🚀 Utilisation

### Activer/Désactiver

```python
from src.core.autostart_manager import AutostartManager

# Activer
AutostartManager.set_autostart(True)

# Désactiver
AutostartManager.set_autostart(False)
```

### Vérifier l'État

```python
is_enabled = AutostartManager.check_autostart()
```

### Synchroniser avec la Config

```python
# Met à jour la config si l'état système a changé
AutostartManager.sync_with_settings(config_manager)

# Change l'état système ET met à jour la config
AutostartManager.set_autostart_with_sync(True, config_manager)
```

## ⚠️ Dépannage

### L'application ne se lance pas au démarrage

**Windows :**

1. Ouvrir `regedit`.
2. Aller à `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.
3. Vérifier la présence de la clé `WritingTools` (ou `WritingToolsDevStartup`).
4. Vérifier que le chemin vers l'exécutable est correct.

**Linux :**

1. Vérifier le dossier `~/.config/autostart/`.
2. Vérifier le contenu de `writing-tools.desktop`.
3. Vérifier les permissions d'exécution.

### Conflits Dev/Prod

Si vous développez et utilisez la version installée en même temps, le gestionnaire essaie de gérer les conflits en utilisant des clés différentes, mais il est recommandé de désactiver le démarrage auto sur la version de développement si la version production est installée.

## 🔗 Références

### Code Source

- [`src/core/autostart_manager.py`](../src/core/autostart_manager.py)

### Documentation Externe

- [Windows Registry Run Keys](https://learn.microsoft.com/en-us/windows/win32/setupapi/run-and-runonce-registry-keys)
- [Linux Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)
