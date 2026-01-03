"""
About View for Writing Assistant Pro
"""

from __future__ import annotations

from collections.abc import Callable

import flet as ft

from src.core import _
from src.ui.components import icon_button
from src.ui.components.top_action_bar import create_top_action_bar
from src.ui.design_system import AppColors


def create_about_view(
    version: str,
    dark_mode: bool,
    hotkey_combination: str,
    on_theme_toggle: Callable,
    on_hide_click: Callable,
    on_close_click: Callable,
    on_link_click: Callable,
) -> ft.Container:
    """
    Create the about view container.

    Args:
        version: Application version string
        dark_mode: Current theme mode
        hotkey_combination: Current hotkey for tooltip
        on_theme_toggle: Callback for theme toggle button
        on_hide_click: Callback for hide button
        on_close_click: Callback for close button
        on_link_click: Callback for link clicks (receives URL)

    Returns:
        Container with the about view content
    """
    # Floating buttons at top right with close button
    close_btn = icon_button(
        icon=ft.Icons.CLOSE,
        tooltip=_("Close"),
        dark_mode=dark_mode,
        on_click=on_close_click,
    )
    extra_buttons = [ft.Container(content=close_btn)]

    action_bar = create_top_action_bar(
        dark_mode=dark_mode,
        hotkey_combination=hotkey_combination,
        on_theme_toggle=on_theme_toggle,
        on_hide_click=on_hide_click,
        extra_buttons=extra_buttons,
    )

    about_text = _(
        "Free & lightweight AI writing assistant, similar to Apple's Apple Intelligence. "
        "Works with many AI models, online and local."
    )
    contrib_text = _(
        "Any help and contributions are welcome! This is an open source project and "
        "we appreciate any feedback or code contributions."
    )

    markdown_content = f"""
# Writing Assistant Pro

{_("Inspired by **Writing Tool APP** by author **3C0D**.")}

{about_text}

---

### ⭐ {_("Contributions")}

{contrib_text}

[Check out the project on GitHub](https://github.com/dd200/writing-assistant-pro)

---

**Version:** {version}
"""

    return ft.Container(
        content=ft.Column(
            [
                action_bar,
                ft.Markdown(
                    markdown_content,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: on_link_click(e.data) if e.data else None,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
        bgcolor=AppColors.get_bg_primary(dark_mode),
    )
