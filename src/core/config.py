"""
Configuration module for Writing Assistant Pro
Centralized configuration management
"""

import argparse

# Application configuration
LANGUAGE = "fr"
DEBUG = False
DARK_MODE = False  # Change this value for theme

# Window configuration
WINDOW_SIZE = (800, 600)
WINDOW_RESIZABLE = True
WINDOW_FRAMELESS = False
WINDOW_START_HIDDEN = True

# Hotkey configuration
HOTKEY_COMBINATION = "ctrl+space"
MIN_TRIGGER_INTERVAL = 0.5  # seconds
HOTKEY_SETUP_DELAY = 2.0  # seconds


def parse_arguments():
    """
    Parse command line arguments for the application.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    global DEBUG
    parser = argparse.ArgumentParser(description="Writing Assistant Pro")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    DEBUG = args.debug
    return args


def get_config():
    """
    Get complete configuration as a dictionary.
    Useful for debugging and logging.

    Returns:
        dict: Complete configuration dictionary
    """
    return {
        "language": LANGUAGE,
        "debug": DEBUG,
        "dark_mode": DARK_MODE,
        "window_size": WINDOW_SIZE,
        "window_resizable": WINDOW_RESIZABLE,
        "window_frameless": WINDOW_FRAMELESS,
        "window_start_hidden": WINDOW_START_HIDDEN,
        "hotkey_combination": HOTKEY_COMBINATION,
        "min_trigger_interval": MIN_TRIGGER_INTERVAL,
        "hotkey_setup_delay": HOTKEY_SETUP_DELAY,
    }
