# Pre-commit Hooks et Qualité de Code

## 📋 Vue d'ensemble

Le projet utilise **pre-commit** pour garantir la qualité du code avant chaque commit. Les outils principaux sont **Ruff** (linter/formateur) et **Pyright** (vérificateur de types).

## 🎯 Objectifs

- Formatage automatique du code
- Détection d'erreurs de syntaxe et de style
- Vérification statique des types
- Prévention des commits de code cassé
- Standardisation du style de code

## 🏗️ Architecture

### Configuration

- [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) - Configuration des hooks

### Outils

- **Ruff** : Remplaçant ultra-rapide de Flake8, Black, isort, etc.
- **Pyright** : Vérificateur de types statique performant.
- **Standard Hooks** : Vérifications de base (YAML, JSON, fichiers larges, etc.).

### Scripts Utilitaires

- [`scripts/quality/run_ruff.py`](../scripts/quality/run_ruff.py) - Lance Ruff (check + format)
- [`scripts/quality/run_pyright.py`](../scripts/quality/run_pyright.py) - Lance Pyright

## 🔧 Hooks Configurés

| Hook                      | Outil      | Description                                  |
| ------------------------- | ---------- | -------------------------------------------- |
| `ruff`                    | Ruff       | Linter avec correction automatique (`--fix`) |
| `ruff-format`             | Ruff       | Formateur de code (style Black)              |
| `pyright`                 | Pyright    | Vérification de types statique               |
| `check-yaml`              | Pre-commit | Valide la syntaxe YAML                       |
| `check-json`              | Pre-commit | Valide la syntaxe JSON                       |
| `check-added-large-files` | Pre-commit | Bloque les fichiers > 1MB                    |
| `check-merge-conflict`    | Pre-commit | Détecte les marqueurs de conflit Git         |

## 🚀 Utilisation

### Installation

Les hooks sont installés automatiquement lors de l'initialisation de l'environnement de développement.

```bash
# Installer manuellement si nécessaire
uv run pre-commit install
```

> [!IMPORTANT] > **N'installez PAS le hook pre-push** avec `uv run pre-commit install --hook-type pre-push`.
>
> **Raison** : Notre configuration `.pre-commit-config.yaml` n'utilise **aucun** `stages: [push]`.
> Tous les hooks s'exécutent uniquement au **commit**.
>
> **Problème si installé** : Le hook pre-push s'exécuterait quand même à chaque push et
> relancerait **tous les hooks** (comportement par défaut), créant une vérification redondante
> et ralentissant vos push.
>
> **Vérifier si installé** :
>
> ```bash
> # Sous Windows PowerShell
> Test-Path .git\hooks\pre-push
>
> # Sous Linux/Mac
> test -f .git/hooks/pre-push && echo "Installé" || echo "Non installé"
> ```
>
> **Désinstaller si nécessaire** :
>
> ```bash
> # Windows PowerShell
> Remove-Item .git\hooks\pre-push -Force
>
> # Linux/Mac
> rm .git/hooks/pre-push
> ```

### Exécution Manuelle

Vous pouvez lancer les vérifications manuellement sans commiter :

```bash
# Lancer tous les hooks sur tous les fichiers
uv run pre-commit run --all-files
```

### Scripts Dédiés

Pour un usage plus ciblé pendant le développement :

**Ruff (Lint + Format)**

```bash
uv run python scripts/quality/run_ruff.py
```

**Pyright (Types)**

```bash
uv run python scripts/quality/run_pyright.py
```

## ⚙️ Workflow Recommandé

1. **Coder** : Faire vos modifications.
2. **Vérifier** : Lancer `scripts/quality/run_ruff.py` pour formater et corriger.
3. **Typer** : Lancer `scripts/quality/run_pyright.py` pour vérifier les types.
4. **Commiter** : `git commit ...`
   - Les hooks se lancent automatiquement.
   - Si un hook échoue (ex: formatage modifié), le commit est bloqué.
   - Vérifiez les modifications et re-commitez.

## ⚠️ Dépannage

### Le commit est bloqué par Ruff

**Cause** : Ruff a modifié des fichiers pour les formater.

**Solution** :

1. Ajoutez les modifications faites par Ruff : `git add .`
2. Relancez le commit : `git commit ...`

### Le commit est bloqué par Pyright

**Cause** : Erreur de type détectée.

**Solution** :

1. Corrigez l'erreur dans le code.
2. Ajoutez le fichier : `git add ...`
3. Relancez le commit.

### Ignorer les Hooks (Déconseillé)

En cas d'urgence absolue :

```bash
git commit -m "Message" --no-verify
```

## 🔗 Références

### Code Source

- [`.pre-commit-config.yaml`](../.pre-commit-config.yaml)
- [`scripts/quality/run_ruff.py`](../scripts/quality/run_ruff.py)
- [`scripts/quality/run_pyright.py`](../scripts/quality/run_pyright.py)

### Documentation Externe

- [Pre-commit](https://pre-commit.com/)
- [Ruff](https://docs.astral.sh/ruff/)
- [Pyright](https://github.com/microsoft/pyright)
