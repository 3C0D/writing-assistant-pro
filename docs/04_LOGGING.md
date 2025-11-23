# Système de Logs

## 📋 Vue d'ensemble

Le projet utilise **Loguru** pour un système de logging moderne, coloré et flexible. Les logs sont automatiquement dirigés vers des fichiers ou la console selon le mode d'exécution.

## 🎯 Objectifs

- Logs centralisés dans le dossier `logs/`
- Logs colorés en mode console
- Logs fichiers en mode windowed
- Niveaux de log configurables (DEBUG, INFO, etc.)
- Pas de logs en production pour optimiser les performances

## 🏗️ Architecture

### Fichier Principal

- [`src/core/services/logger.py`](../src/core/services/logger.py) - Configuration centralisée du logger

### Fonction Principale

```python
setup_root_logger(debug: bool, log_filename: str | None = None) -> None
```

Cette fonction doit être appelée **une seule fois** au démarrage de l'application.

## 📂 Emplacements des Logs

### Mode Développement (`run_dev.py`)

```
logs/run_dev.log
```

- Console visible avec logs colorés
- Fichier de log dans `logs/`
- Niveau: DEBUG

### Mode Build Dev (`build_dev.py`)

```
logs/build_dev.log
```

- Console visible ou masquée selon `--console`/`--windowed`
- Fichier de log dans `logs/` (chemin absolu passé en argument)
- Niveau: DEBUG

### Mode Build Final (Production)

```
Pas de logs fichiers
```

- Console masquée (`--windowed`)
- Logs désactivés pour performance
- Mode silencieux

## 🔧 Utilisation

### Dans le Code

```python
from loguru import logger

# Après setup_root_logger() dans main.py
logger.debug("Message de debug")
logger.info("Message d'information")
logger.warning("Message d'avertissement")
logger.error("Message d'erreur")
logger.critical("Message critique")
```

### Dans les Classes

```python
from loguru import logger

class MyClass:
    def __init__(self):
        self.log = logger.bind(name=self.__class__.__name__)
        self.log.info("MyClass initialized")

    def my_method(self):
        self.log.debug("Method called")
```

## ⚙️ Configuration

### Niveaux de Log

| Niveau     | Usage                                    | Exemple                      |
| ---------- | ---------------------------------------- | ---------------------------- |
| `DEBUG`    | Informations détaillées pour le débogage | Variables, états internes    |
| `INFO`     | Informations générales                   | Démarrage, arrêt, événements |
| `WARNING`  | Avertissements non critiques             | Configurations manquantes    |
| `ERROR`    | Erreurs récupérables                     | Échecs d'opérations          |
| `CRITICAL` | Erreurs critiques                        | Erreurs fatales              |

### Format des Logs

#### Console (avec couleurs)

```
2025-11-22 23:00:00 | DEBUG    | module:function - Message
```

#### Fichier (sans couleurs)

```
2025-11-22 23:00:00 | DEBUG    | module:function - Message
```

## 🚀 Exemples Concrets

### Lancer en Mode Dev avec Logs Console

```bash
uv run python scripts/run_dev.py
```

**Résultat** :

- Logs dans la console (colorés)
- Logs dans `logs/run_dev.log`

### Lancer Build Dev en Mode Console

```bash
uv run python scripts/build_dev.py --console
```

**Résultat** :

- Logs dans la console (colorés)
- Logs dans `logs/build_dev.log`

### Lancer Build Dev en Mode Windowed

```bash
uv run python scripts/build_dev.py --windowed
```

**Résultat** :

- Pas de console
- Logs dans `logs/build_dev.log`

## 📊 Détection Automatique

Le logger détecte automatiquement :

### 1. Mode d'Exécution

```python
if getattr(sys, "frozen", False):
    # Mode frozen (exécutable PyInstaller)
    log_dir = Path(sys.executable).parent
else:
    # Mode développement
    log_dir = Path("logs")
```

### 2. Disponibilité de la Console

```python
has_console = sys.stderr is not None
```

### 3. Nom du Fichier de Log

```python
# Frozen
default_log_name = "build_dev.log" if "dev" in log_dir.name.lower() else "app.log"

# Dev
default_log_name = "run_dev.log"
```

## ⚠️ Limitations Actuelles

### Rotation des Logs Non Implémentée

**Problème** : Les fichiers de logs peuvent grandir indéfiniment.

**Solution Future** : Implémenter la rotation avec Loguru

```python
logger.add(
    str(debug_log_path),
    rotation="10 MB",  # Rotation à 10 MB
    retention=3,       # Garder 3 fichiers
    compression="zip"  # Compresser les anciens
)
```

### Pas de Logs en Production

**Raison** : Optimisation des performances et propreté.

**Alternative** : Si nécessaire, activer des logs minimaux :

```python
# Dans build_final.py, passer --debug pour activer les logs
```

## 🔍 Dépannage

### Les Logs n'Apparaissent Pas

**Vérifier** :

