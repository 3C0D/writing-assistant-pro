"""
Application entry point for Writing Assistant Pro
Properly handles window hide/show with hotkey and prevents closing
"""

from src.core import WritingAssistantApp, parse_arguments


def main():
    """Main entry point"""
    # Parse command line arguments first
    args = parse_arguments()

    # Create and run application
    app = WritingAssistantApp()
    app.run(args)


if __name__ in {"__main__", "__mp_main__"}:
    main()
