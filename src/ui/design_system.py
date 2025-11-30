"""
Centralized Design System for Writing Assistant Pro

This module contains all design tokens (colors, spacing, typography)
used in the application.
"""

from __future__ import annotations

import flet as ft


class AppColors:
    """Application color palette"""

    # Dark Mode - Backgrounds
    DARK_BG_PRIMARY = "#2b2b2b"
    DARK_BG_SECONDARY = "#2e2e2e"
    DARK_BG_RAIL = "#3a3a3a"
    DARK_BG_SURFACE = "#353535"

    # Dark Mode - Text & Icons
    DARK_TEXT_PRIMARY = "#b0b0b0"
    DARK_TEXT_SECONDARY = "#808080"
    DARK_ICON_COLOR = "#b0b0b0"

    # Light Mode - Backgrounds
    LIGHT_BG_PRIMARY = "#fafafa"
    LIGHT_BG_SECONDARY = "#f5f5f5"
    LIGHT_BG_RAIL = "#e0e0e0"
    LIGHT_BG_SURFACE = "#ffffff"

    # Light Mode - Text & Icons
    LIGHT_TEXT_PRIMARY = "#404040"
    LIGHT_TEXT_SECONDARY = "#707070"
    LIGHT_ICON_COLOR = "#505050"

    @staticmethod
    def get_bg_primary(dark_mode: bool) -> str:
        """Get primary background color based on mode"""
        return AppColors.DARK_BG_PRIMARY if dark_mode else AppColors.LIGHT_BG_PRIMARY

    @staticmethod
    def get_bg_secondary(dark_mode: bool) -> str:
        """Get secondary background color based on mode"""
        return AppColors.DARK_BG_SECONDARY if dark_mode else AppColors.LIGHT_BG_SECONDARY

    @staticmethod
    def get_bg_rail(dark_mode: bool) -> str:
        """Get navigation rail background color"""
        return AppColors.DARK_BG_RAIL if dark_mode else AppColors.LIGHT_BG_RAIL

    @staticmethod
    def get_bg_surface(dark_mode: bool) -> str:
        """Get surface background color for elevated elements"""
        return AppColors.DARK_BG_SURFACE if dark_mode else AppColors.LIGHT_BG_SURFACE

    @staticmethod
    def get_text_primary(dark_mode: bool) -> str:
        """Get primary text color based on mode"""
        return AppColors.DARK_TEXT_PRIMARY if dark_mode else AppColors.LIGHT_TEXT_PRIMARY

    @staticmethod
    def get_text_secondary(dark_mode: bool) -> str:
        """Get secondary text color based on mode"""
        return AppColors.DARK_TEXT_SECONDARY if dark_mode else AppColors.LIGHT_TEXT_SECONDARY

    @staticmethod
    def get_icon_color(dark_mode: bool) -> str:
        """Get icon color based on mode"""
        return AppColors.DARK_ICON_COLOR if dark_mode else AppColors.LIGHT_ICON_COLOR


class AppSpacing:
    """Standardized spacing values"""

    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32


class AppTypography:
    """Reusable typography styles"""

    HEADING_LARGE = ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)
    HEADING_MEDIUM = ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
    BODY = ft.TextStyle(size=16)
    BODY_SMALL = ft.TextStyle(size=14)
