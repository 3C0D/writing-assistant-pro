"""
UI Components package for Writing Assistant Pro
"""

from __future__ import annotations

from src.ui.components.common import icon_button, section_header, styled_container
from src.ui.components.input.attachment_zone import Attachment, AttachmentZone
from src.ui.components.input.prompt_bar import PromptBar
from src.ui.components.input.source_indicator import SourceIndicator
from src.ui.components.navigation_rail import RAIL_WIDTH, create_navigation_rail
from src.ui.components.sidebar import create_sidebar

__all__ = [
    "styled_container",
    "icon_button",
    "section_header",
    "RAIL_WIDTH",
    "create_navigation_rail",
    "create_sidebar",
    "PromptBar",
    "SourceIndicator",
    "Attachment",
    "AttachmentZone",
]
