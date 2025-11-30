"""Update notification dialog"""

from __future__ import annotations

import flet as ft

from src.core import _
from src.ui.design_system import AppColors


def show_update_dialog(page: ft.Page, update_info: dict, dark_mode: bool = True) -> None:
    """
    Display dialog when update is available.

    Args:
        page: Flet page instance
        update_info: Update information dictionary from updater
        dark_mode: Whether dark mode is active
    """
    from loguru import logger

    try:

        def close_dialog(e):
            page.close(dialog)

        def open_release(e):
            page.launch_url(update_info["url"])
            close_dialog(e)

        # Truncate release notes for display
        notes = update_info.get("notes", _("No release notes available"))
        if len(notes) > 200:
            notes = notes[:200] + "..."

        version = update_info.get("version", "unknown")

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                _("New version {version} available!").format(version=version),
                color=AppColors.get_text_primary(dark_mode),
            ),
            content=ft.Text(
                notes,
                color=AppColors.get_text_secondary(dark_mode),
            ),
            actions=[
                ft.TextButton(_("Download"), on_click=open_release),
                ft.TextButton(_("Later"), on_click=close_dialog),
            ],
        )

        page.open(dialog)
        logger.info(f"Update dialog shown for version {version}")

    except Exception as e:
        logger.error(f"Failed to show update dialog: {e}", exc_info=True)


def show_no_update_dialog(page: ft.Page, dark_mode: bool = True) -> None:
    """
    Display dialog when no update is available.

    Args:
        page: Flet page instance
        dark_mode: Whether dark mode is active
    """
    from loguru import logger

    try:

        def close_dialog(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                _("Already up to date"),
                color=AppColors.get_text_primary(dark_mode),
            ),
            content=ft.Text(
                _("You are using the latest version."),
                color=AppColors.get_text_secondary(dark_mode),
            ),
            actions=[
                ft.TextButton(_("OK"), on_click=close_dialog),
            ],
        )

        page.open(dialog)
        logger.info("No update dialog shown")

    except Exception as e:
        logger.error(f"Failed to show no update dialog: {e}", exc_info=True)


def show_update_error_dialog(page: ft.Page, error: str, dark_mode: bool = True) -> None:
    """
    Display dialog when update check fails.

    Args:
        page: Flet page instance
        error: Error message
        dark_mode: Whether dark mode is active
    """
    from loguru import logger

    try:

        def close_dialog(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                _("Update check failed"),
                color=AppColors.get_text_primary(dark_mode),
            ),
            content=ft.Text(
                _("Could not check for updates: {error}").format(error=error),
                color=AppColors.get_text_secondary(dark_mode),
            ),
            actions=[
                ft.TextButton(_("OK"), on_click=close_dialog),
            ],
        )

        page.open(dialog)
        logger.info(f"Error dialog shown: {error}")

    except Exception as e:
        logger.error(f"Failed to show error dialog: {e}", exc_info=True)
