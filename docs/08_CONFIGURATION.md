# Système de Configuration

## 📋 Vue d'ensemble

Le système de configuration centralise la gestion des paramètres de l'application. Il utilise un fichier JSON pour la persistance et offre une interface simple pour lire et écrire des valeurs. Il gère également la détection du mode d'exécution (Dev vs Production) et la résolution des chemins de fichiers.

## 🎯 Objectifs

- Configuration persistante (JSON)
- Valeurs par défaut robustes
- Accès simple (attributs ou dictionnaire)
- Gestion transparente des chemins (Dev/Prod)
- Détection automatique de l'environnement

## 🏗️ Architecture

### Fichier Principal

- [`src/core/config/manager.py`](../src/core/config/manager.py)

### Fichier de Données

- `config.json` (racine ou `dist/dev/` ou `dist/production/`)

### Classe `ConfigManager`

C'est le cœur du système. Elle charge, sauvegarde et fournit l'accès aux paramètres.

## 🔧 Fonctionnalités

### 1. Détection du Mode (`get_mode`)

Le système détecte automatiquement comment l'application est exécutée :

- **`dev`** : Exécution depuis le code source (`python main.py`).
- **`build-dev`** : Exécution depuis le build de développement (dossier `dist/dev/`).
- **`build-final`** : Exécution depuis le build de production (fichier unique `dist/production/`).

### 2. Résolution des Chemins (`get_app_root`)

Cette fonction est **critique** pour le bon fonctionnement de l'application. Elle retourne le dossier racine correct selon le mode :

- **Dev** : Racine du projet (où se trouve `src/`, `assets/`, etc.).
- **Frozen** : Dossier contenant l'exécutable (où les assets ont été copiés).

**Utilisation recommandée :**
Toujours utiliser `get_app_root()` pour construire des chemins vers des ressources.

```python
icon_path = get_app_root() / "assets" / "icons" / "app_icon.png"
```

### 3. Gestion du Fichier `config.json`

L'emplacement du fichier de configuration change selon le mode :

- **Dev** : `dist/dev/config.json` (partagé avec le build dev pour faciliter les tests).
- **Frozen** : À côté de l'exécutable (`Writing Assistant Pro.exe`).

Si le fichier n'existe pas, il est créé avec les valeurs par défaut.

### 4. Accès aux Paramètres

Le `ConfigManager` permet deux styles d'accès :

**Style Dictionnaire :**

```python
debug = config.get("debug", False)
config.set("theme", "dark")
```

**Style Attribut (pour les clés existantes) :**

```python
# Lecture (insensible à la casse)
is_debug = config.DEBUG

# Écriture
config.THEME = "light"
```

## 🚀 Utilisation

### Initialisation

```python
from src.core.config import ConfigManager

config = ConfigManager()
```

### Lire une Valeur

```python
# Avec valeur par défaut
language = config.get("language", "en")

# Via attribut (lève une erreur si inexistant)
lang = config.LANGUAGE
```

### Modifier une Valeur

```python
# Sauvegarde automatique
config.set("start_on_boot", True)
```

### Arguments de Ligne de Commande

Le module fournit aussi `parse_arguments()` pour gérer les arguments passés au lancement (ex: `--debug`).

```python
from src.core.config import parse_arguments

args = parse_arguments()
if args.debug:
    print("Debug mode enabled")
```

## ⚙️ Configuration Par Défaut

La configuration par défaut est chargée depuis `src/core/config.json` (le fichier template dans le code source).

Exemple de structure :

```json
{
  "language": "en",
  "theme": "system",
  "start_on_boot": false,
  "window_width": 800,
  "window_height": 600
}
```

## ⚠️ Bonnes Pratiques

1. **Toujours utiliser `get_app_root()`** pour les chemins de fichiers. Ne jamais utiliser de chemins relatifs simples comme `"assets/icon.png"`.
2. **Définir des valeurs par défaut** dans le code (`config.get("key", default)`) pour gérer les fichiers de config anciens ou corrompus.
3. **Ne pas stocker de données sensibles** (mots de passe) dans `config.json` sans chiffrement.

## 🔗 Références

### Code Source

- [`src/core/config/manager.py`](../src/core/config/manager.py)

### Documentation Externe

- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python json](https://docs.python.org/3/library/json.html)
