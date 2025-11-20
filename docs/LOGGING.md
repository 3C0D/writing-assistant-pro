# 📝 Système de Logging

Le projet utilise **[Loguru](https://github.com/Delgan/loguru)** pour la gestion des logs. Cette bibliothèque remplace le module `logging` standard de Python pour offrir une API plus simple, des logs colorés et une meilleure gestion des exceptions.

## 🚀 Pourquoi Loguru ?

- **Simplicité** : Pas de configuration complexe de handlers/formatters.
- **Couleurs** : Sortie console colorée et lisible par défaut.
- **Exceptions** : Affichage détaillé des erreurs avec contexte.
- **Performance** : Rapide et thread-safe.

## ⚙️ Configuration

La configuration est centralisée dans `src/core/logger.py`.

### Modes de fonctionnement

Le logger s'adapte automatiquement selon le mode de lancement :

#### Mode Développement (`--debug`)

- **Niveau** : `DEBUG`
- **Format** : Détaillé avec timestamp, nom du module, fonction et numéro de ligne.
- **Sortie** : `stderr` (console)

```text
2023-10-27 10:30:45 | DEBUG    | src.core.config:load:115 - Configuration loaded
```

#### Mode Production (par défaut)

- **Niveau** : `INFO`
- **Format** : Épuré, sans timestamp (géré par le système hôte si besoin).
- **Sortie** : `stderr` (console)

```text
INFO     | src.core.config - Configuration loaded
```

## 💻 Utilisation

### Importation

Il suffit d'importer l'objet global `logger` depuis `loguru`.

```python
from loguru import logger
```

### Exemples

```python
# Info standard
logger.info("Application démarrée")

# Debug (visible seulement avec --debug)
logger.debug(f"Valeur variable: {ma_variable}")

# Warning
logger.warning("Fichier de configuration non trouvé, utilisation des défauts")

# Erreur
logger.error("Impossible de se connecter à la base de données")

# Exception (dans un bloc try/except)
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Erreur critique survenue")
```

### Contextualisation (Bind)

Pour ajouter du contexte spécifique à un module (recommandé) :

```python
# Dans src/core/hotkey_manager.py
self.log = logger.bind(name="WritingAssistant.HotkeyManager")

self.log.info("Hotkey registered")
# Sortie : ... | WritingAssistant.HotkeyManager - Hotkey registered
```

Ceci permet de filtrer facilement les logs par composant si nécessaire.
