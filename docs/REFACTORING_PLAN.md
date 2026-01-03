# Plan de Refactorisation - `app.py`

## 📊 État Actuel

- **Fichier**: `src/ui/app.py`
- **Lignes**: 778 lignes (~30 KB)
- **Problème principal**: Fichier monolithique avec trop de responsabilités

---

## 🎯 Objectifs de la Refactorisation

1. **Réduire la taille de `app.py`** à ~200-300 lignes max
2. **Extraire les vues** dans le dossier `src/ui/views/`
3. **Centraliser la logique fichier** qui est dupliquée
4. **Éliminer le code dupliqué** (notamment les boutons top-right)

---

## 📋 Tâches de Refactorisation

### Tâche 1: Créer `src/ui/views/settings_view.py`

**Fichier à créer**: `src/ui/views/settings_view.py`

**Code à extraire de `app.py`** (lignes 486-565 + 650-734):

- `_create_settings_view()` → devient `create_settings_view()`
- `_create_hotkey_display()` → devient `create_hotkey_display()`
- `_on_hotkey_click()` → devient `on_hotkey_click()`
- `_on_hotkey_dialog_result()` → devient `on_hotkey_dialog_result()`

**Structure suggérée**:

```python
"""
Settings View for Writing Assistant Pro
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

from src.core import (
    ConfigManager,
    _,
    change_language,
    get_current_language,
    get_language_manager,
)
from src.core.services.hotkey_capture import format_hotkey_for_display
from src.ui.components import icon_button
from src.ui.design_system import AppColors
from src.ui.dialogs import HotkeyDialogResult, show_hotkey_capture_dialog

if TYPE_CHECKING:
    from src.core import HotkeyManager
    from src.core.managers.window import WindowManager


class SettingsView:
    """Encapsulates the settings view logic."""

    def __init__(
        self,
        config: ConfigManager,
        hotkey_manager: HotkeyManager,
        window_manager: WindowManager | None,
        page: ft.Page,
        on_theme_toggle: Callable[[], None],
        on_ui_refresh: Callable[[], None],
        on_show_snackbar: Callable[[str], None],
    ):
        self.config = config
        self.hotkey_manager = hotkey_manager
        self.window_manager = window_manager
        self.page = page
        self._on_theme_toggle = on_theme_toggle
        self._on_ui_refresh = on_ui_refresh
        self._on_show_snackbar = on_show_snackbar
        self.hotkey_initial_value = ""

    def build(self) -> ft.Container:
        """Build and return the settings view container."""
        # Extraire le code de _create_settings_view() ici
        ...

    def _create_hotkey_display(self) -> ft.Container:
        """Create clickable hotkey display."""
        # Extraire le code ici
        ...

    def _on_hotkey_click(self, e) -> None:
        """Handle hotkey click."""
        # Extraire le code ici
        ...

    def _on_hotkey_dialog_result(self, result: HotkeyDialogResult) -> None:
        """Handle hotkey dialog result."""
        # Extraire le code ici
        ...
```

**Dans `app.py`**, remplacer par:

```python
from src.ui.views import SettingsView

# Dans _create_ui():
if self.state.ui_state.settings_visible:
    settings_view = SettingsView(
        config=self.state.config,
        hotkey_manager=self.hotkey_manager,
        window_manager=self.window_manager,
        page=self.page,
        on_theme_toggle=lambda: self.toggle_theme(None),
        on_ui_refresh=self._create_ui,
        on_show_snackbar=self.show_snack_bar,
    )
    settings_content = settings_view.build()
    # ...
```

**Lignes économisées**: ~130 lignes

---

### Tâche 2: Créer `src/ui/views/about_view.py`

**Fichier à créer**: `src/ui/views/about_view.py`

**Code à extraire de `app.py`** (lignes 567-648):

- `_create_about_view()` → devient fonction `create_about_view()`

**Structure suggérée**:

```python
"""
About View for Writing Assistant Pro
"""

from __future__ import annotations

import flet as ft

from src.core import _
from src.ui.components import icon_button
from src.ui.design_system import AppColors


def create_about_view(
    version: str,
    dark_mode: bool,
    hotkey_combination: str,
    on_theme_toggle,
    on_hide_click,
    on_close_click,
    on_link_click,
) -> ft.Container:
    """
    Create the about view container.

    Args:
        version: Application version string
        dark_mode: Current theme mode
        hotkey_combination: Current hotkey for tooltip
        on_theme_toggle: Callback for theme toggle button
        on_hide_click: Callback for hide button
        on_close_click: Callback for close button
        on_link_click: Callback for link clicks (receives URL)

    Returns:
        Container with the about view content
    """
    # Extraire le code de _create_about_view() ici
    ...
```

**Lignes économisées**: ~80 lignes

---

### Tâche 3: Créer `src/ui/views/main_view.py`

**Fichier à créer**: `src/ui/views/main_view.py`

**Code à extraire de `app.py`** (lignes 371-435):

- `_create_main_content()` → devient `create_main_content()`

**Structure suggérée**:

