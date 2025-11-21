# Configuration Pre-commit

## Qu'est-ce que pre-commit ?

Pre-commit est un outil qui exécute automatiquement des vérifications sur ton code **avant** que tu ne commites ou pousses. Ça garantit que ton code respecte toujours les standards de qualité.

## Les hooks installés

### 1. Ruff (formateur et linter Python)

- **Rôle** : Corrige automatiquement le style du code Python
- **Quand** : Au commit
- **Exemple** : Réorganise les imports, enlève les variables inutilisées, etc.

### 2. Pyright (vérificateur de types)

- **Rôle** : Vérifie les annotations de types Python
- **Quand** : Au commit
- **Exemple** : Détecte si tu passes un `str` là où il faut un `int`

### 3. Hooks de nettoyage des fichiers

Ces hooks **modifient** tes fichiers pour les nettoyer :

- `trailing-whitespace` : Supprime les espaces en fin de ligne
- `end-of-file-fixer` : Ajoute une ligne vide à la fin des fichiers
- `mixed-line-ending` : Force les sauts de ligne Unix (LF au lieu de CRLF)

**Quand** : Au **push** uniquement (c'était ça le problème !)

### 4. Hooks de vérification

Ces hooks **ne modifient pas** les fichiers, ils vérifient juste :

- `check-yaml` : Vérifie la syntaxe des fichiers YAML
- `check-json` : Vérifie la syntaxe des fichiers JSON
- `check-toml` : Vérifie la syntaxe des fichiers TOML
- `check-added-large-files` : Bloque les fichiers > 1 Mo
- `check-merge-conflict` : Détecte les marqueurs de conflit Git

**Quand** : Au commit ET au push

## Problème initial et solution

### Le problème

Quand tu committais, les hooks de nettoyage (trailing-whitespace, etc.) **modifiaient** tes fichiers **après** que tu les aies stagés. Résultat :

- Fichier stagé (version avant hook)
- Fichier modifié (version après hook)
- Git confus → commit bloqué avec le message "Unstaged files detected"

### La solution : `stages: [push]`

En mettant `stages: [push]` sur les hooks qui modifient les fichiers, ils ne tournent plus au commit mais seulement au push.

**Avantages :**

1. Le commit n'est plus bloqué
2. Les hooks tournent quand même (au push), donc la qualité est garantie
3. Tu peux commit normalement avec VS Code

## Installation

```bash
# Installe les hooks pour la phase commit
uv run pre-commit install

# Installe les hooks pour la phase push
uv run pre-commit install --hook-type pre-push
```

**Important :** Les deux commandes sont nécessaires car on utilise maintenant les deux phases (commit ET push).

## Configuration VS Code

Pour que VS Code crée déjà des fichiers conformes et éviter que les hooks aient besoin de les modifier :

```json
{
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.eol": "\n"
}
```

Ajoute ça dans `.vscode/settings.json`.

## Workflow normal

1. **Tu modifies des fichiers**
2. **Tu stage tes modifications** (avec VS Code ou `git add`)
3. **Tu commit** → Les hooks de vérification tournent (pyright, ruff, check-yaml, etc.)
4. **Tu push** → Les hooks de nettoyage tournent (trailing-whitespace, etc.)

Si un hook au push modifie des fichiers :

- Le push est annulé
- Tu vois les modifications dans VS Code
- Tu les stages et re-push

## Lancer les hooks manuellement

Pour tester tous les hooks sans commit/push :

```bash
uv run pre-commit run --all-files
```

## Résumé

| Hook                 | Type         | Phase         | Modifie les fichiers ? |
| -------------------- | ------------ | ------------- | ---------------------- |
| ruff                 | Linter       | Commit        | Oui                    |
| pyright              | Type checker | Commit        | Non                    |
| trailing-whitespace  | Nettoyage    | Push          | Oui                    |
| end-of-file-fixer    | Nettoyage    | Push          | Oui                    |
| mixed-line-ending    | Nettoyage    | Push          | Oui                    |
| check-yaml/json/toml | Vérification | Commit + Push | Non                    |
| check-large-files    | Vérification | Commit + Push | Non                    |

**La règle :** Les hooks qui **modifient** sont en phase **push**, les autres en phase **commit** (ou les deux).
