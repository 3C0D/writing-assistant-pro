"""
Top Action Bar - Common floating buttons for all views
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import flet as ft

from src.core import _
from src.ui.components import icon_button


def create_top_action_bar(
    dark_mode: bool,
    hotkey_combination: str,
    on_theme_toggle: Callable,
    on_hide_click: Callable,
    extra_buttons: Sequence[ft.Control] | None = None,
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
