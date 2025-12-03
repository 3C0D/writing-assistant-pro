# Prompt pour Commits Conventionnels

Utilisez ce prompt avec votre assistant LLM (GitHub Copilot, Gemini, etc.)
pour générer des messages de commit respectant le format conventionnel.

---

## Prompt Template

```
Génère un message de commit conventionnel pour les changements suivants.

Format requis : <type>[optional scope]: <description>

Types disponibles :
- feat: nouvelle fonctionnalité (bump MINOR, ex: 1.0.0 → 1.1.0)
- fix: correction de bug (bump PATCH, ex: 1.0.0 → 1.0.1)
- docs: documentation uniquement (pas de bump)
- style: formatage du code (pas de bump)
- refactor: refactorisation (pas de bump)
- test: ajout de tests (pas de bump)
- chore: maintenance (pas de bump)
- perf: amélioration de performance (bump PATCH)
- ci: modifications CI/CD (pas de bump)

Pour un breaking change (bump MAJOR, ex: 1.0.0 → 2.0.0) :
- Ajoute ! après le type (e.g., feat!: ...)
- OU ajoute "BREAKING CHANGE:" dans le footer

Règles strictes :
1. Le message DOIT être en anglais
2. La description doit être concise (max 72 caractères)
3. Utilise l'impératif présent (add, not added)
4. Pas de majuscule au début de la description
5. Pas de point à la fin de la description

Changements effectués :
[DÉCRIS ICI TES CHANGEMENTS OU COLLE TON GIT DIFF]

Fournis uniquement le message de commit, rien d'autre.
Ne donne pas d'explications supplémentaires.
```

---

## Exemples de Messages Valides

### Feature (MINOR bump)

```
feat: add support for custom keyboard shortcuts
feat(ui): implement dark mode toggle in settings
feat(systray): add context menu with quick actions
```

### Bug Fix (PATCH bump)

```
fix: resolve systray icon not appearing in production
fix(config): correct default language detection
fix(shortcuts): prevent duplicate hotkey registration
```

### Breaking Change (MAJOR bump)

```
feat!: redesign settings UI with new structure

BREAKING CHANGE: Settings structure has completely changed.
Users will need to reconfigure their preferences after update.
```

### Documentation

```
docs: update release process documentation
docs(api): add examples for keyboard shortcuts API
```

### Maintenance

```
chore: update dependencies to latest versions
chore(deps): bump flet to 0.24.1
```

---

## Utilisation dans VS Code

### Méthode 1 : Copilot Chat

1. Ouvre le panneau Copilot Chat
2. Colle le prompt ci-dessus
3. Remplace `[DÉCRIS ICI...]` par tes changements
4. Copie le message généré dans l'interface Git

### Méthode 2 : Inline Chat

1. Stage tes changements
2. Ouvre l'inline chat dans le message de commit (Ctrl+I)
3. Colle le prompt avec tes changements
4. Valide le message généré

### Méthode 3 : Extension LLM

Si tu utilises une extension LLM personnalisée :

1. Configure l'extension pour utiliser ce prompt
2. Lie-le à un raccourci clavier
3. Génère automatiquement tes commits

---

## Validation Automatique

Le pre-commit hook valide automatiquement que ton message respecte le
format Conventional Commits. Si le hook rejette ton commit :

1. Vérifie que le type est correct (feat, fix, docs, etc.)
2. Vérifie qu'il n'y a pas de majuscule au début
3. Vérifie qu'il n'y a pas de point à la fin
4. Vérifie que la description est en anglais

---

## Références

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
- Documentation complète : `docs/COMMITIZEN.md`
- Processus de release : `docs/13_RELEASE_PROCESS.md`
