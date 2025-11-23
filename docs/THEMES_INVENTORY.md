# Inventaire des Thèmes - Documentation

## 🎯 Objectif

Ce document liste **tous les thèmes** abordés dans la documentation actuelle du projet, avec leur statut d'implémentation et leur pertinence.

## 📊 Résumé

- **Total de documents** : 24 fichiers .md
- **Thèmes implémentés** : 10
- **Thèmes futurs/planifiés** : 5
- **Documents obsolètes** : 6
- **Documents redondants** : 3

## 🟢 Thèmes Implémentés (À Documenter)

### 1. Architecture et Structure

**Fichiers actuels** :

- `ARCHITECTURE.md` (racine)
- `docs/STRUCTURE.md`

**État du code** : ✅ Implémenté
**Vérification nécessaire** :

- Structure des dossiers `src/`, `scripts/`, etc.
- Organisation des modules
- Séparation core/ui

**Nouveau document** : `ARCHITECTURE.md` (racine, fusionné)

---

### 2. Système de Logs

**Fichiers actuels** :

- `docs/LOGGING.md`

**État du code** : ✅ Implémenté (`src/core/services/logger.py`)
**Vérification nécessaire** :

- [ ] Logs en mode dev vont dans `logs/`
- [ ] Logs en mode build_dev vont dans `dist/dev/`
- [ ] Rotation des logs (max 3 fichiers)
- [ ] Niveaux de log (DEBUG, INFO, etc.)
- [ ] Logs colorés en console

**Nouveau document** : `docs_clean/04_LOGGING.md`

---

### 3. Système de Traduction (i18n)

**Fichiers actuels** :

- `docs/TRANSLATION_README.md`
- `docs/CONFIG_BABEL.md`

**État du code** : ✅ Implémenté (`src/core/services/translation.py`, `scripts/translation_management/`)
**Vérification nécessaire** :

- [ ] Extraction des chaînes avec `_("")`
- [ ] Compilation des fichiers .po → .mo
- [ ] Changement de langue dynamique
- [ ] Langues supportées (fr, en, etc.)

**Nouveau document** : `docs_clean/05_TRANSLATION.md` (fusion)

---

### 4. Système de Build

**Fichiers actuels** :

- `docs/MODES_AND_COMPARISON.md`
- Sections dans `ARCHITECTURE.md` et `README.md`

**État du code** : ✅ Implémenté (`scripts/dev_build/build_dev.py`, `scripts/dev_build/build_final.py`)
**Vérification nécessaire** :

- [ ] Build dev (--onedir) fonctionne
- [ ] Build final (--onefile) fonctionne
- [ ] Assets copiés correctement
- [ ] Icône systray visible dans les builds
- [ ] Taille des exécutables

**Nouveau document** : `docs_clean/03_BUILD_SYSTEM.md`

---

### 5. Icône Systray

**Fichiers actuels** :

- Sections dans `ARCHITECTURE.md`

**État du code** : ✅ Implémenté (`src/core/managers/systray.py`)
**Vérification nécessaire** :

- [ ] Icône visible en dev
- [ ] Icône visible en build
- [ ] Menu contextuel fonctionnel
- [ ] Actions (Afficher, Quitter, etc.)

**Nouveau document** : `docs_clean/06_SYSTRAY.md`

---

### 6. Démarrage Automatique

**Fichiers actuels** :

- Sections dans `ARCHITECTURE.md`

**État du code** : ✅ Implémenté (`src/core/managers/autostart.py`)
**Vérification nécessaire** :

- [ ] Activation du démarrage auto
- [ ] Désactivation du démarrage auto
- [ ] Clé de registre Windows correcte
- [ ] Chemin de l'exécutable correct

**Nouveau document** : `docs_clean/07_AUTOSTART.md`

---

### 7. Configuration

**Fichiers actuels** :

- Sections dans `ARCHITECTURE.md`

**État du code** : ✅ Implémenté (`src/core/config/manager.py`, `src/core/config/config.json`)
**Vérification nécessaire** :

- [ ] Chargement de `config.json`
- [ ] Valeurs par défaut
- [ ] Détection mode dev/frozen
- [ ] Chemins des ressources (`get_app_root()`)

**Nouveau document** : `docs_clean/08_CONFIGURATION.md`

---

### 8. Développement (Workflows)

**Fichiers actuels** :

