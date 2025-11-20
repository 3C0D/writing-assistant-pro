# Migration NiceGUI → Flet - Plan d'Implémentation

## Contexte

### Problème avec NiceGUI + PyInstaller

L'application utilise actuellement NiceGUI en mode `native=True` pour créer une application desktop. **Problème critique** : NiceGUI + PyInstaller a un bug non résolu qui cause l'erreur :

```
SyntaxError: source code string cannot contain null bytes
```

**Cause** : Lors d'une erreur 404, NiceGUI appelle `runpy.run_path(sys.argv[0])` pour recharger le script, même avec `reload=False`. Sur un exécutable PyInstaller, cela échoue car `sys.argv[0]` pointe vers un binaire.

**Tentatives échouées** :

- `--collect-all nicegui`
- `reload=False` + `NICEGUI_RELOAD="false"`
- Déplacement de `ui.run()` au niveau module
- Monkey-patching de NiceGUI
- `nicegui-pack`

**Conclusion** : Bug non résolu depuis des mois. Migration vers Flet nécessaire.

---

## Solution : Migration vers Flet

### Pourquoi Flet ?

✅ **Packaging PyInstaller parfait** - aucun problème de compatibilité
✅ **Vraie application native** - fenêtre desktop réelle
✅ **Interface moderne** - Material Design 3, animations fluides
✅ **Même fonctionnalités** - hotkeys, hide/show, theming, i18n
✅ **Meilleure performance** - basé sur Flutter
✅ **Communauté active** - documentation excellente

---

## Plan de Migration

### Étape 1 : Préparation Git

```bash
# Créer branche feature
git checkout -b feature/flet-migration

# Vérifier état
git status
```

### Étape 2 : Mise à Jour Dépendances

**Fichier** : `pyproject.toml`

Remplacer dans `[project.dependencies]` :

```toml
# Avant
"nicegui>=2.5.0",

# Après
"flet>=0.24.0",
```

Puis installer :

```bash
uv sync
```

### Étape 3 : Backup Code NiceGUI

```bash
# Renommer main.py
git mv main.py main_nicegui.py.bak

# Renommer src/ui → src/ui_nicegui.bak
git mv src/ui src/ui_nicegui.bak
```

### Étape 4 : Créer Structure Flet

#### 4.1 Nouveau `main.py`

```python
"""
Application entry point for Writing Assistant Pro (Flet version)
"""

import multiprocessing

import flet as ft

from src.core import parse_arguments
from src.ui_flet import WritingAssistantFletApp

multiprocessing.freeze_support()


def main():
    """Main entry point"""
    args = parse_arguments()

    app = WritingAssistantFletApp()

    # Run Flet app
    ft.app(target=app.main)


if __name__ == "__main__":
    main()
```

#### 4.2 Créer `src/ui_flet/__init__.py`

```python
"""
Flet-based UI components for Writing Assistant Pro
"""

from .app_flet import WritingAssistantFletApp

__all__ = ["WritingAssistantFletApp"]
```

#### 4.3 Créer `src/ui_flet/app_flet.py`

