"""
Sidebar Component

Collapsible sidebar with navigation menu.
"""

from __future__ import annotations

import flet as ft

from src.core import _
from src.ui.design_system import AppColors


def create_sidebar(dark_mode: bool) -> ft.Container:
    """
    Create a sidebar

    Args:
        dark_mode: Dark mode enabled or not

    Returns:
        Container representing the sidebar
    """
    return ft.Container(
        width=250,
        bgcolor=AppColors.get_bg_secondary(dark_mode),
        padding=10,
        content=ft.Column(
            [
                ft.Text(
                    _("Menu"),
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.get_text_primary(dark_mode),
                ),
                ft.Divider(),
                # Placeholder for future menu items
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text(_("Home")),
                    on_click=lambda _: None,
                ),
            ],
            spacing=10,
        ),
    )
