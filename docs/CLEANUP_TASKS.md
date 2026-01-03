# Tâches de Nettoyage Post-Refactorisation

## 📊 Résumé de la Refactorisation Effectuée

| Métrique        | Avant | Après | Changement    |
| --------------- | ----- | ----- | ------------- |
| Lignes `app.py` | 778   | 548   | -230 lignes   |
| Pyright         | ✅    | ✅    | Aucune erreur |
| Ruff            | ✅    | ✅    | Aucune erreur |

### Nouveaux Fichiers Créés

- `src/ui/views/settings_view.py` (218 lignes)
- `src/ui/views/about_view.py` (105 lignes)
- `src/ui/views/main_view.py` (71 lignes)
- `src/ui/components/top_action_bar.py` (54 lignes)
- `src/ui/services/file_handler.py` (91 lignes)
- `src/ui/views/__init__.py` (mis à jour)

---

## ⚠️ Problèmes Détectés à Corriger

### Problème 1: CODE MORT dans `app.py` (CRITIQUE)

**Fichier**: `src/ui/app.py`

**Lignes**: 420-504 (85 lignes)

Les méthodes suivantes sont maintenant dupliquées dans `SettingsView` mais n'ont
**PAS été supprimées** de `app.py`:

- `_create_hotkey_display()` (lignes 420-452)
- `_on_hotkey_click()` (lignes 454-465)
- `_on_hotkey_dialog_result()` (lignes 467-504)

**Action**: Supprimer ces 3 méthodes de `app.py` car elles existent maintenant dans
`src/ui/views/settings_view.py`.

**Code à supprimer**:

```python
# Supprimer lignes 420-504 de app.py (ces méthodes)
def _create_hotkey_display(self) -> ft.Container:
    ...

def _on_hotkey_click(self, e) -> None:
    ...

def _on_hotkey_dialog_result(self, result: HotkeyDialogResult) -> None:
    ...
```

**Après suppression**: `app.py` passera de 548 à ~463 lignes.

---

### Problème 2: Imports inutilisés potentiels dans `app.py`

**Fichier**: `src/ui/app.py`

Après la suppression du code mort, vérifier si ces imports sont encore nécessaires :

```python
from src.core.services.hotkey_capture import format_hotkey_for_display  # Possiblement inutile
from src.ui.dialogs import HotkeyDialogResult, show_hotkey_capture_dialog  # Possiblement inutile
```

**Action**: Après suppression du code mort, exécuter `uv run python scripts/run_ruff.py`
qui détectera et supprimera automatiquement les imports inutilisés.

---

### Problème 3: Import local dans `on_check_updates()` (Mineur)

**Fichier**: `src/ui/app.py` lignes 528-533

```python
def on_check_updates(self, e):
    from src.core.services.updater import check_for_updates  # ❌ Import local
    from src.ui.dialogs import (...)                         # ❌ Import local
```

**Action**: Déplacer ces imports en haut du fichier pour suivre les conventions PEP 8.

---

### Problème 4: Attribut `on_language_change` dans `app.py` potentiellement inutilisé

**Fichier**: `src/ui/app.py` lignes 341-352

La méthode `on_language_change` est maintenant dans `SettingsView`, mais elle
semble aussi exister dans `app.py`. Vérifier si elle est encore utilisée.

**Action**: Vérifier l'utilisation et supprimer si obsolète.

---

## ✅ Checklist d'Exécution

1. [ ] Supprimer les méthodes dupliquées (Problème 1)
2. [ ] Exécuter `uv run python scripts/run_ruff.py` (nettoyage automatique des imports)
3. [ ] Exécuter `uv run python scripts/run_pyright.py`
4. [ ] Tester l'application: `uv run python main.py --debug`
5. [ ] Vérifier que les Settings fonctionnent (changement de langue, hotkey)
6. [ ] Vérifier le compte de lignes: `(Get-Content src/ui/app.py | Measure-Object -Line).Lines`
7. [ ] Commit les changements

---

## 📏 Objectif Final

| Fichier  | Cible           | Notes                          |
| -------- | --------------- | ------------------------------ |
| `app.py` | ~400-450 lignes | Après suppression du code mort |

---

## 🗂️ Code Exact à Supprimer

### Dans `src/ui/app.py`, supprimer les lignes 420-504 :

```python
    def _create_hotkey_display(self) -> ft.Container:
        """Create clickable hotkey display that opens capture dialog."""
        current_hotkey = self.state.config.HOTKEY_COMBINATION
        display_text = format_hotkey_for_display(current_hotkey)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        _("Shortcut Key"),
                        size=12,
                        color=AppColors.get_text_secondary(self.state.config.DARK_MODE),
                    ),
                    ft.Container(
                        content=ft.Text(
                            display_text,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.get_text_primary(self.state.config.DARK_MODE),
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                        border_radius=8,
                        bgcolor=AppColors.get_bg_secondary(self.state.config.DARK_MODE),
                        border=ft.border.all(
                            1, AppColors.get_text_secondary(self.state.config.DARK_MODE)
                        ),
                    ),
                ],
                spacing=5,
            ),
            on_click=self._on_hotkey_click,
            width=300,
        )

    def _on_hotkey_click(self, e) -> None:
        """Handle click on hotkey display to open capture dialog."""
        if not self.page:
            return

        show_hotkey_capture_dialog(
            page=self.page,
            current_hotkey=self.state.config.HOTKEY_COMBINATION,
            dark_mode=self.state.config.DARK_MODE,
            on_result=self._on_hotkey_dialog_result,
            hotkey_manager=self.hotkey_manager,
        )

    def _on_hotkey_dialog_result(self, result: HotkeyDialogResult) -> None:
        """Handle result from hotkey capture dialog."""
        if result.action == "cancel":
            # Re-register the original hotkey (was unregistered when dialog opened)
            if self.state.config.HOTKEY_COMBINATION and self.window_manager:
                self.log.info("Cancel: re-registering original hotkey")
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        if result.action == "save":
            new_hotkey = result.hotkey
        else:
            # Unknown action, just re-register original
            if self.state.config.HOTKEY_COMBINATION and self.window_manager:
                self.hotkey_manager.register_delayed(self.window_manager.toggle_window)
            return

        # Update config
        old_hotkey = self.state.config.HOTKEY_COMBINATION
        self.state.config.HOTKEY_COMBINATION = new_hotkey or ""

        # Re-register the hotkey (or unregister if None)
        if new_hotkey:
            self.log.info(f"Hotkey changed: {old_hotkey} -> {new_hotkey}")
            if self.window_manager:
                self.hotkey_manager.reregister(self.window_manager.toggle_window)
        else:
            self.log.info(f"Hotkey disabled (was: {old_hotkey})")
            # Already unregistered when dialog opened, no need to unregister again

        # Refresh UI to show new hotkey
        self._create_ui()

        # Show confirmation
        if self.page:
            display = format_hotkey_for_display(new_hotkey) if new_hotkey else _("None")
            self.show_snack_bar(_("Hotkey: {display}").format(display=display))
            self.page.update()
```

### Aussi supprimer/vérifier la méthode `on_language_change` (lignes 341-352) si inutilisée
