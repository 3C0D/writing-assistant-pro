# Tests Automatisés

## 📋 Vue d'ensemble

Le projet utilise **pytest** pour les tests unitaires et d'intégration. Les tests assurent la stabilité des composants critiques comme la configuration, la traduction et la logique métier.

## 🎯 Objectifs

- Valider le bon fonctionnement des modules
- Prévenir les régressions
- Documenter le comportement attendu via les tests
- Faciliter le refactoring

## 🏗️ Architecture

### Dossier `tests/`

```
tests/
├── conftest.py       # Fixtures partagées (config temporaire, etc.)
├── test_config.py    # Tests du gestionnaire de configuration
└── [autres tests]
```

### Outils

- **pytest** : Framework de test.
- **pytest-cov** (optionnel) : Couverture de code.

## 🚀 Lancer les Tests

### Tous les Tests

```bash
uv run pytest
```

### Un Fichier Spécifique

```bash
uv run pytest tests/test_config.py
```

### Avec Logs (Mode Verbeux)

```bash
uv run pytest -v -s
```

## 📝 Écrire des Tests

### Structure d'un Test

```python
def test_ma_fonction():
    # 1. Arrange (Préparation)
    data = "test"

    # 2. Act (Action)
    result = ma_fonction(data)

    # 3. Assert (Vérification)
    assert result == "attendu"
```

### Utiliser les Fixtures (`conftest.py`)

Des fixtures sont disponibles pour simuler l'environnement.

Exemple avec `temp_config_file` (crée un fichier config temporaire) :

```python
def test_config_persistence(temp_config_file):
    # temp_config_file est injecté automatiquement par pytest
    config = ConfigManager(config_file=str(temp_config_file))
    # ...
```

## 🧪 Tests Existants

### Configuration (`test_config.py`)

- Chargement des valeurs par défaut.
- Persistance (Sauvegarde/Rechargement).
- Accès par attributs (`config.KEY`).

## ⚠️ Bonnes Pratiques

1. **Nommage** : Les fichiers de test doivent commencer par `test_`. Les fonctions aussi.
2. **Indépendance** : Chaque test doit être indépendant (ne pas dépendre de l'état laissé par un autre test).
3. **Mocking** : Utiliser `unittest.mock` pour isoler les composants (ex: ne pas faire de vrais appels réseau ou système de fichiers si possible).
4. **Couverture** : Viser à tester les cas nominaux (succès) et les cas d'erreur (exceptions).

## 🔗 Références

- [pytest Documentation](https://docs.pytest.org/)
