"""
Reusable common UI components

Factory functions to create components with consistent styling.
"""

from __future__ import annotations

import flet as ft

from src.ui.design_system import AppColors, AppSpacing


def styled_container(
    content: ft.Control,
    dark_mode: bool,
    elevation: int = 2,
    padding: int = AppSpacing.MD,
) -> ft.Container:
    """
    Container with uniform styling

    Args:
        content: Container content
        dark_mode: Dark mode enabled or not
        elevation: Elevation level (shadow)
        padding: Internal spacing

    Returns:
        Styled container
    """
    return ft.Container(
        content=content,
        padding=ft.padding.all(padding),
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=elevation * 2,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        bgcolor=AppColors.get_bg_surface(dark_mode),
    )


def icon_button(
    icon: str,
    tooltip: str,
    dark_mode: bool,
    on_click,
    icon_size: int = 20,
) -> ft.IconButton:
    """
    Icon button with consistent styling

    Args:
        icon: Icon to display (ft.Icons constant)
        tooltip: Tooltip text on hover
        dark_mode: Dark mode enabled or not
        on_click: Click callback
        icon_size: Icon size

    Returns:
        Styled IconButton
    """
    return ft.IconButton(
        icon=icon,
        icon_color=AppColors.get_icon_color(dark_mode),
        tooltip=tooltip,
        on_click=on_click,
        icon_size=icon_size,
    )


def section_header(
    text: str,
    dark_mode: bool,
    size: int = 20,
) -> ft.Text:
    """
    Section header with uniform styling

    Args:
        text: Header text
        dark_mode: Dark mode enabled or not
        size: Text size

    Returns:
        Styled Text for header
    """
    return ft.Text(
        text,
        size=size,
        weight=ft.FontWeight.BOLD,
        color=AppColors.get_text_primary(dark_mode),
    )
