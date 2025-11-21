# Guide de Développement - Writing Assistant Pro

Ce document décrit les outils et workflows de développement pour le projet Writing Assistant Pro (Version Flet).

## 📋 Scripts Disponibles

Tous les scripts sont situés dans le dossier `scripts/` et doivent être exécutés avec `uv run python`.

### Scripts de Développement

#### `run_dev.py`

Lance l'application en mode développement.

```bash
uv run python scripts/run_dev.py
```

**Fonctionnalités :**

- Active le mode debug (`--debug`)
- Logs détaillés dans la console
- Utilise les ressources locales

---

#### `run_ruff.py`

Exécute Ruff pour le linting et le formatage du code.

```bash
uv run python scripts/run_ruff.py
```

**Étapes exécutées :**

1. Vérification et correction automatique des problèmes (`check --fix`)
2. Formatage du code (`format`)
3. Vérification finale

**Utilisation recommandée :** Avant chaque commit.

---

#### `run_pyright.py`

Exécute Pyright pour la vérification de types statiques.

```bash
uv run python scripts/run_pyright.py
```

**Utilisation recommandée :** Pour détecter les erreurs de type.

---

### Scripts de Build

#### `build_dev.py`

Crée un exécutable de développement (dossier éclaté).

```bash
uv run python scripts/build_dev.py
```

**Caractéristiques :**

- Format : `--onedir` (Dossier `dist/dev/`)
- Console : Visible par défaut
- Logs : Activés (Console ou `dist/dev/debug.log`)
- Usage : Debugging du packaging

---

#### `build_final.py`

Crée l'exécutable de production (fichier unique).

```bash
uv run python scripts/build_final.py
```

**Caractéristiques :**

- Format : `--onefile` (Fichier `dist/production/Writing Assistant Pro.exe`)
- Console : Masquée (`--windowed`)
- Logs : Désactivés (Silencieux)
- Usage : Distribution finale

---

### Scripts de Traduction

#### `translation_management/update_translations.py`

Met à jour les fichiers de traduction pour toutes les langues configurées.

```bash
uv run python scripts/translation_management/update_translations.py
```

**Fonctionnalités :**

- Extrait les chaînes marquées `_()`
- Met à jour les fichiers `.po`
- Compile les fichiers `.mo`

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

### 4. Tests

```bash
# Exécuter les tests
uv run pytest
```

---

## 🐛 Debugging

### Logs

- **Développement** : Les logs sont écrits dans le dossier `logs/` à la racine du projet (si pas de console) ou directement dans la console.
- **Production** : Pas de logs par défaut.

### Mode Debug

Le mode debug est activé automatiquement avec `run_dev.py` et fournit des logs détaillés.

---

## 💡 Bonnes Pratiques

1. **Toujours utiliser `uv run`** pour exécuter les scripts Python.
2. **Vérifier Ruff et Pyright** avant chaque commit.
3. **Respecter la limite de 100 caractères** par ligne.
4. **Utiliser `from __future__ import annotations`** dans tous les fichiers Python de `src/`.
5. **Utiliser `get_app_root()`** pour les chemins de fichiers.