```python
"""
Main View for Writing Assistant Pro
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import flet as ft

from src.ui.components import icon_button
from src.ui.design_system import AppColors

if TYPE_CHECKING:
    from src.ui.components.input.prompt_bar import PromptBar


def create_main_content(
    prompt_bar: PromptBar,
    dark_mode: bool,
    hotkey_combination: str,
    on_theme_toggle: Callable,
    on_hide_click: Callable,
) -> ft.Container:
    """
    Create the main content area with prompt bar.

    Args:
        prompt_bar: The PromptBar component instance
        dark_mode: Current theme mode
        hotkey_combination: Current hotkey for tooltip
        on_theme_toggle: Callback for theme toggle
        on_hide_click: Callback for hide button

    Returns:
        Container with main content layout
    """
    # Extraire le code de _create_main_content() ici
    ...
```

**Lignes économisées**: ~65 lignes

---

### Tâche 4: Créer `src/ui/components/top_action_bar.py`

**Problème identifié**: Code dupliqué 3 fois (lignes 390-403, 506-519, 569-589)

Les boutons `theme_btn` + `hide_btn` sont créés identiquement dans:

- `_create_main_content()` (lignes 391-403)
- `_create_settings_view()` (lignes 507-519)
- `_create_about_view()` (lignes 570-582)

**Fichier à créer**: `src/ui/components/top_action_bar.py`

```python
"""
Top Action Bar - Common floating buttons for all views
"""

from __future__ import annotations

from typing import Callable

import flet as ft

from src.core import _
from src.ui.components import icon_button


def create_top_action_bar(
    dark_mode: bool,
    hotkey_combination: str,
    on_theme_toggle: Callable,
    on_hide_click: Callable,
    extra_buttons: list[ft.Control] | None = None,
) -> ft.Row:
    """
    Create the top action bar with theme/hide buttons.

    Args:
        dark_mode: Current theme mode
        hotkey_combination: Hotkey for hide tooltip
        on_theme_toggle: Theme toggle callback
        on_hide_click: Hide window callback
        extra_buttons: Additional buttons to add (e.g., close button)

    Returns:
        Row with action buttons aligned to the right
    """
    theme_btn = icon_button(
        icon=(ft.Icons.DARK_MODE if not dark_mode else ft.Icons.LIGHT_MODE),
        tooltip=_("Toggle Dark/Light Mode"),
        dark_mode=dark_mode,
        on_click=on_theme_toggle,
    )

    hide_btn = icon_button(
        icon=ft.Icons.VISIBILITY_OFF,
        tooltip=f"{_('Hide')} ({hotkey_combination})",
        dark_mode=dark_mode,
        on_click=on_hide_click,
    )

    buttons = [ft.Container(expand=True), theme_btn, hide_btn]
    if extra_buttons:
        buttons.extend(extra_buttons)

    return ft.Row(buttons, spacing=5)
```

**Lignes économisées**: ~30 lignes (en enlevant le code dupliqué)

---

### Tâche 5: Extraire la logique FilePicker dans `src/ui/services/file_handler.py`

**Problème identifié**: La logique de traitement de fichiers (lignes 281-351) contient:

- Des constantes `IMAGE_EXT` et `TEXT_EXT` dupliquées (aussi dans `prompt_bar.py`)
- Une logique complexe dans une fonction imbriquée
- Import de `PIL` et `uuid` à l'intérieur de la fonction (mauvaise pratique)

**Fichier à créer**: `src/ui/services/file_handler.py`

```python
"""
File handling utilities for attachments
"""

from __future__ import annotations

import uuid

from loguru import logger
from PIL import Image

from src.core import AttachmentType
from src.ui.components.input.attachment_zone import Attachment


# Constants should be centralized
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"}
TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".html", ".css", ".json",
    ".xml", ".yaml", ".toml", ".c", ".cpp", ".h",
}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | TEXT_EXTENSIONS


def is_supported_file(filename: str) -> bool:
    """Check if file type is supported."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    return f".{ext}" in SUPPORTED_EXTENSIONS


def process_picked_files(files: list) -> list[Attachment]:
    """
    Process files from FilePicker and return attachments.

    Args:
        files: List of FilePickerFile objects

    Returns:
        List of Attachment objects
    """
    attachments = []
    log = logger.bind(name="WritingAssistant.FileHandler")

    for f in files:
        if not f.path:
            continue

        if not is_supported_file(f.name):
            log.warning(f"Skipping unsupported file: {f.name}")
            continue

        ext = f.path.lower().rsplit(".", 1)[-1] if "." in f.path else ""

        try:
            if f".{ext}" in IMAGE_EXTENSIONS:
                img = Image.open(f.path)
                att_type = AttachmentType.IMAGE
                content = img
            elif f".{ext}" in TEXT_EXTENSIONS:
                with open(f.path, encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                att_type = AttachmentType.TEXT
            else:
                att_type = AttachmentType.FILE
                content = f.path

            attachments.append(
                Attachment(
                    id=str(uuid.uuid4()),
                    type=att_type,
                    content=content,
                    name=f.name,
                    size=str(f.size),
                )
            )
        except Exception as ex:
            log.error(f"Error loading file {f.name}: {ex}")

    return attachments
```

