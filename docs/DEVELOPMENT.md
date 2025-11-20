# Guide de Développement - Writing Assistant Pro

Ce document décrit les outils et workflows de développement pour le projet Writing Assistant Pro.

## 📋 Scripts Disponibles

Tous les scripts sont situés dans le dossier `scripts/` et doivent être exécutés avec `uv run python`.

### Scripts de Développement

#### `run_dev.py`

Lance l'application en mode développement avec debug activé.

```bash
uv run python scripts/run_dev.py
```

**Fonctionnalités :**

- Active le mode debug
- Logs détaillés
- Rechargement automatique (selon configuration)

---

#### `run_ruff.py`

Exécute Ruff pour le linting et le formatage du code.

```bash
uv run python scripts/run_ruff.py
```

**Étapes exécutées :**

1. Vérification et correction automatique des problèmes
2. Formatage du code
3. Vérification finale

**Utilisation recommandée :** Avant chaque commit

---

#### `run_pyright.py`

Exécute Pyright pour la vérification de types statiques.

```bash
uv run python scripts/run_pyright.py
```

**Utilisation recommandée :**

- Après modifications de code avec annotations de type
- Avant chaque commit
- Pour détecter les erreurs de type que l'IDE pourrait manquer

---

### Scripts de Build

#### `build_dev.py`

Crée un exécutable de développement avec console.

```bash
uv run python scripts/build_dev.py
```

**Caractéristiques :**

- Console visible pour debugging
- Utilise `data_dev.json`
- Sortie : `dist/dev/`

---

#### `build_final.py`

Crée l'exécutable de production.

```bash
uv run python scripts/build_final.py
```

**Caractéristiques :**

- Pas de console (mode windowed)
- Utilise `data.json`
- Sortie : `dist/production/`

---

### Scripts de Traduction

#### `translation_management/update_translations.py`

Met à jour les fichiers de traduction pour toutes les langues configurées.

```bash
uv run python scripts/translation_management/update_translations.py
```

**Fonctionnalités :**

- Lit les langues depuis `src/core/config.json`
- Crée les dossiers manquants
- Génère les fichiers JSON de traduction

---

## 🔧 Workflow de Développement Recommandé

### 1. Avant de Commencer

```bash
# Mettre à jour les dépendances
uv sync
```

### 2. Pendant le Développement

```bash
# Lancer l'application en mode dev
uv run python scripts/run_dev.py
```

### 3. Avant de Commiter

**Vérifications obligatoires :**

```bash
# 1. Linting et formatage
uv run python scripts/run_ruff.py

# 2. Vérification des types
uv run python scripts/run_pyright.py
```

**Ou utiliser le pre-commit hook (voir section suivante)**

### 4. Tests

```bash
# Exécuter les tests
uv run pytest
```

---

## 🪝 Pre-commit Hooks

Le projet utilise `pre-commit` pour automatiser les vérifications avant chaque commit.

### Installation

```bash
# Installer pre-commit
uv add --dev pre-commit

# Activer les hooks
uv run pre-commit install
```

### Utilisation

Les hooks s'exécutent automatiquement à chaque `git commit`. Pour les exécuter manuellement :

```bash
# Sur tous les fichiers
uv run pre-commit run --all-files

# Sur les fichiers staged uniquement
uv run pre-commit run
```

### Contourner les Hooks

En cas d'urgence (à utiliser avec précaution) :

```bash
git commit --no-verify -m "message"
```

---

## 🎯 Tâches VS Code

Le projet inclut des tâches VS Code configurées dans `.vscode/tasks.json` :

- **Run Ruff** : Linting et formatage
- **Run Pyright** : Vérification de types
- **Run Dev** : Lancer l'application
- **Run Tests** : Exécuter pytest
- **Build Dev** : Build développement
- **Build Final** : Build production

**Accès :** `Ctrl+Shift+P` → "Tasks: Run Task"

Des boutons sont également disponibles dans la barre d'état grâce à l'extension "Task Buttons".

---

## 📚 Documentation Additionnelle

- [`docs/LOGGING.md`](file:///c:/Users/dd200/Documents/Mes_projets/WritingTools%20Related/writing-assistant-pro/docs/LOGGING.md) - Système de logging avec Loguru
- [`docs/PYTHON_NOTES.md`](file:///c:/Users/dd200/Documents/Mes_projets/WritingTools%20Related/writing-assistant-pro/docs/PYTHON_NOTES.md) - Notes et règles Python du projet
- [`README.md`](file:///c:/Users/dd200/Documents/Mes_projets/WritingTools%20Related/writing-assistant-pro/README.md) - Vue d'ensemble du projet

---

## 🐛 Debugging

### Logs

Les logs sont stockés dans `logs/` :

- `app.log` - Logs de l'application
- Rotation automatique configurée

### Mode Debug

Le mode debug est activé automatiquement avec `run_dev.py` et fournit :

- Logs détaillés dans la console
- Informations de débogage supplémentaires
- Traceback complets

---

## 💡 Bonnes Pratiques

1. **Toujours utiliser `uv run`** pour exécuter les scripts Python
2. **Vérifier Ruff et Pyright** avant chaque commit
3. **Tester localement** avant de pousser
4. **Documenter** les nouvelles fonctionnalités
5. **Respecter la limite de 100 caractères** par ligne (même commentaires)
6. **Utiliser `from __future__ import annotations`** dans tous les fichiers Python de `src/`

---

## 🔍 Résolution de Problèmes

### Erreurs de Type (Pyright)

Si Pyright signale des erreurs :

1. Vérifier les annotations de type
2. Consulter la documentation de la bibliothèque concernée
3. Utiliser `# type: ignore` en dernier recours avec un commentaire explicatif

### Erreurs de Linting (Ruff)

Ruff corrige automatiquement la plupart des problèmes. Si une erreur persiste :

1. Lire le message d'erreur
2. Consulter la documentation Ruff pour la règle spécifique
3. Utiliser `# noqa: <code>` si nécessaire avec justification

### Build Échoue

1. Vérifier que toutes les dépendances sont installées : `uv sync`
2. Nettoyer les builds précédents : supprimer `dist/` et `build/`
3. Vérifier les logs de build pour les erreurs spécifiques
