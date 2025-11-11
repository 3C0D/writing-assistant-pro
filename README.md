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

## 📖 Fonctionnalités

- ✅ Application desktop native (NiceGUI + pywebview)
- ✅ Mode développement avec hot reload
- ✅ Système de logging complet
- ✅ Thèmes light/dark switchables
- ✅ Système de traduction intégré (gettext)
- ✅ Structure modulaire et extensible

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| UI Framework | NiceGUI |
| Langage | Python 3.13+ |
| Gestionnaire de dépendances | UV |
| Rendu | pywebview (native) |
| Traductions | Gettext (Babel) |
| IDE recommandé | VS Code |

## 📁 Structure du projet

```
writing-assistant-pro/
├── main.py                      # Point d'entrée
├── src/                         # Code source
│   ├── core/
│   │   ├── config.py            # Configuration globale
│   │   ├── logger.py            # Logging centralisé
│   │   ├── styles.py            # Gestion des thèmes
│   │   └── translation.py       # Module de traduction
│   └── ui/                      # Interface utilisateur
├── scripts/                     # Scripts utilitaires
│   ├── run_dev.py               # Lancement mode dev
│   └── translation_management/  # Outils de traduction
├── styles/                      # Fichiers CSS (thèmes)
├── translations/                # Fichiers de traduction
└── docs/                        # Documentation détaillée
```

## 📚 Documentation complète

| Document | Emplacement | Description | Lignes |
|----------|-------------|-------------|--------|
| **README** | `README.md` | Démarrage rapide et présentation | - |
| **ARCHITECTURE** | `ARCHITECTURE.md` | Architecture complète, composants, workflow | 379 |
| **STRUCTURE** | `docs/STRUCTURE.md` | Détails structure fichiers et rôles | 213 |
| **CONFIG BABEL** | `docs/CONFIG_BABEL.md` | Configuration système de traduction | 59 |
| **NICE GUI** | `docs/nice_gui.md` | Guide d'utilisation NiceGUI | 163 |
| **RECAP** | `docs/RECAP.md` | Récapitulatif global du projet | 126 |
| **TRANSLATION** | `docs/TRANSLATION_README.md` | Guide complet des traductions | 156 |

### Contenu détaillé de chaque document

**ARCHITECTURE.md (379 lignes)**
- Vue d'ensemble des composants NiceGUI
- Structure détaillée avec `.babelrc` et `babel.cfg`
- Composants clés : main.py, logger.py, styles.py, ui/__init__.py
- Workflow de développement (dev/production)
- Gestion des thèmes light/dark
- Système de traduction avec Babel
- Configuration VS Code et conventions de code

**docs/STRUCTURE.md (213 lignes)**
- Structure complète avec tous les fichiers
- Explication détaillée des rôles de chaque composant
- `src/core/` (config, logger, styles, translation)
- `src/ui/` (interface utilisateur)
- `scripts/` (utilitaires)
- `styles/` (thèmes CSS)
- `translations/` (fichiers .po/.mo)

**docs/CONFIG_BABEL.md (59 lignes)**
- Configuration `babel.cfg` (extraction)
- Configuration `.babelrc` (init/update/compile)
- Workflow en 3 étapes automatisé
- Commande unique de mise à jour

**docs/nice_gui.md (163 lignes)**
- Guide complet d'utilisation NiceGUI
- Mode natif (pywebview) vs navigateur
- Packaging en application installable
- Exemples d'interface moderne

**docs/RECAP.md (126 lignes)**
- Récapitulatif des modifications de la session complète
- Objectifs réalisés et résultats
- Structure finale et fonctionnalités

**docs/TRANSLATION_README.md (156 lignes)**
- Guide complet du système de traduction
- Workflow pratique étape par étape
- Comment ajouter du texte à traduire
- Ajout de nouvelles langues
- Dépannage et outils graphiques

## 🔧 Développement

### Modifier l'interface
Édite le fichier `src/ui/__init__.py` ou crée de nouveaux modules dans `src/ui/`.

### Ajouter des traductions
```python
from src.core import _
ui.label(_("Texte à traduire"))
```

Puis met à jour les traductions :
```bash
uv run python scripts/translation_management/update_translations.py
```

### Changer de thème
Dans `src/core/config.py`, modifie `DARK_MODE` :
```python
DARK_MODE = True  # Mode sombre
```

## 📝 Commandes utiles

```bash
# Lancer en mode dev avec hot reload
uv run python scripts/run_dev.py

# Installer des dépendances
uv add <package>

# Mettre à jour les traductions
uv run python scripts/translation_management/update_translations.py

# Mode debug détaillé
uv run python main.py --debug
```

---

**Pour plus d'informations détaillées, voir [ARCHITECTURE.md](./ARCHITECTURE.md)**
