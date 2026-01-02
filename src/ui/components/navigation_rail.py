"""
Navigation Rail Component

Permanent navigation rail on the left of the interface.
"""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from src.ui.design_system import AppColors

# Standard width for the navigation rail
RAIL_WIDTH = 50


def create_navigation_rail(
    dark_mode: bool,
    on_menu_click: Callable,
    on_settings_click: Callable,
) -> ft.Container:
    """
    Create a navigation rail

    Args:
        dark_mode: Dark mode enabled or not
        on_menu_click: Callback for menu button
        on_settings_click: Callback for settings button

    Returns:
        Container representing the navigation rail
    """
    return ft.Container(
        width=RAIL_WIDTH,
        bgcolor=AppColors.get_bg_rail(dark_mode),
        content=ft.Column(
            [
                # Menu button at top
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=AppColors.get_icon_color(dark_mode),
                    tooltip="Toggle Menu",
                    on_click=on_menu_click,
                ),
                # Spacer
                ft.Container(expand=True),
                # Settings button at bottom
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_color=AppColors.get_icon_color(dark_mode),
                    tooltip="Settings",
                    on_click=on_settings_click,
                    icon_size=20,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
        ),
    )
