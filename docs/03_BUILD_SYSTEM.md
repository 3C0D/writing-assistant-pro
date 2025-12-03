# Système de Build

## 📋 Vue d'ensemble

Le projet utilise **PyInstaller** pour créer des exécutables autonomes. Deux modes de build sont disponibles : **développement** (debug) et **production** (distribution).

## 🎯 Objectifs

- Builds automatisés avec PyInstaller
- Mode dev pour le débogage
- Mode production pour la distribution
- Gestion automatique des assets et dépendances
- Optimisation de la taille et des performances

## 🏗️ Architecture

### Scripts de Build

| Script                                                  | Mode          | Format      | Console         | Logs       | Usage        |
| ------------------------------------------------------- | ------------- | ----------- | --------------- | ---------- | ------------ |
| [`build_dev.py`](../scripts/dev_build/build_dev.py)     | Développement | `--onedir`  | Visible/Masquée | Activés    | Débogage     |
| [`build_final.py`](../scripts/dev_build/build_final.py) | Production    | `--onefile` | Masquée         | Désactivés | Distribution |

### Fichiers Utilitaires

- [`scripts/dev_build/build_utils.py`](../scripts/dev_build/build_utils.py) - Fonctions communes aux builds

## 📂 Structure des Builds

### Build Dev (`dist/dev/`)

```
dist/dev/
├── Writing Assistant Pro.exe    # Exécutable principal
├── _internal/                    # Dépendances Python
│   ├── flet/                     # Framework Flet
│   ├── loguru/                   # Logger
│   └── [autres dépendances]
├── assets/                       # Ressources copiées
│   ├── icons/
│   └── [autres assets]
├── translations/                 # Fichiers de traduction
│   ├── fr/LC_MESSAGES/
│   └── [autres langues]
└── config.json                   # Configuration
```

**Caractéristiques** :

- Format dossier éclaté (`--onedir`)
- Dossier `_internal/` visible
- Facile à déboguer
- Taille : ~35-40 MB

### Build Final (`dist/production/`)

```
dist/production/
└── Writing Assistant Pro.exe    # Exécutable autonome
```

**Caractéristiques** :

- Format fichier unique (`--onefile`)
- Tout est embarqué dans l'exe
- Prêt pour distribution
- Taille : ~20-25 MB

## 🚀 Utilisation

### Build Développement

#### Mode Console (par défaut)

```bash
uv run python scripts/build_dev.py
```

**Résultat** :

- Console visible
- Logs dans console + `logs/build_dev.log`
- Application lancée automatiquement

#### Mode Windowed

```bash
uv run python scripts/build_dev.py --windowed
```

**Résultat** :

- Pas de console
- Logs dans `logs/build_dev.log`
- Application lancée automatiquement

#### Build Propre

```bash
uv run python scripts/build_dev.py --clean
```

**Résultat** :

- Nettoie le cache PyInstaller
- Build depuis zéro
- Plus lent mais plus fiable

### Build Production

```bash
uv run python scripts/build_final.py
```

**Résultat** :

- Exécutable unique dans `dist/production/`
- Console masquée
- Logs désactivés
- Prêt pour distribution

## ⚙️ Configuration

### Options PyInstaller

#### Build Dev

```python
pyinstaller_command = [
    "uv", "run", "-m", "PyInstaller",
    "--onedir",                    # Dossier éclaté
    "--console",                   # ou --windowed
    "--icon=src/core/config/icons/app_icon.png",
    "--name=Writing Assistant Pro",
    "--distpath=dist/dev",
    "--collect-all", "flet",       # Collecter assets Flet
]
```

#### Build Final

```python
pyinstaller_command = [
    "uv", "run", "-m", "PyInstaller",
    "--onefile",                   # Fichier unique
    "--windowed",                  # Pas de console
    "--icon=assets/icons/app_icon.png",
    "--name=Writing Assistant Pro",
    "--distpath=dist/production",
    "--clean",                     # Toujours propre
    "--collect-all", "flet",
]
```

### Exclusions de Modules

Pour réduire la taille, certains modules sont exclus :

```python
PYINSTALLER_EXCLUSIONS = [
    "tkinter",
    "unittest",
    "test",
    "distutils",
    # Ajouter d'autres modules non utilisés
]
```

## 🔧 Fonctionnalités Avancées

### Auto-Clean Intelligent (Build Dev)

Le système détecte automatiquement les changements Git et nettoie le cache si nécessaire :

```python
def should_auto_clean() -> bool:
    """Détecte si un nettoyage est nécessaire"""
    # Vérifie le dernier commit
    # Compare avec le cache de build
    # Retourne True si différence > 10 minutes
```

**Avantages** :

- Builds rapides en temps normal
- Nettoyage automatique après Git operations
- Évite les builds corrompus

### Gestion des Processus

Avant chaque build, les processus existants sont terminés :

```python
terminate_existing_processes(
    exe_name="Writing Assistant Pro.exe",
    script_name="main.py"
)
```

### Copie Automatique des Fichiers

Les fichiers nécessaires sont copiés automatiquement :

```python
copy_required_files(mode="development", dist_subdir="dev")
```

**Fichiers copiés** :

- `assets/` → `dist/dev/assets/`
- `translations/` → `dist/dev/translations/`
- `config.json` → `dist/dev/config.json`

### Timer de Build

Affiche la durée du build :

```python
timer = BuildTimer()
timer.start()
# ... build ...
timer.print_duration("development build")
```

## 📊 Comparaison des Modes

