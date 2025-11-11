# ✍️ Writing Assistant Pro

Une application desktop pour l'édition de texte construite avec **NiceGUI** et **Python 3.13+**.

## 🚀 Démarrage rapide

### Prérequis
- Python 3.13+
- [UV](https://docs.astral.sh/uv/) (gestionnaire de dépendances)

### Installation

```bash
# Cloner le projet
git clone <repo>
cd writing-assistant-pro

# (Optionnel) Créer et activer l'environnement virtuel
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.\.venv\Scripts\Activate.ps1  # Windows
```

### Lancer l'application

**Mode développement (recommandé) :**
```bash
uv run python scripts/run_dev.py
# ou
uv run python main.py --debug
```

**Mode production :**
```bash
python main.py
```

## 📖 Documentation

Consulte [ARCHITECTURE.md](./ARCHITECTURE.md) pour une description complète de la structure et du workflow de développement.

## 🎯 Fonctionnalités principales

- ✅ Application desktop native (NiceGUI + pywebview)
- ✅ Mode développement avec hot reload
- ✅ Système de logging complet
- ✅ Thèmes light/dark switchables
- ✅ Configuration VS Code intégrée
- ✅ Structure modulaire et extensible

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| UI Framework | NiceGUI |
| Langage | Python 3.13+ |
| Gestionnaire de dépendances | UV |
| Rendu | pywebview (native) |
| Logs | logging (stdlib) |
| Thèmes | CSS |
| IDE recommendé | VS Code |

## 📁 Structure du projet

```
writing-assistant-pro/
├── main.py              # Point d'entrée
├── logger.py            # Logging centralisé
├── styles.py            # Gestion des thèmes
├── ui/                  # Module interface utilisateur
├── scripts/
│   └── run_dev.py       # Lancement mode dev
├── styles/              # Fichiers CSS
│   ├── light.css
│   └── dark.css
└── ARCHITECTURE.md      # Documentation détaillée
```

Pour plus de détails, voir [ARCHITECTURE.md](./ARCHITECTURE.md).

## 🔨 Développement

### Modifier l'interface

Édite le fichier `ui/__init__.py` ou crée de nouveaux modules dans `ui/pages/`.

### Ajouter des logs

```python
from logger import setup_logger
log = setup_logger(debug=DEBUG)
log.debug("Message de debug")
log.info("Information")
```

### Changer de thème

Dans `main.py`, change :
```python
DARK_MODE = True  # Mode sombre
```

## 📝 Commandes utiles

```bash
# Lancer en mode dev avec debug
uv run python main.py --debug

# Lancer sans debug
uv run python main.py

# Installer des dépendances additionnelles
uv add <package>

# Mettre à jour les dépendances
uv sync
```

## 🤝 Contribution

Les contributions sont bienvenues ! Consulte [ARCHITECTURE.md](./ARCHITECTURE.md) pour les conventions de code.

## 📄 Licence

À définir

## 📧 Contact

À définir

---

**Pour plus d'informations, voir [ARCHITECTURE.md](./ARCHITECTURE.md)**
