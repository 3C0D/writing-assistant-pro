from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import flet as ft

from src.core import (
    AttachmentID,
    EventType,
    get_event_bus,
)
from src.core.services.input_source import InputSourceService, InputState
from src.ui.components.input.attachment_zone import Attachment, AttachmentZone
from src.ui.components.input.source_indicator import SourceIndicator
from src.ui.design_system import AppColors

if TYPE_CHECKING:
    pass


class PromptBar(ft.Container):
    """
    Main input area containing the prompt text field, source indicators,
    and attachment management.

    Logic:
    - Selection has priority over Clipboard (if both exist, Selection is ON)
    - Only one source can be active at a time (mutual exclusivity)
    - Removing an attachment deactivates its source button
    - Source buttons only appear if content exists
    """

    # Use enums instead of magic strings
    ID_SELECTION_TEXT = AttachmentID.SELECTION_TEXT.value
    ID_CLIPBOARD_TEXT = AttachmentID.CLIPBOARD_TEXT.value
    ID_CLIPBOARD_IMAGE = AttachmentID.CLIPBOARD_IMAGE.value

    def __init__(
        self,
        input_service: InputSourceService,
        on_submit: Callable[[str, list[Attachment], dict], None],
        on_attach_click: Callable[[], None],
        on_height_change: Callable[[float], None] | None = None,
    ):
        super().__init__()
        self.input_service = input_service
        self.on_submit = on_submit
        self.on_attach_click = on_attach_click
        self.on_height_change = on_height_change
        self._page: ft.Page | None = None

        # State
        self.attachments: list[Attachment] = []
        self.input_state: InputState | None = None

        # UI Components
        self.text_field = self._create_text_field()
        self.submit_button = self._create_submit_button()
        self.selection_btn = self._create_selection_button()
        self.clipboard_btn = self._create_clipboard_button()
        self.attachment_zone = AttachmentZone(
            attachments=[],
            on_remove_attachment=self._handle_remove_attachment,
            on_add_click=self._handle_add_file_click,
        )

        # Structure
        self.content = self._build_layout()

        # Styling
        self.bgcolor = ft.Colors.TRANSPARENT
        self.padding = 10
        self.border_radius = 12

        # Initialize
        self._is_mounted = False
        self.did_mount = self._on_mount
        self.will_unmount = self._on_unmount

    def _on_unmount(self) -> None:
        """Handle unmount - reset mounting state."""
        self._is_mounted = False

    def _on_mount(self) -> None:
        """Initialize on mount - just set up page reference, don't detect sources yet."""
        if self.page:
            self._page = self.page
            self.attachment_zone.set_page(self.page)
            self._is_mounted = True

        # Listen to PRE_SHOW event (BEFORE window takes focus) for selection capture
        get_event_bus().on(EventType.WINDOW_PRE_SHOW, self._on_window_pre_show)

    def _on_window_pre_show(self, data: dict | None = None) -> None:
        """Handle window pre-show event - capture selection BEFORE window gets focus."""
        # Guard: only refresh if mounted to page
        if not self._is_mounted or not self._page:
            return
        self.refresh()

    # =========================================================================
    # Source Detection & UI Update
    # =========================================================================

    def _refresh_sources(self) -> None:
        """Detect available inputs and update UI with priority logic."""
        self.input_state = self.input_service.detect_sources()

        has_selection = self.input_state.has_selection
        has_clipboard = self.input_state.has_clipboard_content

        # Update button visibility
        self.selection_btn.visible = has_selection
        self.clipboard_btn.visible = has_clipboard

        # Update preview text
        self.selection_btn.preview_text = self.input_state.selection_text
        if self.input_state.clipboard_text:
            self.clipboard_btn.preview_text = self.input_state.clipboard_text
        elif self.input_state.clipboard_image:
            self.clipboard_btn.preview_text = "Image"
        else:
            self.clipboard_btn.preview_text = None

        # Priority logic: Selection > Clipboard
        if has_selection:
            # Selection takes priority - activate it
            self.selection_btn.activate()
            self.clipboard_btn.deactivate()
            self._add_selection_attachment()
        elif has_clipboard:
            # No selection, activate clipboard
            self.clipboard_btn.activate()
            self.selection_btn.deactivate()
            self._add_clipboard_attachment()
        else:
            # No sources
            self.selection_btn.deactivate()
            self.clipboard_btn.deactivate()

        self._update_attachment_zone()
        self.update()

    # =========================================================================
    # Source Toggle Handlers
    # =========================================================================

    def _handle_source_toggle(self, source_id: str, is_active: bool) -> None:
        """Handle toggle of any source button with mutual exclusivity."""
        if is_active:
            # Activating a source - deactivate the other
            if source_id == "selection":
                self.clipboard_btn.deactivate()
                self.clipboard_btn.update()  # Force UI update
                self._remove_clipboard_attachments()
                self._add_selection_attachment()
            elif source_id == "clipboard":
                self.selection_btn.deactivate()
                self.selection_btn.update()  # Force UI update
                self._remove_selection_attachment()
                self._add_clipboard_attachment()
        else:
            # Deactivating - remove corresponding attachment
            if source_id == "selection":
                self._remove_selection_attachment()
            elif source_id == "clipboard":
                self._remove_clipboard_attachments()

        self._update_attachment_zone()
        self.update()  # Force PromptBar UI update

    # =========================================================================
    # Attachment Management
    # =========================================================================

    def _add_selection_attachment(self) -> None:
        """Add selection text as attachment."""
        if not self.input_state or not self.input_state.selection_text:
            return

        # Remove existing selection attachment first
        self._remove_selection_attachment()

        att = Attachment(
            id=self.ID_SELECTION_TEXT,
            type="text",
            content=self.input_state.selection_text,
            name="Sélection",
            source="selection",
        )
        self.attachments.append(att)

    def _remove_selection_attachment(self) -> None:
        """Remove selection text attachment."""
        self.attachments = [a for a in self.attachments if a.id != self.ID_SELECTION_TEXT]

    def _add_clipboard_attachment(self) -> None:
        """Add clipboard content as attachment (text or image)."""
        if not self.input_state:
            return

        # Remove existing clipboard attachments first
        self._remove_clipboard_attachments()

        # Add text attachment if exists
        if self.input_state.clipboard_text:
            att = Attachment(
                id=self.ID_CLIPBOARD_TEXT,
                type="text",
                content=self.input_state.clipboard_text,
                name="Clipboard",
                source="clipboard",
            )
            self.attachments.append(att)

        # Add image attachment if exists
        if self.input_state.clipboard_image:
            att = Attachment(
                id=self.ID_CLIPBOARD_IMAGE,
                type="image",
                content=self.input_state.clipboard_image,
                name="Clipboard Image",
                source="clipboard",
            )
            self.attachments.append(att)

    def _remove_clipboard_attachments(self) -> None:
        """Remove all clipboard-based attachments."""
        self.attachments = [
            a
            for a in self.attachments
            if a.id not in (self.ID_CLIPBOARD_TEXT, self.ID_CLIPBOARD_IMAGE)
        ]

    def _reorder_attachments(self) -> None:
        """Ensure selection/clipboard are always first, followed by fixed order files."""
        # Source-based attachments (Selection and Clipboard)
        sources = [a for a in self.attachments if a.source in ("selection", "clipboard")]

        # Other attachments (Files) - maintain their original relative order
        other = [
            a
            for a in self.attachments
            if not a.source or a.source not in ("selection", "clipboard")
        ]

        self.attachments = sources + other

    def _handle_remove_attachment(self, att_id: str) -> None:
        """Handle removal of an attachment - also deactivates source if applicable."""
        # Find the attachment to get its source
        removed_att = next((a for a in self.attachments if a.id == att_id), None)

        # Remove the attachment
        self.attachments = [a for a in self.attachments if a.id != att_id]
        self._update_attachment_zone()

        # Deactivate source button if this was a source-based attachment
        if removed_att and removed_att.source:
            if removed_att.source == "selection":
                self.selection_btn.deactivate()
                self.selection_btn.update()
            elif removed_att.source == "clipboard":
                # Check if any clipboard attachments remain
                remaining_clipboard = [
                    a
                    for a in self.attachments
                    if a.id in (self.ID_CLIPBOARD_TEXT, self.ID_CLIPBOARD_IMAGE)
                ]
                if not remaining_clipboard:
                    self.clipboard_btn.deactivate()
                    self.clipboard_btn.update()

    def _handle_add_file_click(self) -> None:
        """Trigger file picker via callback."""
        if self.on_attach_click:
            self.on_attach_click()

    # Unsupported file extensions (binary/archive files)
    UNSUPPORTED_EXTENSIONS = {
        "exe",
        "dll",
        "so",
        "bin",
        "dat",
        "iso",
        "msi",
        "zip",
        "rar",
        "7z",
        "tar",
        "gz",
        "bz2",
        "dmg",
        "pkg",
        "deb",
        "rpm",
    }

    @classmethod
    def is_file_supported(cls, file_path: str) -> bool:
        """Check if file type is supported for attachment."""
        ext = file_path.split(".")[-1].lower() if "." in file_path else ""
        return ext not in cls.UNSUPPORTED_EXTENSIONS

    def add_attachments(self, new_attachments: list[Attachment]) -> None:
        """External method to add attachments (e.g., from FilePicker)."""
        # Filter out unsupported file types
        valid_attachments = [
            att
            for att in new_attachments
            if att.type != "file" or self.is_file_supported(str(att.content))
        ]
        self.attachments.extend(valid_attachments)
        self._update_attachment_zone()

    def _update_attachment_zone(self) -> None:
        """Update the attachment zone display."""
        self._reorder_attachments()
        self.attachment_zone.attachments = self.attachments
        self.attachment_zone.refresh()

    # =========================================================================
    # UI Creation
    # =========================================================================

    def _create_text_field(self) -> ft.TextField:
        return ft.TextField(
            multiline=True,
            min_lines=1,
            max_lines=5,
            hint_text="Comment puis-je vous aider ?",
            border=ft.InputBorder.NONE,
            text_size=16,
            content_padding=15,
            expand=True,
            on_submit=self._handle_submit_action,
            shift_enter=True,
        )

    def _create_submit_button(self) -> ft.IconButton:
        return ft.IconButton(
            icon=ft.Icons.ARROW_UPWARD_ROUNDED,
            icon_color=ft.Colors.WHITE,
            bgcolor=AppColors.PRIMARY,
            on_click=self._handle_submit_action,
            tooltip="Envoyer",
        )

    def _create_selection_button(self) -> SourceIndicator:
        return SourceIndicator(
            icon=ft.Icons.TEXT_FIELDS,
            label="Sélection",
            source_id="selection",
            visible=False,
            on_toggle=self._handle_source_toggle,
        )

    def _create_clipboard_button(self) -> SourceIndicator:
        return SourceIndicator(
            icon=ft.Icons.PASTE,
            label="Clipboard",
            source_id="clipboard",
            visible=False,
            on_toggle=self._handle_source_toggle,
        )

    def _handle_submit_action(self, e: ft.ControlEvent) -> None:
        """Handle submit - gather all input sources and send."""
        text = (self.text_field.value or "").strip()
        if not text and not self.attachments:
            return

        # Gather source data for prompt construction
        source_data: dict[str, str | None] = {}

        if self.selection_btn.is_active and self.input_state:
            source_data["selection_text"] = self.input_state.selection_text

        if self.clipboard_btn.is_active and self.input_state:
            source_data["clipboard_text"] = self.input_state.clipboard_text
            # Note: clipboard_image is in attachments

        self.on_submit(text, self.attachments, source_data)

        # Clear after submit
        self.text_field.value = ""
        self.text_field.update()
        self.attachments = []
        self._update_attachment_zone()

    def _build_layout(self) -> ft.Column:
        """Build the main layout."""
        # Input container with text field and buttons
        input_container = ft.Container(
            content=ft.Row(
                controls=[
                    # Add file button
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                        icon_color=ft.Colors.GREY_500,
                        tooltip="Ajouter des fichiers",
                        on_click=lambda _: self._handle_add_file_click(),
                    ),
                    self.text_field,
                    ft.Container(self.submit_button, padding=5),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        )

        return ft.Column(
            controls=[
                # Row 1: Source Indicators (Selection first, then Clipboard)
                ft.Row(
                    controls=[self.selection_btn, self.clipboard_btn],
                    spacing=10,
                ),
                # Row 2: Input Area
                input_container,
                # Row 3: Attachments
                self.attachment_zone,
            ],
            spacing=8,
        )

    # =========================================================================
    # Public API
    # =========================================================================

    def refresh(self) -> None:
        """Refresh input sources detection."""
        self._refresh_sources()
