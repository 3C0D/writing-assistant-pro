"""
Main View for Writing Assistant Pro
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import flet as ft

from src.ui.components.top_action_bar import create_top_action_bar
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
    # Floating buttons at top right
    action_bar = create_top_action_bar(
        dark_mode=dark_mode,
        hotkey_combination=hotkey_combination,
        on_theme_toggle=on_theme_toggle,
        on_hide_click=on_hide_click,
    )

    # Main container
    return ft.Container(
        content=ft.Column(
            [
                # Buttons row at top right
                action_bar,
                # Spacer to push prompt to center (vertically)
                ft.Container(expand=True),
                # Prompt Bar Area
                ft.Container(
                    content=prompt_bar,
                    width=700,  # Constrain width for aesthetic centering
                ),
                # Bottom spacer (smaller than top one usually, or equal for true center)
                ft.Container(expand=True),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        expand=True,
        bgcolor=AppColors.get_bg_primary(dark_mode),
    )
