from __future__ import annotations

from collections.abc import Callable

import flet as ft

from src.ui.design_system import AppColors


class SourceIndicator(ft.Container):
    """
    Toggle button indicating availability of an input source (Clipboard/Selection).

    Features:
    - Visual on/off state with color change
    - Preview text display (truncated)
    - Callback for activation (for mutual exclusivity)
    - Method to deactivate programmatically without triggering toggle
    """

    def __init__(
        self,
        icon: str,
        label: str,
        source_id: str,
        is_active: bool = False,
        visible: bool = False,
        on_toggle: Callable[[str, bool], None] | None = None,
        preview_text: str | None = None,
    ):
        """
        Initialize a SourceIndicator button.

        Args:
            icon: Icon name to display
            label: Label text (e.g., "Clipboard", "Selection")
            source_id: Unique identifier for this source (e.g., "clipboard", "selection")
            is_active: Initial active state
            visible: Initial visibility
            on_toggle: Callback when toggled, receives (source_id, is_active)
            preview_text: Optional preview text to display
        """
        super().__init__()
        self.icon_name = icon
        self.label_text = label
        self.source_id = source_id
        self._is_active = is_active
        self.on_toggle = on_toggle
        self._preview_text = preview_text

        # Styling
        self.visible = visible
        self.border_radius = 8
        self.padding = ft.padding.symmetric(horizontal=12, vertical=6)
        self.on_click = self._handle_click
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_OUT)

        # Build UI
        self.icon_control: ft.Icon | None = None
        self.text_control: ft.Text | None = None
        self.content = self._build_content()
        self._update_style()

    def _build_content(self) -> ft.Row:
        self.icon_control = ft.Icon(
            name=self.icon_name,
            size=16,
        )
        self.text_control = ft.Text(
            value=self._get_display_text(),
            size=12,
            weight=ft.FontWeight.W_500,
            no_wrap=True,
        )

        return ft.Row(
            controls=[self.icon_control, self.text_control],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _get_display_text(self) -> str:
        text = self.label_text
        if self._preview_text:
            # Truncate to ~30 chars
            preview = self._preview_text.replace("\n", " ").strip()
            if len(preview) > 30:
                preview = preview[:27] + "..."
            text += f": {preview}"
        return text

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Handle click - toggle state and notify parent."""
        self._is_active = not self._is_active
        self._update_style()
        self.update()

        if self.on_toggle:
            self.on_toggle(self.source_id, self._is_active)

    def _update_style(self) -> None:
        """Update visual style based on active state."""
        if self._is_active:
            self.bgcolor = ft.Colors.with_opacity(0.15, AppColors.ACCENT)
            self.border = ft.border.all(1.5, AppColors.ACCENT)
            if self.icon_control:
                self.icon_control.color = AppColors.ACCENT
            if self.text_control:
                self.text_control.color = AppColors.ACCENT
        else:
            self.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
            self.border = ft.border.all(1, ft.Colors.GREY_700)
            if self.icon_control:
                self.icon_control.color = ft.Colors.GREY_500
            if self.text_control:
                self.text_control.color = ft.Colors.GREY_500

    # =========================================================================
    # Public API
    # =========================================================================

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """Set active state and update style (does NOT trigger callback)."""
        self._is_active = value
        self._update_style()

    @property
    def preview_text(self) -> str | None:
        return self._preview_text

    @preview_text.setter
    def preview_text(self, value: str | None) -> None:
        """Update preview text and refresh display."""
        self._preview_text = value
        if self.text_control:
            self.text_control.value = self._get_display_text()

    def activate(self) -> None:
        """Activate this indicator (triggers visual update but NOT callback)."""
        self._is_active = True
        self._update_style()

    def deactivate(self) -> None:
        """Deactivate this indicator (triggers visual update but NOT callback)."""
        self._is_active = False
        self._update_style()
