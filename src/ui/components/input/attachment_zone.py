from __future__ import annotations

import base64
import io
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import flet as ft
from PIL.Image import Image as PILImage

from src.ui.design_system import AppColors


@dataclass
class Attachment:
    """Represents an attached item (file, image, or text from source)."""

    id: str  # Unique ID (e.g., "clipboard_image", "selection_text", "file_xxx")
    type: str  # 'image', 'file', or 'text'
    content: Any  # File path (str), PIL Image, or text content (str)
    name: str
    source: str | None = None  # Optional: 'clipboard', 'selection', or None for files
    size: str | None = None


def pil_image_to_base64(image: PILImage, max_size: int = 200) -> str:
    """Convert PIL Image to base64 string for Flet display."""
    # Resize for thumbnail if needed
    image.thumbnail((max_size, max_size))

    # Convert to RGB if necessary (e.g., RGBA images)
    if image.mode in ("RGBA", "P"):
        background = PILImage.new("RGB", image.size, (255, 255, 255))  # type: ignore
        if image.mode == "P":
            image = image.convert("RGBA")
        background.paste(image, mask=image.split()[3] if len(image.split()) > 3 else None)
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    # Save to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


class AttachmentThumbnail(ft.Container):
    """
    Clickable thumbnail for an attachment.
    Displays image preview or text excerpt, with click-to-expand and remove button.
    """

    THUMBNAIL_SIZE = 80

    def __init__(
        self,
        attachment: Attachment,
        on_remove: Callable[[str], None],
        on_click: Callable[[Attachment], None] | None = None,
    ):
        super().__init__()
        self.attachment = attachment
        self.on_remove = on_remove
        self.on_click_expand = on_click

        # Styling
        self.bgcolor = ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
        self.border_radius = 8
        self.padding = 0
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))
        self.width = self.THUMBNAIL_SIZE
        self.height = self.THUMBNAIL_SIZE
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE

        self.content = self._build_content()

    def _build_content(self) -> ft.Stack:
        """Build thumbnail with content and remove button overlay."""
        # Main content (image or text)
        main_content = self._create_main_content()

        # Remove button (top right)
        remove_btn = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE, size=12, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            border_radius=10,
            padding=2,
            on_click=lambda _: self.on_remove(self.attachment.id),
            right=4,
            top=4,
        )

        # Source badge (bottom left) - shows clipboard/selection icon
        source_badge = None
        if self.attachment.source:
            icon = ft.Icons.PASTE if self.attachment.source == "clipboard" else ft.Icons.TEXT_FIELDS
            source_badge = ft.Container(
                content=ft.Icon(icon, size=10, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.with_opacity(0.7, AppColors.ACCENT),
                border_radius=8,
                padding=3,
                left=4,
                bottom=4,
            )

        # Clickable wrapper
        clickable_content = ft.Container(
            content=main_content,
            on_click=self._handle_click,
            expand=True,
        )

        stack_controls = [clickable_content, remove_btn]
        if source_badge:
            stack_controls.append(source_badge)

        return ft.Stack(
            controls=stack_controls,
            width=self.THUMBNAIL_SIZE,
            height=self.THUMBNAIL_SIZE,
        )

    def _create_main_content(self) -> ft.Control:
        """Create the main visual content based on attachment type."""
        if self.attachment.type == "image" and isinstance(self.attachment.content, PILImage):
            # Image thumbnail
            try:
                base64_str = pil_image_to_base64(self.attachment.content, self.THUMBNAIL_SIZE)
                return ft.Image(
                    src_base64=base64_str,
                    fit=ft.ImageFit.COVER,
                    width=self.THUMBNAIL_SIZE,
                    height=self.THUMBNAIL_SIZE,
                )
            except Exception:
                # Fallback to icon if image conversion fails
                return self._create_icon_fallback(ft.Icons.IMAGE, AppColors.ACCENT)

        elif self.attachment.type == "text":
            # Text preview
            text_content = str(self.attachment.content) if self.attachment.content else ""
            preview = text_content[:100] + "..." if len(text_content) > 100 else text_content

            return ft.Container(
                content=ft.Text(
                    value=preview,
                    size=9,
                    color=ft.Colors.GREY_400,
                    max_lines=4,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                padding=6,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            )

        else:
            # File - show icon
            return self._create_icon_fallback(ft.Icons.INSERT_DRIVE_FILE, ft.Colors.GREY_500)

    def _create_icon_fallback(self, icon: str, color: str) -> ft.Container:
        """Create an icon-based fallback display."""
        return ft.Container(
            content=ft.Icon(icon, size=32, color=color),
            alignment=ft.alignment.center,
        )

    def _handle_click(self, e: ft.ControlEvent) -> None:
        """Handle click to expand/view full content."""
        if self.on_click_expand:
            self.on_click_expand(self.attachment)


class AttachmentPreviewDialog(ft.AlertDialog):
    """Dialog to show full attachment content (image or text)."""

    def __init__(self, attachment: Attachment, on_close: Callable[[], None]):
        self.attachment = attachment
        self._on_close = on_close

        super().__init__(
            modal=True,
            title=ft.Text(attachment.name, size=16, weight=ft.FontWeight.W_500),
            content=self._build_content(),
            actions=[
                ft.TextButton("Fermer", on_click=lambda _: self._on_close()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _build_content(self) -> ft.Control:
        """Build the dialog content based on attachment type."""
        if self.attachment.type == "image" and isinstance(self.attachment.content, PILImage):
            try:
                # Larger preview for dialog
                base64_str = pil_image_to_base64(self.attachment.content, 600)
                return ft.Container(
                    content=ft.Image(
                        src_base64=base64_str,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    width=500,
                    height=400,
                )
            except Exception:
                return ft.Text("Impossible d'afficher l'image")

        elif self.attachment.type == "text":
            text_content = str(self.attachment.content) if self.attachment.content else ""
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value=text_content,
                            size=12,
                            selectable=True,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=500,
                height=300,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                border_radius=8,
                padding=15,
            )

        else:
            # File info
            return ft.Column(
                controls=[
                    ft.Icon(ft.Icons.INSERT_DRIVE_FILE, size=48, color=ft.Colors.GREY_500),
                    ft.Text(self.attachment.name, size=14),
                    ft.Text(
                        f"Path: {self.attachment.content}",
                        size=11,
                        color=ft.Colors.GREY_500,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )


class AttachmentZone(ft.Row):
    """Zone displaying attached files, images, and source content as thumbnails."""

    def __init__(
        self,
        attachments: list[Attachment],
        on_remove_attachment: Callable[[str], None],
        on_add_click: Callable[[], None] | None = None,
        page: ft.Page | None = None,
    ):
        super().__init__()
        self.attachments = attachments
        self.on_remove_attachment = on_remove_attachment
        self.on_add_click = on_add_click
        self._page = page

        self.wrap = True
        self.spacing = 8
        self.run_spacing = 8

        self._build_controls()

    def _build_controls(self) -> None:
        """Build thumbnail controls for all attachments."""
        self.controls = []

        for att in self.attachments:
            thumbnail = AttachmentThumbnail(
                attachment=att,
                on_remove=self._handle_remove,
                on_click=self._handle_thumbnail_click,
            )
            self.controls.append(thumbnail)

    def _handle_remove(self, attachment_id: str) -> None:
        """Handle removal of an attachment."""
        self.on_remove_attachment(attachment_id)

    def _handle_thumbnail_click(self, attachment: Attachment) -> None:
        """Handle click on thumbnail - show preview dialog."""
        if self._page:
            self._current_dialog = AttachmentPreviewDialog(
                attachment=attachment,
                on_close=self._close_dialog,
            )
            self._page.open(self._current_dialog)

    def _close_dialog(self) -> None:
        """Close the preview dialog properly."""
        if self._page and hasattr(self, "_current_dialog") and self._current_dialog:
            self._page.close(self._current_dialog)
            self._current_dialog = None

    def set_page(self, page: ft.Page) -> None:
        """Set the page reference for dialog display."""
        self._page = page

    def refresh(self) -> None:
        """Rebuild controls and update display."""
        self._build_controls()
        self.update()
