"""
Header component for the application
"""

from loguru import logger
from nicegui import ui


def create_header(config, window_manager) -> None:
    """
    Create application header with title and hide button.

    Args:
        config: Application configuration object
        window_manager: WindowManager instance for window control
    """
    log = logger.bind(name="WritingAssistant.ui.header")

    with (
        ui.header()
        .classes("items-center justify-between")
        .style("position: relative; background-color: #1976d2")
    ):
        ui.label("Writing Assistant Pro").classes("text-h6")

        with ui.row().classes("items-center gap-2"):
            # Theme toggle button
            def toggle_theme() -> None:
                new_mode = not config.DARK_MODE
                config.DARK_MODE = new_mode  # This saves to file via ConfigManager

                # Import here to avoid circular imports if any
                from src.core.styles import set_theme

                set_theme(new_mode)

                # Update button icon
                theme_btn.props(f"icon={'dark_mode' if not new_mode else 'light_mode'}")

            theme_btn = (
                ui.button(
                    icon="dark_mode" if not config.DARK_MODE else "light_mode",
                    on_click=toggle_theme,
                )
                .props("flat round dense")
                .tooltip("Toggle Dark/Light Mode")
            )

            ui.button(
                f"Hide ({config.HOTKEY_COMBINATION})",
                on_click=lambda: window_manager.hide_window(),
                icon="visibility_off",
            ).props("flat dense").style("z-index: 1000")

    log.debug("Header created successfully")
