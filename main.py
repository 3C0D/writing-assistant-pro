"""
Application entry point for Writing Assistant Pro (Flet version)
"""

import multiprocessing

import flet as ft

from src.core import parse_arguments
from src.ui import WritingAssistantFletApp

# Required for PyInstaller
multiprocessing.freeze_support()


def main():
    """Main entry point"""
    # Parse arguments (useful for debug flags)
    parse_arguments()

    app = WritingAssistantFletApp()

    # Run Flet app
    # native=True is default for desktop
    ft.app(target=app.main)


if __name__ in {"__main__", "__mp_main__"}:
    main()