**Dans `app.py`**, remplacer `_setup_file_picker` par:

```python
from src.ui.services.file_handler import process_picked_files

def _setup_file_picker(self):
    """Initialize and setup the file picker"""
    def handle_file_result(e: ft.FilePickerResultEvent):
        if e.files and self.prompt_bar:
            new_attachments = process_picked_files(e.files)
            if new_attachments:
                self.prompt_bar.add_attachments(new_attachments)

    self.file_picker = ft.FilePicker(on_result=handle_file_result)
    if self.page:
        self.page.overlay.append(self.file_picker)
        self.page.update()
```

**Lignes économisées dans app.py**: ~60 lignes

---

### Tâche 6: Mettre à jour `src/ui/views/__init__.py`

```python
"""
UI Views package for Writing Assistant Pro
"""

from __future__ import annotations

from src.ui.views.about_view import create_about_view
from src.ui.views.main_view import create_main_content
from src.ui.views.settings_view import SettingsView

__all__ = [
    "create_about_view",
    "create_main_content",
    "SettingsView",
]
```

---

## 🐛 Problèmes de Code / Code Junk Identifié

### 1. Imports à l'intérieur des fonctions (Anti-pattern)

**Fichier**: `app.py` lignes 287-291

```python
def handle_file_result(e: ft.FilePickerResultEvent):
    if e.files and self.prompt_bar:
        import uuid                                    # ❌ Import inside function
        from PIL import Image                          # ❌ Import inside function
        from src.ui.components.input.prompt_bar import PromptBar  # ❌ Inutile
```

**Correction**: Déplacer les imports en haut du fichier ou dans le nouveau module.

---

### 2. Constantes dupliquées

**Fichier 1**: `app.py` lignes 293-309

```python
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"}
TEXT_EXT = {".txt", ".md", ".py", ...}
```

**Fichier 2**: `prompt_bar.py` lignes ~340-358 (similaires)

**Correction**: Centraliser dans `src/ui/services/file_handler.py` ou `src/core/constants.py`

---

### 3. Logique de toggle manquante pour `on_check_updates`

**Fichier**: `app.py` lignes 753-777

Les imports sont faits à l'intérieur de la fonction:

```python
def on_check_updates(self, e):
    from src.core.services.updater import check_for_updates  # ❌
    from src.ui.dialogs import (...)                         # ❌
```

**Correction**: Importer en haut du fichier.

---

## ⚠️ Autres Problèmes Signalés

### 1. Event Bus: Events non émis uniformément

Le `WINDOW_SHOWN` est correctement émis, mais vérifier que:

- Tous les handlers sont bien enregistrés
- Les events sont émis de manière cohérente

**Statut**: Semble OK après review

### 2. `prompt_bar.py` - Fichier très long (523 lignes, ~20KB)

Ce fichier pourrait aussi bénéficier d'une refactorisation future, mais c'est moins
prioritaire que `app.py`. Les méthodes de création d'éléments UI pourraient être
extraites.

### 3. `attachment_zone.py` - Fichier long (418 lignes, ~15KB)

Contient 3 classes: `Attachment`, `AttachmentThumbnail`, `AttachmentPreviewDialog`,
`AttachmentZone`. Pourrait être séparé mais fonctionne bien comme un module cohérent.

---

## 📊 Résumé des Économies

| Tâche        | Lignes économisées |
| ------------ | ------------------ |
| SettingsView | ~130               |
| AboutView    | ~80                |
| MainView     | ~65                |
| TopActionBar | ~30                |
| FileHandler  | ~60                |
| **Total**    | **~365 lignes**    |

**Résultat attendu**: `app.py` passera de **778 lignes** à environ **~410 lignes**

---

## ✅ Checklist d'Exécution

Pour chaque tâche, le LLM devra:

1. [ ] Créer le nouveau fichier avec le code extrait
2. [ ] Ajouter les imports nécessaires dans le nouveau fichier
3. [ ] Modifier `app.py` pour utiliser le nouveau module
4. [ ] Supprimer le code extrait de `app.py`
5. [ ] Mettre à jour `__init__.py` si nécessaire
6. [ ] Exécuter `uv run python scripts/run_ruff.py`
7. [ ] Exécuter `uv run python scripts/run_pyright.py`
8. [ ] Tester manuellement l'application

---

## 📁 Structure Finale

```
src/ui/
├── __init__.py
├── app.py                          # ~410 lignes (réduit de 778)
├── design_system.py
├── components/
│   ├── __init__.py
│   ├── common.py
│   ├── navigation_rail.py
│   ├── sidebar.py
│   ├── top_action_bar.py           # NOUVEAU
│   └── input/
│       ├── attachment_zone.py
│       ├── prompt_bar.py
│       └── source_indicator.py
├── dialogs/
│   ├── __init__.py
│   ├── hotkey_dialog.py
│   └── update_dialog.py
├── views/
│   ├── __init__.py                 # MIS À JOUR
│   ├── about_view.py               # NOUVEAU
│   ├── main_view.py                # NOUVEAU
│   └── settings_view.py            # NOUVEAU
└── services/
    └── file_handler.py             # NOUVEAU
```