- `docs/DEVELOPMENT.md`

**État du code** : ✅ Implémenté (scripts dans `scripts/`)
**Vérification nécessaire** :

- [ ] `run_dev.py` fonctionne
- [ ] `run_ruff.py` fonctionne
- [ ] `run_pyright.py` fonctionne
- [ ] Tasks VS Code fonctionnent

**Nouveau document** : `docs_clean/02_DEVELOPMENT.md`

---

### 9. Pre-commit Hooks

**Fichiers actuels** :

- `docs/PRECOMMIT.md`
- `docs/RUFF_SETUP.md`

**État du code** : ✅ Implémenté (`.pre-commit-config.yaml`)
**Vérification nécessaire** :

- [ ] Hooks installés
- [ ] Ruff check + format
- [ ] Pyright check
- [ ] Configuration VS Code cohérente

**Nouveau document** : `docs_clean/10_PRECOMMIT.md` (fusion)

---

### 10. Gestion des Assets (Icônes)

**Fichiers actuels** :

- `docs/ICONS.md`

**État du code** : ✅ Implémenté (`src/core/config/icons/`)

**Prochaines étapes** :

- [x] Centralisation dans `src/core/config/icons/` PNG → ICO
- [ ] Centralisation dans `assets/icons/`
- [ ] Utilisation dans l'app et le build

**Nouveau document** : `docs_clean/09_ASSETS.md`

---

## 🔵 Thèmes Futurs (Non Implémentés)

### 11. Raccourcis Clavier Globaux

**Fichiers actuels** :

- `docs/KEYBOARD_SHORTCUTS.md`

**État du code** : ❌ Non implémenté (documentation prématurée)
**Action** : Déplacer vers `docs_clean/99_ROADMAP.md`

---

### 12. Optimisation Mémoire

**Fichiers actuels** :

- `docs/MEMORY_OPTIMIZATION.md`

**État du code** : ❌ Non implémenté (prématuré)
**Action** : Déplacer vers `docs_clean/99_ROADMAP.md`

---

### 13. Stockage de Données

**Fichiers actuels** :

- `docs/storage_strategy.md`

**État du code** : ❌ Non implémenté
**Action** : Déplacer vers `docs_clean/99_ROADMAP.md`

---

### 14. Interface Chat LLM

**Fichiers actuels** :

- `docs/BASE_SOLIDE_PLAN.md`

**État du code** : ❌ Non implémenté (plan futur)
**Action** : Déplacer vers `docs_clean/99_ROADMAP.md`

---

### 15. Système de Plugins

**Fichiers actuels** :

- `docs/BASE_SOLIDE_PLAN.md`

**État du code** : ❌ Non implémenté
**Action** : Déplacer vers `docs_clean/99_ROADMAP.md`

---

## 🔴 Documents Obsolètes (À Supprimer)

### 16. Migration NiceGUI → Flet

**Fichiers actuels** :

- `FLET_MIGRATION.md` (racine)
- `docs/nice_gui.md`

**Raison** : Migration terminée, NiceGUI n'est plus utilisé
**Action** : ❌ Supprimer

---

### 17. Corrections

**Fichiers actuels** :

- `correction.md` (racine)

**Raison** : Document temporaire de corrections
**Action** : ❌ Supprimer

---

### 18. Récapitulatif

**Fichiers actuels** :

- `docs/RECAP.md`

**Raison** : Redondant avec README.md
**Action** : ❌ Supprimer

---

### 19. Todo Lists

**Fichiers actuels** :

- `Todo.md` (racine)
- `docs/todo.md`

**Raison** : Redondant, non à jour
**Action** : ❌ Supprimer

---

### 20. Notes Python

**Fichiers actuels** :

- `docs/PYTHON_NOTES.md`

**Raison** : Notes génériques, pas spécifiques au projet
**Action** : ⚠️ À évaluer (peut-être utile pour débutants)

---

### 21. Styling Guide

**Fichiers actuels** :

- `docs/styling-guide.md`

**Raison** : Non utilisé avec Flet (était pour NiceGUI)
**Action** : ❌ Supprimer ou adapter pour Flet

---

## 📋 Thèmes Additionnels à Documenter

### 22. Tests

**Fichiers actuels** : Aucun (dossier `tests/` existe mais vide)
**État du code** : ⚠️ Partiellement implémenté (pytest configuré)
**Nouveau document** : `docs_clean/11_TESTING.md`

