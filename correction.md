Je comprends le problème ! C'est une question classique de configuration des loggers en Python. Analysons ce qui se passe :

## Le Problème

Quand tu utilises `logging.basicConfig()` dans `main.py` **et** que tu crées un logger avec `setup_logger()`, tu crées deux handlers qui écrivent tous les deux les mêmes messages, d'où les doublons.

## La Solution

Voici comment réorganiser le code pour que tout fonctionne correctement sans doublons :## Explication du Problème et de la Solution

### Pourquoi il y avait des doublons ?

1. **Dans `main.py`** : Tu appelais `logging.basicConfig()` qui configure le **root logger** (le logger racine de Python)
2. **Dans `styles.py`** : Tu utilisais `log = logging.getLogger(__name__)` qui crée un logger **enfant** du root logger
3. **Résultat** : Les messages étaient loggés deux fois :
   - Une fois par le handler du logger enfant
   - Une fois par le handler du root logger (à cause de la propagation)

### La Solution : Hiérarchie de Loggers

J'ai créé une **hiérarchie de loggers** propre :

```
WritingAssistant (root de l'app)
├── WritingAssistant.main
├── WritingAssistant.styles
│   └── WritingAssistant.styles.CSSHotReloader
└── WritingAssistant.HiddenWindowApp
```

**Avantages** :
- ✅ Pas de doublons
- ✅ Chaque module a son propre logger identifiable
- ✅ Configuration centralisée via `setup_root_logger()`
- ✅ Les logs affichent le nom du module (ex: `WritingAssistant.styles`)

### Les Changements Clés

1. **`logger.py`** :
   - Ajout de `setup_root_logger()` pour configurer le logger racine UNE SEULE FOIS
   - Ajout de `logger.propagate = False` dans `setup_logger()` pour éviter la propagation (si tu utilises cette fonction pour des cas spéciaux)

2. **`main.py`** :
   - Remplacement de `logging.basicConfig()` par `setup_root_logger(debug=DEBUG)`
   - Création de loggers spécifiques : `logging.getLogger("WritingAssistant.main")` et `logging.getLogger("WritingAssistant.HiddenWindowApp")`
   - Suppression de l'argument `logging` passé à `create_interface()` (inutile)

3. **`styles.py`** :
   - Utilisation de `logging.getLogger("WritingAssistant.styles")` au niveau du module
   - Création d'un logger pour la classe : `logging.getLogger("WritingAssistant.styles.CSSHotReloader")`
   - Suppression du `print()` (maintenant que les logs fonctionnent correctement)

### Utilisation

Maintenant, dans **n'importe quel module**, tu peux simplement faire :

```python
import logging

log = logging.getLogger("WritingAssistant.ton_module")
log.info("Message de log")
```

Et ça fonctionnera automatiquement avec la configuration définie dans `main.py` ! 🎉


"""
Centralized logging configuration for the application.
"""

import logging
import sys


def setup_logger(debug: bool, name: str = "WritingAssistant") -> logging.Logger:
    """
    Configure and return a logger for the application.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
        name: Logger name

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    if debug:
        # DEBUG mode: detailed logs with timestamp and level
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        # Production mode: simple logs
        log_level = logging.INFO
        log_format = "%(levelname)s - %(message)s"
    
    # Create a handler to display logs in the console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    # Configure the logger
    logger.setLevel(log_level)
    logger.addHandler(handler)
    
    # CRITICAL: Prevent propagation to root logger to avoid duplicates
    logger.propagate = False
    
    if debug:
        logger.debug("DEBUG Mode enabled - Detailed logging")
    
    return logger


def setup_root_logger(debug: bool) -> None:
    """
    Configure the root logger for the entire application.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
    """
    root_logger = logging.getLogger()
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    if debug:
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        log_level = logging.INFO
        log_format = "%(name)s - %(levelname)s - %(message)s"
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    
    if debug:
        root_logger.debug("Root logger configured - Debug mode enabled")

