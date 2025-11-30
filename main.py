"""
Application entry point for Writing Assistant Pro (Flet version)
"""

import multiprocessing

import flet as ft

from src.core import (
    parse_arguments,
    setup_exception_handler,
    setup_root_logger,
)
from src.ui import WritingAssistantFletApp
from src.version import __version__

# Required for PyInstaller
multiprocessing.freeze_support()


def main():
    """Main entry point"""
    # Parse arguments (useful for debug flags)
    args = parse_arguments()

    # Setup logging BEFORE creating the app (important for PyInstaller)
    debug_mode = args.debug if hasattr(args, "debug") else False
    log_file = args.log_file if hasattr(args, "log_file") else None
    setup_root_logger(debug=debug_mode, log_filename=log_file)

    # Setup exception handler to log crashes to dedicated files
    setup_exception_handler()

    # Create app instance, passing debug mode and version
    app = WritingAssistantFletApp(debug=debug_mode, version=__version__)

    # Run Flet app
    # native=True is default for desktop
    ft.app(target=app.main)


if __name__ in {"__main__", "__mp_main__"}:
    main()
