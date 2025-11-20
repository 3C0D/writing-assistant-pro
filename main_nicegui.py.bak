"""
Application entry point for Writing Assistant Pro
Properly handles window hide/show with hotkey and prevents closing
"""

import multiprocessing

from src.core import WritingAssistantApp, parse_arguments

# Required for PyInstaller on Windows with multiprocessing used by NiceGUI
# Must be called at module level before any multiprocessing
multiprocessing.freeze_support()


def main():
    """Main entry point"""
    # Parse command line arguments first
    args = parse_arguments()

    # Create and run application
    app = WritingAssistantApp()
    app.run(args)


# Call main directly without guard for NiceGUI multiprocessing compatibility
# NiceGUI's native mode requires ui.run() to be accessible in subprocesses
if __name__ in {"__main__", "__mp_main__"}:
    main()
