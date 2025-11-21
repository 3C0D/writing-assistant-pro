"""
Configuration module for Writing Assistant Pro
Centralized configuration management with JSON persistence
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from loguru import logger

from .utils import load_json_file, save_json_file


# Default configuration values
# Default configuration values
def load_default_config() -> dict[str, Any]:
    """Load default configuration from config.json in the same directory."""
    config_path = Path(__file__).parent / "config.json"
    return load_json_file(config_path, default={})


DEFAULT_CONFIG = load_default_config()


# Global constants for paths
APP_ROOT = Path(__file__).parent.parent.parent  # Default for dev mode


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
        elif exe_parent.name == "final":
            return "build-final"
        # Fallback if structure is unexpected
        return "build-final"

    return "dev"


def get_app_root() -> Path:
    """
    Get the application root directory based on running mode.

    Returns:
        Path: The base directory for resolving external resources (config, styles, etc.)
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


class ConfigManager:
    """
    Manages application configuration with JSON file persistence.
    Supports attribute-style access for backward compatibility.
    """

    def __init__(self, config_file: str = "config.json"):
        self.mode = get_mode()
        self.app_root = get_app_root()
        self.log = logger.bind(name="WritingAssistant.Config")

        # Determine config file path based on mode
        if self.mode == "dev":
            # Dev mode uses dist/dev/config.json to share with build-dev
            dist_dev = self.app_root / "dist" / "dev"
            dist_dev.mkdir(parents=True, exist_ok=True)
            self._config_file = dist_dev / config_file
        else:
            # Frozen modes use config.json next to executable
            self._config_file = self.app_root / config_file

        self._config: dict[str, Any] = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from JSON file."""
        if self._config_file.exists():
            saved_config = load_json_file(self._config_file)
            if saved_config:
                # Update default config with saved values (preserves new keys in default)
                self._config.update(saved_config)
                self.log.info(f"Configuration loaded from {self._config_file} (Mode: {self.mode})")
        else:
            self.log.info(f"No configuration file found at {self._config_file}, using defaults")
            self.save()

    def save(self) -> None:
        """Save current configuration to JSON file."""
        save_json_file(self._config_file, self._config)
        self.log.info(f"Configuration saved to {self._config_file}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save."""
        self._config[key] = value
        self.save()

    def __getattr__(self, name: str) -> Any:
        """
        Allow attribute-style access to configuration keys (uppercase).
        Example: config.DEBUG -> config.get('debug')
        """
        key = name.lower()
        if key in self._config:
            return self._config[key]
        raise AttributeError(f"'ConfigManager' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Allow attribute-style assignment for configuration keys (uppercase).
        Example: config.DEBUG = True -> config.set('debug', True)
        """
        if name.startswith("_") or name == "log" or name in ["mode", "app_root"]:
            super().__setattr__(name, value)
            return

        key = name.lower()
        if key in self._config:
            self.set(key, value)
        else:
            super().__setattr__(name, value)


# Global instance for backward compatibility if needed,
# but prefer creating an instance in App
# config = ConfigManager()


def parse_arguments():
    """
    Parse command line arguments for the application.
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    import argparse

    parser = argparse.ArgumentParser(description="Writing Assistant Pro")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    # Use parse_known_args to ignore NiceGUI's multiprocessing arguments
    args, _ = parser.parse_known_args()
    return args
