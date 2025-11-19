"""
Configuration module for Writing Assistant Pro
Centralized configuration management with JSON persistence
"""

import json
from pathlib import Path
from typing import Any

from loguru import logger

# Default configuration values
DEFAULT_CONFIG = {
    "language": "fr",
    "debug": False,
    "dark_mode": False,
    "window_size": [800, 600],
    "window_resizable": True,
    "window_frameless": False,
    "window_start_hidden": True,
    "hotkey_combination": "ctrl+.",
    "min_trigger_interval": 0.5,
    "hotkey_setup_delay": 2.0,
}


class ConfigManager:
    """
    Manages application configuration with JSON file persistence.
    Supports attribute-style access for backward compatibility.
    """

    def __init__(self, config_file: str = "config.json"):
        self._config_file = Path(config_file)
        self._config: dict[str, Any] = DEFAULT_CONFIG.copy()
        self.log = logger.bind(name="WritingAssistant.Config")
        self.load()

    def load(self) -> None:
        """Load configuration from JSON file."""
        if self._config_file.exists():
            try:
                with open(self._config_file, encoding="utf-8") as f:
                    saved_config = json.load(f)
                    # Update default config with saved values (preserves new keys in default)
                    self._config.update(saved_config)
                self.log.info(f"Configuration loaded from {self._config_file}")
            except Exception as e:
                self.log.error(f"Failed to load configuration: {e}")
        else:
            self.log.info("No configuration file found, using defaults")
            self.save()

    def save(self) -> None:
        """Save current configuration to JSON file."""
        try:
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            self.log.info(f"Configuration saved to {self._config_file}")
        except Exception as e:
            self.log.error(f"Failed to save configuration: {e}")

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
        if name.startswith("_") or name == "log":
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
    return parser.parse_args()
