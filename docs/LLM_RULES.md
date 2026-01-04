# 🤖 LLM Rules - Writing Assistant Pro

Document de référence concis pour les LLM travaillant sur ce projet.

---

## 🛠️ Outils Obligatoires

### 1. EventBus (Communication découplée)

```python
from src.core import EventType, emit_event, get_event_bus

# Émettre un événement
emit_event(EventType.LANGUAGE_CHANGED, {"language": "fr"})

# S'abonner dans une classe
bus = get_event_bus()
bus.on(EventType.WINDOW_SHOWN, self._handle_window_show)
```

### 2. Error Handler (Gestion d'erreurs)

```python
from src.core import handle_error, AppError

try:
    risky_operation()
except Exception as e:
    handle_error(e, context="operation_name", error_type=AppError)
```

### 3. Translation (i18n)

```python
from src.core import _

# Tout texte UI doit utiliser _()
ft.Text(_("Settings"))
message = _("Hotkey: {display}").format(display=display)
```

### 4. Configuration (via AppState)

```python
# ✅ Correct
self.state.config.DARK_MODE

# ❌ Incorrect - jamais d'import direct
from src.core.config import config
```

### 5. Resource Managers (Fichiers/Images)

```python
from src.core import safe_image_open, safe_file_read

with safe_image_open(path) as image:
    # Utiliser l'image
    pass
```

---

## 🚫 Anti-Patterns à Éviter

| ❌ Ne pas faire               | ✅ Faire                          |
| ----------------------------- | --------------------------------- |
| Imports locaux dans fonctions | Imports en haut du fichier        |
| Magic strings `"event_name"`  | Enums `EventType.EVENT_NAME`      |
| Dupliquer du code             | Extraire dans composants partagés |
| `print()` pour debug          | `logger.debug()` avec Loguru      |
| Accès direct config           | Via `self.state.config`           |

---

## 📁 Structure du Projet

```
src/
├── core/                    # Logique métier
│   ├── config/             # ConfigManager
│   ├── managers/           # hotkey, window, systray, autostart
│   ├── services/           # translation, logger, input_source, updater
│   ├── event_bus.py        # Pub/sub pattern
│   ├── error_handler.py    # Gestion d'erreurs
│   ├── state.py            # AppState, UIState
│   └── enums.py            # EventType, AttachmentType, etc.
└── ui/
    ├── app.py              # Application principale
    ├── design_system.py    # Couleurs, typo, spacing
    ├── components/         # Composants réutilisables
    ├── dialogs/            # Modales
    └── views/              # Vues (settings, about, main)
```

---

## ⚙️ Commandes de Vérification

```bash
# Linting et formatage (TOUJOURS lancer avant commit)
uv run python scripts/quality/run_ruff.py

# Vérification types (TOUJOURS lancer avant commit)
uv run python scripts/quality/run_pyright.py

# Tests
uv run pytest

# Lancer l'app en debug
uv run python main.py --debug
```

---

## 📋 Checklist Avant Modification

1. [ ] Lire les fichiers concernés d'abord
2. [ ] Vérifier les patterns existants
3. [ ] Utiliser les outils ci-dessus (EventBus, error_handler, etc.)
4. [ ] Maximum 100 caractères par ligne
5. [ ] Tout texte UI dans `_()`
6. [ ] Exécuter ruff + pyright
7. [ ] Tester manuellement si UI modifiée

---

## 🔗 EventTypes Disponibles

| Event                   | Émetteur              | Description            |
| ----------------------- | --------------------- | ---------------------- |
| `WINDOW_SHOWN`          | window.py, systray.py | Fenêtre affichée       |
| `WINDOW_HIDDEN`         | window.py             | Fenêtre cachée         |
| `WINDOW_PRE_SHOW`       | window.py             | Juste avant affichage  |
| `LANGUAGE_CHANGED`      | translation.py        | Langue modifiée        |
| `HOTKEY_CHANGED`        | hotkey.py             | Hotkey modifié         |
| `UPDATE_AVAILABLE`      | updater.py            | Mise à jour disponible |
| `INPUT_SOURCE_DETECTED` | input_source.py       | Source détectée        |

---

_Dernière mise à jour: 2026-01-05_