| Aspect             | Build Dev            | Build Final              |
| ------------------ | -------------------- | ------------------------ |
| **Format**         | `--onedir` (dossier) | `--onefile` (exe unique) |
| **Console**        | Configurable         | Toujours masquée         |
| **Logs**           | Activés              | Désactivés               |
| **Taille**         | ~35-40 MB            | ~20-25 MB                |
| **Vitesse build**  | Rapide (cache)       | Lent (toujours clean)    |
| **Débogage**       | Facile               | Difficile                |
| **Distribution**   | Non                  | Oui                      |
| **Lancement auto** | Oui                  | Non                      |

## 🔍 Workflow Complet

### Build Dev

1. **Nettoyage** (si nécessaire)

   - Détection auto des changements Git
   - Nettoyage du cache PyInstaller

2. **Préparation**

   - Copie des fichiers requis
   - Terminaison des processus existants
   - Vérification de l'icône

3. **Build PyInstaller**

   - Création de l'exécutable
   - Collection des dépendances Flet
   - Exclusion des modules inutiles

4. **Post-Build**

   - Déplacement des fichiers
   - Nettoyage du dossier temporaire

5. **Lancement**
   - Lancement automatique de l'exe
   - Affichage du chemin du log

### Build Final

1. **Nettoyage Complet**

   - Suppression de `build/`
   - Suppression de `dist/production/`
   - Suppression des `.spec`

2. **Préparation**

   - Copie des fichiers requis
   - Terminaison des processus existants

3. **Build PyInstaller**

   - Création de l'exécutable unique
   - Mode `--clean` forcé
   - Optimisation maximale

4. **Résultat**
   - Exécutable dans `dist/production/`
   - Prêt pour distribution

## ⚠️ Problèmes Courants

### Build Échoue avec "Module not found"

**Cause** : Dépendance manquante dans PyInstaller

**Solution** :

```python
# Ajouter dans build_dev.py ou build_final.py
pyinstaller_command.extend(["--hidden-import", "nom_du_module"])
```

### Icône ne s'Affiche Pas

**Cause** : Fichier `app_icon.png` manquant dans `assets/icons/`

**Solution** :

Vérifiez que le fichier `src/core/config/icons/app_icon.png` existe bien. PyInstaller gère nativement le format PNG, aucune conversion en `.ico` n'est nécessaire.

### Build Très Lent

**Cause** : Cache PyInstaller corrompu

**Solution** :

```bash
# Forcer un build propre
uv run python scripts/build_dev.py --clean
```

### Exécutable ne se Lance Pas

**Vérifier** :

1. Les logs dans `logs/build_dev.log`
2. Les dépendances manquantes
3. Les chemins de fichiers

**Solution** :

```bash
# Lancer en mode console pour voir les erreurs
uv run python scripts/build_dev.py --console
```

### Taille de l'Exécutable Trop Grande

**Optimisations** :

1. Ajouter plus d'exclusions
2. Utiliser `--onefile` (production)
3. Compresser avec UPX (optionnel)

```python
# Ajouter dans PYINSTALLER_EXCLUSIONS
PYINSTALLER_EXCLUSIONS = [
    "tkinter",
    "unittest",
    "test",
    "matplotlib",  # Si non utilisé
    "numpy",       # Si non utilisé
]
```

## 🔗 Dépendances

### Requises pour le Build

```toml
[project.optional-dependencies]
build = [
    "pyinstaller>=6.0.0",
]
```

### Installation

```bash
uv sync --extra build
```

## 📝 Bonnes Pratiques

### 1. Tester en Build Dev Avant Production

```bash
# Toujours tester d'abord en dev
uv run python scripts/build_dev.py --console

# Puis en production
uv run python scripts/build_final.py
```

### 2. Vérifier les Logs

```bash
# Vérifier les logs après build
cat logs/build_dev.log
```

### 3. Nettoyer Régulièrement

```bash
# Build propre après changements importants
uv run python scripts/build_dev.py --clean
```

### 4. Versionner les Builds

```bash
# Renommer l'exe avec version
cp "dist/production/Writing Assistant Pro.exe" \
   "dist/production/Writing Assistant Pro v1.0.0.exe"
```

## 🚧 Améliorations Futures

### Versioning Automatique

Ajouter la version dans le nom de l'exécutable automatiquement.

### Compression UPX

Réduire la taille avec UPX :

```python
pyinstaller_command.append("--upx-dir=/path/to/upx")
```

### Signature de Code

Signer l'exécutable pour Windows :

```bash
signtool sign /f certificate.pfx /p password "Writing Assistant Pro.exe"
```

### Création d'Installeur

Créer un installeur avec NSIS ou Inno Setup.

### Build Multi-Plateforme

Automatiser les builds pour Windows, Linux et macOS.

## 🔗 Références

### Code Source

- [`scripts/dev_build/build_dev.py`](../scripts/dev_build/build_dev.py) - Build développement
- [`scripts/dev_build/build_final.py`](../scripts/dev_build/build_final.py) - Build production
- [`scripts/dev_build/build_utils.py`](../scripts/dev_build/build_utils.py) - Utilitaires communs

### Documentation Externe

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Flet Packaging Guide](https://flet.dev/docs/guides/python/packaging-desktop-app)
- [UV Documentation](https://docs.astral.sh/uv/)

## 💡 Astuces

### Déboguer un Build qui Plante

```bash
# 1. Lancer en mode console
uv run python scripts/build_dev.py --console

# 2. Vérifier les logs
cat logs/build_dev.log

# 3. Tester l'exe directement
cd dist/dev
"./Writing Assistant Pro.exe" --debug
```

### Réduire le Temps de Build

```bash
# Éviter --clean sauf si nécessaire
uv run python scripts/build_dev.py

# Le système auto-clean détectera les changements Git
```

### Tester le Build Final Localement

```bash
# Build
uv run python scripts/build_final.py

# Tester
cd dist/production
"./Writing Assistant Pro.exe"
```