---

### 23. Getting Started

**Fichiers actuels** : Sections dans `README.md`
**État du code** : ✅ Implémenté
**Nouveau document** : `docs_clean/01_GETTING_STARTED.md` (détaillé)

---

### 24. Roadmap

**Fichiers actuels** :

- `docs/roadmap.md`
- `docs/BASE_SOLIDE_PLAN.md`

**État du code** : N/A (futur)
**Nouveau document** : `docs_clean/99_ROADMAP.md` (consolidé)

---

## 📊 Matrice de Mapping

| Ancien Document                | Nouveau Document                   | Action                   |
| ------------------------------ | ---------------------------------- | ------------------------ |
| `ARCHITECTURE.md`              | `ARCHITECTURE.md`                  | Fusionner avec STRUCTURE |
| `docs/STRUCTURE.md`            | `ARCHITECTURE.md`                  | Fusionner                |
| `README.md`                    | `README.md`                        | Mettre à jour            |
| `docs/LOGGING.md`              | `docs_clean/04_LOGGING.md`         | Vérifier et nettoyer     |
| `docs/TRANSLATION_README.md`   | `docs_clean/05_TRANSLATION.md`     | Fusionner                |
| `docs/CONFIG_BABEL.md`         | `docs_clean/05_TRANSLATION.md`     | Fusionner                |
| `docs/MODES_AND_COMPARISON.md` | `docs_clean/03_BUILD_SYSTEM.md`    | Intégrer                 |
| `docs/DEVELOPMENT.md`          | `docs_clean/02_DEVELOPMENT.md`     | Vérifier et améliorer    |
| `docs/PRECOMMIT.md`            | `docs_clean/10_PRECOMMIT.md`       | Fusionner                |
| `docs/RUFF_SETUP.md`           | `docs_clean/10_PRECOMMIT.md`       | Fusionner                |
| `docs/ICONS.md`                | `docs_clean/09_ASSETS.md`          | Intégrer                 |
| `docs/KEYBOARD_SHORTCUTS.md`   | `docs_clean/99_ROADMAP.md`         | Déplacer (futur)         |
| `docs/MEMORY_OPTIMIZATION.md`  | `docs_clean/99_ROADMAP.md`         | Déplacer (futur)         |
| `docs/storage_strategy.md`     | `docs_clean/99_ROADMAP.md`         | Déplacer (futur)         |
| `docs/BASE_SOLIDE_PLAN.md`     | `docs_clean/99_ROADMAP.md`         | Déplacer (futur)         |
| `docs/roadmap.md`              | `docs_clean/99_ROADMAP.md`         | Fusionner                |
| `FLET_MIGRATION.md`            | -                                  | ❌ Supprimer             |
| `docs/nice_gui.md`             | -                                  | ❌ Supprimer             |
| `correction.md`                | -                                  | ❌ Supprimer             |
| `docs/RECAP.md`                | -                                  | ❌ Supprimer             |
| `Todo.md`                      | -                                  | ❌ Supprimer             |
| `docs/todo.md`                 | -                                  | ❌ Supprimer             |
| `docs/PYTHON_NOTES.md`         | -                                  | ⚠️ À évaluer             |
| `docs/styling-guide.md`        | -                                  | ⚠️ À évaluer             |
| -                              | `docs_clean/01_GETTING_STARTED.md` | ✨ Créer                 |
| -                              | `docs_clean/06_SYSTRAY.md`         | ✨ Créer                 |
| -                              | `docs_clean/07_AUTOSTART.md`       | ✨ Créer                 |
| -                              | `docs_clean/08_CONFIGURATION.md`   | ✨ Créer                 |
| -                              | `docs_clean/11_TESTING.md`         | ✨ Créer                 |

## 🎯 Prochaines Étapes

1. **Phase de Vérification** : Vérifier le code pour chaque thème implémenté
2. **Phase de Création** : Créer les nouveaux documents dans `docs_clean/`
3. **Phase de Nettoyage** : Supprimer/archiver les anciens documents
4. **Phase de Validation** : Tester toute la documentation

## 📝 Notes

- Tous les documents dans `docs_clean/` seront numérotés pour faciliter la navigation
- Les documents futurs seront regroupés dans `99_ROADMAP.md`
- Les documents obsolètes seront supprimés après validation
- Les informations redondantes seront consolidées
