"""
Navigation Rail Component

Permanent navigation rail on the left of the interface.
"""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from src.core import _
from src.ui.design_system import AppColors

# Standard width for the navigation rail
RAIL_WIDTH = 50


def create_navigation_rail(
    dark_mode: bool,
    on_menu_click: Callable,
    on_settings_click: Callable,
    show_menu: bool = True,
) -> ft.Container:
    """
    Create a navigation rail

    Args:
        dark_mode: Dark mode enabled or not
        on_menu_click: Callback for menu button
        on_settings_click: Callback for settings button
        show_menu: Whether to show the menu button at the top

    Returns:
        Container representing the navigation rail
    """
    controls = []

    # Menu button at top if visible
    if show_menu:
        controls.append(
            ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color=AppColors.get_icon_color(dark_mode),
                tooltip=_("Toggle Menu"),
                on_click=on_menu_click,
            )
        )

    # Spacer
    controls.append(ft.Container(expand=True))

    # Settings button at bottom
    controls.append(
        ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_color=AppColors.get_icon_color(dark_mode),
            tooltip=_("Settings"),
            on_click=on_settings_click,
            icon_size=20,
        )
    )

    return ft.Container(
        width=RAIL_WIDTH,
        bgcolor=AppColors.get_bg_rail(dark_mode),
        content=ft.Column(
            controls,
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
        ),
    )
