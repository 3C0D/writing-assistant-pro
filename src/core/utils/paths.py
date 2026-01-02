"""
Path utilities for Writing Assistant Pro
Handles application root detection and mode determination
"""

from __future__ import annotations

import os
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


def get_icon_path() -> Path:
    """
    Get the path to the application icon.
    Prioritizes .ico on Windows for better compatibility.

    Returns:
        Path: Path to the app_icon.ico or app_icon.png file.
    """
    app_root = get_app_root()

    is_windows = os.name == "nt"
    primary_ext = ".ico" if is_windows else ".png"
    secondary_ext = ".png" if is_windows else ".ico"

    # Search folders
    folders = [
        app_root / "src" / "core" / "config" / "icons",
        app_root / "icons",
        app_root / "assets" / "icons",
    ]

    # Try primary extension first
    for folder in folders:
        path = folder / f"app_icon{primary_ext}"
        if path.exists():
            return path

    # Try secondary extension
    for folder in folders:
        path = folder / f"app_icon{secondary_ext}"
        if path.exists():
            return path

    # Final fallback to source png
    return APP_ROOT / "src" / "core" / "config" / "icons" / "app_icon.png"
