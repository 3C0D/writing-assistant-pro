# 🔧 Configuration Babel - Writing Assistant Pro

## Fichiers de configuration

### `babel.cfg`

- **Rôle** : Configuration pour l'extraction des textes translatable
- **Utilisé par** : `pybabel extract` (Step 1)
- **Contenu** :

  ```ini
  [python: src/**.py]
  [python: **.py]
  
  [extractors]
  ignore_extensions = .pyc,.pyo,.egg-info,.git
  ignore_patterns = ^\.
  ```

### `.babelrc`

- **Rôle** : Configuration pour init/update/compile
- **Utilisé par** : `pybabel init`, `pybabel update`, `pybabel compile` (Steps 2-3)
- **Contenu** :

  ```ini
  [extract_messages]
  output_file = translations/template.pot

  [init_catalog]
  domain = writing_assistant
  input_file = translations/template.pot
  output_dir = translations

  [update_catalog]
  domain = writing_assistant
  input_file = translations/template.pot
  output_dir = translations

  [compile_catalog]
  domain = writing_assistant
  directory = translations
  ```

## Workflow

Le script `scripts/translation_management/update_translations.py` automatise tout en 3 étapes :

1. **Extract** : Utilise `babel.cfg` pour extraire les textes du code `src/`
2. **Update/Init** : Crée ou met à jour les fichiers `.po` pour chaque langue
3. **Compile** : Génère les fichiers `.mo` binaires pour l'app

## Commande unique

```bash
uv run python scripts/translation_management/update_translations.py
```

**C'est tout ce qu'il y a à retenir ! 🎯**
