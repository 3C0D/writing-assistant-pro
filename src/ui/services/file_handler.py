"""
File handling utilities for attachments
"""

from __future__ import annotations

import uuid

from loguru import logger
from PIL import Image

from src.core import AttachmentType
from src.ui.components.input.attachment_zone import Attachment

# Constants should be centralized
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico"}
TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".json",
    ".xml",
    ".yaml",
    ".toml",
    ".c",
    ".cpp",
    ".h",
}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | TEXT_EXTENSIONS


def is_supported_file(filename: str) -> bool:
    """Check if file type is supported."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    return f".{ext}" in SUPPORTED_EXTENSIONS


def process_picked_files(files: list) -> list[Attachment]:
    """
    Process files from FilePicker and return attachments.

    Args:
        files: List of FilePickerFile objects

    Returns:
        List of Attachment objects
    """
    attachments = []
    log = logger.bind(name="WritingAssistant.FileHandler")

    for f in files:
        if not f.path:
            continue

        if not is_supported_file(f.name):
            log.warning(f"Skipping unsupported file: {f.name}")
            continue

        ext = f.path.lower().rsplit(".", 1)[-1] if "." in f.path else ""

        try:
            if f".{ext}" in IMAGE_EXTENSIONS:
                img = Image.open(f.path)
                att_type = AttachmentType.IMAGE
                content = img
            elif f".{ext}" in TEXT_EXTENSIONS:
                with open(f.path, encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                att_type = AttachmentType.TEXT
            else:
                att_type = AttachmentType.FILE
                content = f.path

            attachments.append(
                Attachment(
                    id=str(uuid.uuid4()),
                    type=att_type,
                    content=content,
                    name=f.name,
                    size=str(f.size),
                )
            )
        except Exception as ex:
            log.error(f"Error loading file {f.name}: {ex}")

    return attachments
