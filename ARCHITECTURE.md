# Architecture - Writing Assistant Pro

## 📋 Vue d'ensemble

**writing-assistant-pro** est une application desktop construite avec :
- **NiceGUI** : Framework UI moderne basé sur Python et web technologies
- **Python 3.13+** : Langage principal
- **UV** : Gestionnaire de dépendances et environnements Python
- **Mode développement** : Hot reload, logging détaillé, thème switchable

L'architecture est conçue pour être **modulaire, scalable et facile à développer**.

---

## 📁 Structure du projet

```
writing-assistant-pro/
│
├── main.py                      # Point d'entrée principal
├── logger.py                    # Configuration du logging centralisée
├── styles.py                    # Gestion des thèmes (light/dark)
├── pyproject.toml               # Configuration du projet (dépendances)
├── uv.lock                      # Lock file des dépendances (UV)
│
├── styles/                      # Fichiers CSS des thèmes
│   ├── light.css                # Thème clair
│   └── dark.css                 # Thème sombre
│
├── ui/                          # Module UI (à étendre)
│   └── __init__.py              # Crée l'interface principale
│
├── scripts/                     # Scripts utilitaires
│   └── run_dev.py               # Lance l'app en mode développement
│
├── docs/                        # Documentation
│   └── architecture.py          # ⚠️ À supprimer (remplacé par ARCHITECTURE.md)
│
└── .vscode/                     # Configuration VS Code
    └── settings.json            # Config Code Runner pour UV
```

---

## 🚀 Composants clés

### `main.py` - Point d'entrée
Le fichier principal qui orchestrate tout :
- Récupère les flags de ligne de commande (`--debug`)
- Configure le logger
- Charge les thèmes
- Lance l'application NiceGUI en mode natif

**Arguments supportés :**
- `--debug` : Active le mode DEBUG (logs détaillés)

**Configuration :**
```python
DEBUG = '--debug' in sys.argv
DARK_MODE = False  # À changer pour activer le thème sombre
```

### `logger.py` - Logging centralisé
Gère tout le logging de l'application :
- En mode DEBUG : logs détaillés avec timestamp
- En mode production : logs simples

**Utilisation :**
```python
from logger import setup_logger
log = setup_logger(debug=DEBUG)
log.debug("Message de debug")
log.info("Information")
log.warning("Attention")
log.error("Erreur")
```

### `styles.py` - Gestion des thèmes
Charge les thèmes CSS depuis des fichiers externes :
- `styles/light.css` - Thème clair (défaut)
- `styles/dark.css` - Thème sombre

**Utilisation :**
```python
from styles import apply_theme
apply_theme(DARK_MODE)  # Applique le thème choisi
```

### `ui/__init__.py` - Interface utilisateur
Module principal pour l'interface. Actuellement très simple, mais à étendre avec :
- Pages (home, editor, settings, etc.)
- Composants réutilisables (toolbar, panels, etc.)

**Structure future envisagée :**
```
ui/
├── __init__.py           # Fonction principale create_interface()
├── pages/
│   ├── home.py          # Page d'accueil
│   └── editor.py        # Éditeur principal
├── components/
│   ├── toolbar.py       # Barre d'outils
│   ├── sidebar.py       # Barre latérale
│   └── statusbar.py     # Barre de statut
└── dialogs/
    ├── settings.py      # Dialogue des paramètres
    └── about.py         # À propos
```

---

## 🛠️ Workflow de développement

### Lancer l'app en mode développement

```bash
# Via le script dédié (avec hot reload)
uv run python scripts/run_dev.py

# Ou directement
uv run python main.py --debug

# Ou depuis VS Code : appuyer sur la flèche ▶️ (Code Runner)
```

**En mode DEBUG :**
- ✅ Hot reload activé (les changements apparaissent immédiatement)
- ✅ Logs détaillés avec timestamp
- ✅ Titre de fenêtre montre "(DEV MODE)"

### Lancer l'app en mode production

