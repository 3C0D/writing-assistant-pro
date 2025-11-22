# Gestion des Icônes - Writing Assistant Pro

## 📁 Structure des Icônes

```
assets/icons/
├── app_icon.png          ← Icône source (PNG haute résolution)
└── icons/
    └── app_icon.ico      ← Icône convertie (ICO pour Windows)
```

## 🎯 Principe de Fonctionnement

### Centralisation

Tous les icônes sont centralisés dans le dossier `assets/icons/` :

- **Fichiers sources** : PNG haute résolution dans `assets/icons/`
- **Fichiers convertis** : ICO dans `assets/icons/icons/`

### Utilisation par PyInstaller

Le script de build (`build_dev.py`, `build_final.py`) utilise directement le fichier PNG :

- PyInstaller supporte nativement les fichiers PNG comme icônes
- Pas de génération automatique de dossiers temporaires
- Pas de copie dans `src/config/icons/` (ancien comportement supprimé)

## 🔄 Conversion PNG → ICO

### Script de Conversion

Le script `scripts/convert_icon.py` permet de convertir automatiquement les PNG en ICO.

**Commande :**

```bash
uv run python scripts/convert_icon.py
```

**Fonctionnement :**

1. 🔍 Scanne tous les fichiers `.png` dans `assets/icons/`
2. ✅ Vérifie si le `.ico` correspondant existe dans `assets/icons/icons/`
3. 🔄 Convertit uniquement les fichiers manquants
4. ⏭️ Ignore les fichiers déjà convertis
5. 📊 Affiche un résumé (convertis, ignorés, échoués)

**Exemple de sortie :**

```
===== Writing Assistant Pro - Icon Converter =====

Source directory: assets/icons
Target directory: assets/icons/icons

Found 1 PNG file(s):
  - app_icon.png

⏭️  Skipping app_icon.png (ICO already exists)

==================================================
Summary:
  ✓ Converted: 0
  ⏭️  Skipped:   1
==================================================
```

### Tâche VS Code

Une tâche VS Code est disponible pour faciliter la conversion :

**Utilisation :**

1. `Ctrl+Shift+P`
2. "Tasks: Run Task"
3. "Convert Icon (PNG to ICO)"

## 📝 Workflow

### Ajouter un Nouvel Icône

1. **Placer le PNG source** dans `assets/icons/`

   ```
   assets/icons/mon_icone.png
   ```

2. **Convertir en ICO** (optionnel, pour Windows)

   ```bash
   uv run python scripts/convert_icon.py
   ```

   Le script créera automatiquement :

   ```
   assets/icons/icons/mon_icone.ico
   ```

3. **Utiliser dans le code**

   ```python
   from src.core.config import get_app_root

   icon_path = get_app_root() / "assets" / "icons" / "mon_icone.png"
   ```

### Modifier un Icône Existant

1. **Modifier le fichier PNG** dans `assets/icons/`
2. **Supprimer le ICO correspondant** dans `assets/icons/icons/`
   ```bash
   rm assets/icons/icons/mon_icone.ico
   ```
3. **Reconvertir**
   ```bash
   uv run python scripts/convert_icon.py
   ```

## 🔧 Configuration Technique

### Taille des Icônes

Le script génère des icônes ICO avec une résolution de **256x256 pixels**.

Pour modifier cette taille, éditer `scripts/convert_icon.py` :

```python
sizes = [(256, 256)]  # Modifier ici
```

### Dépendances

La conversion PNG → ICO nécessite **Pillow** (PIL) :

```bash
uv add pillow
```

## ⚠️ Important

### Ne PAS créer `src/config/icons/`

Ce dossier était utilisé dans l'ancienne version mais a été supprimé.

- ❌ Ne pas créer manuellement ce dossier
- ❌ Ne pas y placer d'icônes
- ✅ Utiliser uniquement `assets/icons/`

### Fichiers .gitignore

Les fichiers ICO générés dans `assets/icons/icons/` peuvent être :

- **Committés** si vous voulez les partager avec l'équipe
- **Ignorés** si vous préférez que chaque développeur les génère localement

Actuellement, ils sont **committés** pour faciliter le développement.

## 📚 Références

- **Script de conversion** : [`scripts/convert_icon.py`](../scripts/convert_icon.py)
- **Fonction de détection** : `ensure_icon_exists()` dans [`scripts/utils.py`](../scripts/utils.py)
- **Tâche VS Code** : [`.vscode/tasks.json`](../.vscode/tasks.json)