```python
"""
Main Flet application for Writing Assistant Pro
"""

import flet as ft

from src.core import (
    ConfigManager,
    HotkeyManager,
    _,
    change_language,
    get_current_language,
)


class WritingAssistantFletApp:
    """Main Flet application class"""

    def __init__(self):
        self.config = ConfigManager()
        self.hotkey_manager = HotkeyManager(self.config)
        self.page = None

    def main(self, page: ft.Page):
        """Main Flet page setup"""
        self.page = page

        # Page configuration
        page.title = (
            "🔥 Writing Assistant Pro (DEV MODE)"
            if self.config.DEBUG
            else "Writing Assistant Pro"
        )
        page.window.width = 800
        page.window.height = 600
        page.theme_mode = (
            ft.ThemeMode.DARK if self.config.DARK_MODE else ft.ThemeMode.LIGHT
        )
        page.padding = 0

        # Hide window on start
        page.window.visible = False

        # Create UI
        self._create_ui()

        # Setup hotkey for toggle
        self.hotkey_manager.register_delayed(self.toggle_window)

        page.update()

    def _create_ui(self):
        """Create the user interface"""
        # AppBar (header)
        self.page.appbar = ft.AppBar(
            title=ft.Text("Writing Assistant Pro"),
            center_title=False,
            bgcolor=ft.colors.BLUE_600,
            actions=[
                ft.IconButton(
                    icon=(
                        ft.icons.DARK_MODE
                        if not self.config.DARK_MODE
                        else ft.icons.LIGHT_MODE
                    ),
                    icon_color=ft.colors.WHITE,
                    tooltip="Toggle Dark/Light Mode",
                    on_click=self.toggle_theme,
                ),
                ft.IconButton(
                    icon=ft.icons.VISIBILITY_OFF,
                    icon_color=ft.colors.WHITE,
                    tooltip=f"Hide ({self.config.HOTKEY_COMBINATION})",
                    on_click=lambda _: self.hide_window(),
                ),
            ],
        )

        # Language selector
        self.language_select = ft.Dropdown(
            label=_("Language"),
            options=[
                ft.dropdown.Option("en", _("English")),
                ft.dropdown.Option("fr", _("Français")),
                ft.dropdown.Option("it", _("Italiano")),
            ],
            value=get_current_language(),
            on_change=self.on_language_change,
            width=150,
        )

        # Main content
        self.label_main = ft.Text(
            _("Hello, this is a real desktop app!"),
            size=18,
        )

        self.button_main = ft.ElevatedButton(
            _("Click me"),
            on_click=self.on_button_click,
        )

        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.language_select]),
                        ft.Column(
                            [self.label_main, self.button_main],
                            spacing=10,
                        ),
                    ],
                    spacing=20,
                ),
                padding=20,
            )
        )

    def on_button_click(self, e):
        """Button click handler"""
        self.page.snack_bar = ft.SnackBar(ft.Text(_("Clicked!!!")))
        self.page.snack_bar.open = True
        self.page.update()

    def on_language_change(self, e):
        """Language change handler"""
        new_lang = e.control.value
        change_language(new_lang)

        # Update all text
        self.label_main.value = _("Hello, this is a real desktop app!")
        self.button_main.text = _("Click me")
        self.language_select.label = _("Language")
        self.language_select.options = [
            ft.dropdown.Option("en", _("English")),
            ft.dropdown.Option("fr", _("Français")),
            ft.dropdown.Option("it", _("Italiano")),
        ]

        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Language changed to {new_lang}")
        )
        self.page.snack_bar.open = True
        self.page.update()

    def toggle_theme(self, e):
        """Toggle dark/light theme"""
        new_dark_mode = not self.config.DARK_MODE
        self.config.DARK_MODE = new_dark_mode

        self.page.theme_mode = (
            ft.ThemeMode.DARK if new_dark_mode else ft.ThemeMode.LIGHT
        )
        e.control.icon = (
            ft.icons.DARK_MODE if not new_dark_mode else ft.icons.LIGHT_MODE
        )

        self.page.update()

    def toggle_window(self):
        """Toggle window visibility"""
        if self.page.window.visible:
            self.hide_window()
        else:
            self.show_window()

    def hide_window(self):
        """Hide the window"""
        if self.page:
            self.page.window.visible = False
            self.page.update()

    def show_window(self):
        """Show the window"""
        if self.page:
            self.page.window.visible = True
            self.page.window.to_front()
            self.page.update()
```

### Étape 5 : Scripts de Build

#### 5.1 Créer `scripts/build_dev_flet.py`

```python
#!/usr/bin/env python3
"""
Writing Assistant Pro - Flet Dev Build Script
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"

from utils import (
    BuildTimer,
    clear_console,
    copy_required_files,
    get_executable_name,
    get_project_root,
    terminate_existing_processes,
)

DEFAULT_SCRIPT_NAME = "main.py"
MODE = "build-dev"


def run_build_dev() -> bool:
    """Run PyInstaller build for dev release"""
    pyinstaller_command = [
        "uv",
        "run",
        "-m",
        "PyInstaller",
        "--console",
        "--name=Writing Assistant Pro",
        "--distpath=dist/dev",
        "--clean",
        "--noconfirm",
        "--collect-all",
        "flet",  # Flet assets
        DEFAULT_SCRIPT_NAME,
    ]

    try:
        print("Starting Flet dev build...")
        subprocess.run(pyinstaller_command, check=True)
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed: {e}")
        return False


def main():
    """Main function"""
    clear_console()
    print("===== Flet Dev Build =====\n")

    timer = BuildTimer()
    timer.start()

    try:
        get_project_root()

        # Clean old build
        if Path("dist/dev").exists():
            shutil.rmtree("dist/dev")

        # Copy required files
        copy_required_files("dev")

        # Terminate existing processes
        terminate_existing_processes(exe_name=get_executable_name())

        # Run build
        if not run_build_dev():
            return 1

        print("\n===== Dev build completed =====")
        timer.print_duration("dev build")

        return 0

    except KeyboardInterrupt:
        print(f"\n{MODE} cancelled by user.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

#### 5.2 Similaire pour `build_final_flet.py`

Copier `build_dev_flet.py` et changer :

- `--console` → `--windowed`
- `dist/dev` → `dist/prod`
- MODE = "build-final"

### Étape 6 : Test

```bash
# Test dev mode
uv run python main.py

# Test build dev
uv run python scripts/build_dev_flet.py

# Test build final
uv run python scripts/build_final_flet.py
```

---

## Validation Finale

### Checklist

- [ ] `uv sync` réussi
- [ ] Mode dev fonctionne (`uv run python main.py`)
- [ ] Fenêtre démarre cachée
- [ ] Hotkey `Ctrl+.` toggle la fenêtre
- [ ] Bouton hide fonctionne
- [ ] Toggle theme fonctionne
- [ ] Changement de langue fonctionne
- [ ] Build dev réussi
- [ ] Build dev exécutable lance et fonctionne
- [ ] Build final réussi
- [ ] Build final exécutable lance et fonctionne

---

## Rollback si Nécessaire

```bash
# Retour à master
git checkout master

# Supprimer branche
git branch -D feature/flet-migration
```