1. `setup_root_logger()` est appelé au démarrage
2. Le dossier `logs/` existe (créé automatiquement en dev)
3. Le mode debug est activé (`--debug`)

**Solution** :

```bash
# Vérifier le contenu du dossier logs
ls logs/

# Lancer avec debug explicite
uv run python main.py --debug
```

### Les Logs ne Sont Pas Colorés

**Cause** : Mode windowed ou redirection de sortie

**Solution** :

```bash
# Forcer le mode console
uv run python scripts/build_dev.py --console
```

### Fichier de Log Introuvable

**Vérifier le chemin** :

```python
# En dev
logs/run_dev.log

# En build dev
logs/build_dev.log
```

**Note** : Le chemin est affiché à la fin de l'exécution :

```
ℹ️  Log file: logs/run_dev.log
```

## 📝 Bonnes Pratiques

### 1. Utiliser le Logger, Pas `print()`

```python
# ❌ Mauvais
print("Application started")

# ✅ Bon
logger.info("Application started")
```

### 2. Niveaux de Log Appropriés

```python
# ❌ Mauvais
logger.debug("Application crashed!")

# ✅ Bon
logger.critical("Application crashed!")
```

> [!NOTE]
> Depuis l'implémentation de la capture automatique des crashes, le
> `logger.critical()` est maintenant utilisé activement par le système de
> gestion d'exceptions non gérées.

### 3. Messages Informatifs

```python
# ❌ Mauvais
logger.info("Done")

# ✅ Bon
logger.info("Translation files compiled successfully")
```

### 4. Contexte dans les Logs

```python
# ❌ Mauvais
logger.error("Failed")

# ✅ Bon
logger.error(f"Failed to load config file: {config_path}")
```

## 💥 Capture Automatique des Crashes

### Vue d'ensemble

Le système capture automatiquement **toutes** les exceptions non gérées et les logs dans des **fichiers crash dédiés** pour faciliter l'identification.

- ✅ Capture active dans **tous les modes** (dev et production)
- ✅ Fichiers crash **séparés** pour visibilité immédiate
- ✅ Les logs normaux continuent en parallèle
- ✅ Traceback complet inclus dans chaque crash

### Emplacements des Fichiers Crash

| Mode          | Fichier Crash         | Emplacement                |
| ------------- | --------------------- | -------------------------- |
| `run_dev`     | `crash_run_dev.log`   | `logs/crash_run_dev.log`   |
| `build_dev`   | `crash_build_dev.log` | `logs/crash_build_dev.log` |
| `build_final` | `crash.log`           | Dossier parent de l'exe    |

> [!TIP]
> En production, le fichier `crash.log` suit l'exe : si vous déplacez
> l'exécutable, le crash log sera créé dans le nouveau dossier.

### Configuration

La capture des crashes est configurée dans [`main.py`](../main.py#L26-L27) :

```python
# Setup logging
setup_root_logger(debug=debug_mode, log_filename=log_file)

# Setup exception handler to log crashes to dedicated files
setup_exception_handler()
```

**Appeler `setup_exception_handler()` une seule fois** après
`setup_root_logger()`.

### Format des Logs de Crash

Exemple de contenu dans `logs/crash_run_dev.log` :

```
================================================================================
CRASH DETECTED - 2025-11-23 03:28:30
================================================================================
Traceback (most recent call last):
  File "c:\\Users\\dd200\\Documents\\...\\test_crash.py", line 31, in <module>
    raise RuntimeError("This is an intentional crash for testing!")
RuntimeError: This is an intentional crash for testing!
================================================================================
```

### Avantages

1. **Visibilité immédiate** : Fichier crash séparé = pas besoin de fouiller
   dans les logs normaux
2. **Mode spécifique** : Nom du fichier indique le mode d'exécution
   (run_dev, build_dev, production)
3. **Historique** : Mode append, tous les crashes sont conservés
4. **Production-ready** : Fonctionne même en mode prod sans logs normaux

### Test de la Capture

Pour tester la capture des crashes :

```bash
# Utiliser le script de test fourni
uv run python scripts/test_crash.py

# Vérifier le fichier de crash créé
cat logs/crash_run_dev.log
```

## 🔗 Références

### Code Source

- [`src/core/logger.py`](../src/core/logger.py#L14-L93) - Configuration du logger
- [`scripts/run_dev.py`](../scripts/run_dev.py#L43) - Utilisation en dev
- [`scripts/build_dev.py`](../scripts/build_dev.py#L194-L195) - Utilisation en build

### Documentation Externe

- [Loguru Documentation](https://loguru.readthedocs.io/)
- [Python Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels)

## 🚧 Améliorations Futures

### Rotation des Logs

Implémenter la rotation automatique pour limiter la taille des fichiers.

### Logs Structurés

Ajouter des logs au format JSON pour faciliter l'analyse.

### Logs en Production

Ajouter des logs minimaux en production (erreurs uniquement).

### Centralisation des Logs

Envoyer les logs vers un service centralisé (Sentry, etc.).
