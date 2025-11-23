"""
Configuration manager for Writing Assistant Pro
Centralized configuration management with JSON persistence
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from loguru import logger

from ..utils.json_helpers import load_json_file, save_json_file
from ..utils.paths import get_app_root, get_mode


def load_default_config() -> dict[str, Any]:
    """Load default configuration from config.json in the same directory."""
    config_path = Path(__file__).parent / "config.json"
    return load_json_file(config_path, default={})


DEFAULT_CONFIG = load_default_config()


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
                # Update default config with saved values (
                # preserves new keys in default)
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
        if (
            name.startswith("_")
            or name == "log"
            or name
            in [
                "mode",
                "app_root",
            ]
        ):
            super().__setattr__(name, value)
            return

        key = name.lower()
        if key in self._config:
            self.set(key, value)
        else:
            super().__setattr__(name, value)


def parse_arguments():
    """
    Parse command line arguments for the application.
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    import argparse

    parser = argparse.ArgumentParser(description="Writing Assistant Pro")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--log-file", type=str, help="Custom log filename")
    # Use parse_known_args to allow unknown arguments (
    # Flet may pass extra args)
    args, _ = parser.parse_known_args()
    return args
