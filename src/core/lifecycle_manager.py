"""
Lifecycle Manager for Writing Assistant Pro

Handles application lifecycle events such as restart and shutdown.
"""

import logging
import os
import sys

logger = logging.getLogger(__name__)


class LifecycleManager:
    """
    Manages application lifecycle events.
    """

    @staticmethod
    def restart_app() -> None:
        """
        Restart the application.
        Works for both development (script) and frozen (exe) modes.
        """
        logger.info("Initiating application restart...")

        try:
            # Flush stdout/stderr to ensure logs are written
            sys.stdout.flush()
            sys.stderr.flush()

            if getattr(sys, "frozen", False):
                # Frozen mode (PyInstaller)
                # Re-execute the executable
                logger.info(f"Restarting frozen app: {sys.executable}")
                os.execl(sys.executable, sys.executable, *sys.argv[1:])
            else:
                # Development mode
                # Re-execute the python interpreter with the script
                python = sys.executable
                script = sys.argv[0]
                args = sys.argv[1:]

                logger.info(f"Restarting dev app: {python} {script} {args}")
                os.execl(python, python, script, *args)

        except Exception as e:
            logger.exception(f"Failed to restart application: {e}")
            # Fallback: just exit if restart fails
            sys.exit(1)

    @staticmethod
    def shutdown_app(exit_code: int = 0) -> None:
        """
        Shutdown the application.
        """
        logger.info(f"Shutting down application with code {exit_code}")
        sys.exit(exit_code)