```bash
python main.py
```

**En mode production :**
- ✅ Pas de hot reload
- ✅ Logs simples (INFO et supérieur seulement)
- ✅ Titre de fenêtre normal

---

## 🎨 Gestion des thèmes

### Activer le mode sombre

1. Ouvre `main.py`
2. Change `DARK_MODE = False` en `DARK_MODE = True`
3. Relance l'application

```python
DARK_MODE = True  # Mode sombre
DARK_MODE = False # Mode clair (défaut)
```

### Ajouter un nouveau thème

1. Crée un fichier `styles/custom.css`
2. Modifie `styles.py` pour charger le nouveau thème
3. Ajoute une option pour le sélectionner

---

## 📊 Configuration de VS Code

Le fichier `.vscode/settings.json` configure Code Runner pour utiliser `uv run python` :

```json
{
  "code-runner.executorMap": {
    "python": "uv run python"
  },
  "code-runner.runInTerminal": true,
  "code-runner.saveFileBeforeRun": true
}
```

**Utilisation :** Appuyer sur la flèche ▶️ pour exécuter le script actuel via `uv run python`.

---

## 🔧 Dépendances

Définies dans `pyproject.toml` :

```toml
[project]
dependencies = [
    "nicegui",     # Framework UI
    "pywebview",   # Pour mode natif
]
```

Géré par **UV** (plus rapide et fiable que pip).

---

## 📝 Conventions de code

### Logging

N'utilise **jamais** de `if DEBUG: print()`. Utilise le logger :

```python
from logger import setup_logger
log = setup_logger(debug=DEBUG)

# ✅ BON
log.debug("Message de debug")
log.info("Information")

# ❌ MAUVAIS
if DEBUG:
    print("Message")
```

### Organisation du code UI

Tout le code UI doit être dans le dossier `ui/` :

```python
# ✅ BON - dans ui/__init__.py ou ui/pages/
from nicegui import ui

def create_interface(logger):
    ui.label("Hello")

# ❌ MAUVAIS - mélanger avec la logique principale
```

### Arguments de ligne de commande

Utilise le flag `--debug` pour le mode développement :

```python
DEBUG = '--debug' in sys.argv
```

---

## 🚦 Prochaines étapes

### Court terme
- [ ] Ajouter plus de composants UI (input, textarea, boutons avancés)
- [ ] Créer une page `ui/pages/home.py` pour la page d'accueil
- [ ] Ajouter une barre de menu/toolbar

### Moyen terme
- [ ] Ajouter un système de configuration (fichier config.yaml)
- [ ] Implémenter la persistance des données
- [ ] Créer des tests unitaires
- [ ] Ajouter une CI/CD (GitHub Actions)

### Long terme
- [ ] Architecture MVVM pour la logique métier
- [ ] Système de plugins
- [ ] Localisation (i18n)
- [ ] Packaging et distribution (exe, dmg, etc.)

---

## 🐛 Dépannage

### Les logs s'affichent plusieurs fois
C'est normal en mode DEBUG avec le reload activé. Chaque rechargement réexécute le code.

### Le thème ne change pas
- Vérifie que `DARK_MODE` est bien modifié dans `main.py`
- Redémarre l'application (le reload ne recharge pas les CSS)

### Code Runner ne fonctionne pas
- Vérifie que `.vscode/settings.json` existe
- Redémarre VS Code
- Installe l'extension Code Runner si nécessaire

---

## 📚 Ressources

- [NiceGUI Documentation](https://nicegui.io/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Python logging Documentation](https://docs.python.org/3/library/logging.html)
- [pywebview Documentation](https://pywebview.kivy.org/)

---

## 📄 Historique des modifications

### Version 0.1.0 (Initial)
- ✅ Setup de base avec NiceGUI
- ✅ Mode développement avec hot reload
- ✅ Système de logging
- ✅ Gestion des thèmes (light/dark)
- ✅ Configuration VS Code
- ✅ Structure UI modulaire
