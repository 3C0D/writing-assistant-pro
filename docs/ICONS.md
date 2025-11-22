# Gestion des Icônes - Writing Assistant Pro

## 📁 Structure des Icônes

```
assets/icons/
└── app_icon.png          ← Icône de l'application
```

## 🎯 Format Utilisé

Le projet utilise des fichiers **PNG** pour tous les besoins :

- ✅ **PyInstaller** : Supporte nativement les PNG sur Windows, macOS et Linux
- ✅ **Systray (pystray)** : Charge les PNG via PIL/Pillow sur toutes les plateformes

## 📝 Workflow

### Ajouter un Nouvel Icône

1. **Placer le PNG** dans `assets/icons/`

   ```
   assets/icons/mon_icone.png
   ```

2. **Utiliser dans le code**

   ```python
   from src.core.config import get_app_root

   icon_path = get_app_root() / "assets" / "icons" / "mon_icone.png"
   ```

### Modifier un Icône Existant

1. **Remplacer le fichier PNG** dans `assets/icons/`
2. **Rebuild** si nécessaire pour PyInstaller

## 🔧 Configuration Technique

### Résolution Recommandée

Pour une qualité optimale sur tous les systèmes :

- **Minimum** : 256x256 pixels
- **Recommandé** : 512x512 pixels ou plus
- **Format** : PNG avec transparence (canal alpha)

### Utilisation par PyInstaller

Le script de build utilise directement le PNG :

```python
# Dans build_dev.py et build_final.py
icon_path = ensure_icon_exists()  # Retourne le chemin vers le PNG
pyinstaller_command = [
    # ...
    f"--icon={icon_path}",  # PyInstaller accepte les PNG
    # ...
]
```

### Utilisation par Systray

Le `SystrayManager` charge le PNG via PIL :

```python
# Dans src/core/systray_manager.py
icon_path = app_root / "assets" / "icons" / "app_icon.png"
image = Image.open(icon_path)  # PIL supporte les PNG
```

## 📚 Références

- **Fonction de détection** : `ensure_icon_exists()` dans [`scripts/utils.py`](../scripts/utils.py)
- **Systray Manager** : [`src/core/systray_manager.py`](../src/core/systray_manager.py)
- **Scripts de build** : [`scripts/build_dev.py`](../scripts/build_dev.py) et [`scripts/build_final.py`](../scripts/build_final.py)
