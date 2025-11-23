"""
Utility functions for Writing Assistant Pro.
Common operations for file handling and data management.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger


def load_json_file(path: Path, default: Any = None) -> Any:
    """
    Load data from a JSON file.

    Args:
        path: Path to the JSON file
        default: Default value to return if file doesn't exist or fails to load

    Returns:
        Loaded data or default value
    """
    if not path.exists():
        return default

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {path}: {e}")
        return default


def save_json_file(path: Path, data: Any) -> None:
    """
    Save data to a JSON file.
    Creates parent directories if they don't exist.

    Args:
        path: Path to the JSON file
        data: Data to save
    """
    try:
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save JSON to {path}: {e}")


def update_json_file(path: Path, updates: dict) -> None:
    """
    Update an existing JSON file with new data.
    Merges updates into existing data.

    Args:
        path: Path to the JSON file
        updates: Dictionary of updates to apply
    """
    data = load_json_file(path, default={})
    if isinstance(data, dict):
        data.update(updates)
        save_json_file(path, data)
    else:
        logger.error(f"Cannot update JSON file {path}: content is not a dictionary")
