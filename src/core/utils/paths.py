"""
Path utilities for Writing Assistant Pro
Handles application root detection and mode determination
"""

from __future__ import annotations

import sys
from pathlib import Path

# Global constants for paths
APP_ROOT = Path(__file__).parent.parent.parent.parent  # src/core/utils -> project root


def get_mode() -> str:
    """
    Detect the running mode of the application.
    Returns:
        str: "dev", "build-dev", or "build-final"
    """
    # Check if frozen (PyInstaller)
    if getattr(sys, "frozen", False):
        # After flattening: exe is at dist/dev/Writing Assistant Pro.exe
        # So exe parent is directly the dist subfolder (dev or final)
        exe_parent = Path(sys.executable).parent  # "dev" or "final"

        if exe_parent.name == "dev":
            return "build-dev"

        # Any other folder name (production, final, etc.) is treated as final build
        return "build-final"

    return "dev"


def get_app_root() -> Path:
    """
    Get the application root directory based on running mode.

    Returns:
        Path: The base directory for resolving external resources (
        config, styles, etc.)
    """
    mode = get_mode()

    if mode == "dev":
        # In dev mode, return project root
        # Static assets (styles, translations) are in source tree
        # Config will be in dist/dev (handled by ConfigManager)
        return APP_ROOT

    else:
        # In frozen modes (build-dev, build-final)
        # After flattening: exe is at dist/dev/Writing Assistant Pro.exe
        # External files are also in dist/dev/
        # So app_root is the same as exe parent directory
        return Path(sys.executable).parent
