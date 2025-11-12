"""
Application entry point for Writing Assistant Pro
Properly handles window hide/show with hotkey and prevents closing
"""

from src.core import parse_arguments
from src.core import WritingAssistantApp


def main():
    """Main entry point"""
    # Parse command line arguments first
    parse_arguments()

    # Create and run application
    app = WritingAssistantApp()
    app.run()

if __name__ in {'__main__', '__mp_main__'}:
    main()
