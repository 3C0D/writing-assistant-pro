"""
Centralized logging configuration for the application.
Migrated to loguru for modern, colored logging with better formatting.
"""

from __future__ import annotations

import sys
import threading
import traceback
from datetime import datetime
from pathlib import Path
from types import TracebackType

from loguru import logger


def setup_root_logger(debug: bool, log_filename: str | None = None) -> None:
    """
    Configure the root logger for the entire application using loguru.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (logs), False for minimal logs
        log_filename: Optional custom filename for the log file
    """
    # Remove default handler (console output)
    logger.remove()

    # Check if we're in windowed mode (no console, sys.stderr is None)
    has_console = sys.stderr is not None

    # Determine log file directory and name
    if getattr(sys, "frozen", False):
        # Frozen: log in the directory containing the exe
        log_dir = Path(sys.executable).parent
        default_log_name = "build_dev.log" if "dev" in log_dir.name.lower() else "app.log"
    else:
        # Development: log in logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        default_log_name = "run_dev.log"

    # Use provided filename or default
    if log_filename:
        # Check if provided path is absolute
        log_path = Path(log_filename)
        if log_path.is_absolute():
            # Use as-is and ensure parent directory exists
            log_path.parent.mkdir(parents=True, exist_ok=True)
            debug_log_path = log_path
        else:
            # Relative path, join with log_dir
            debug_log_path = log_dir / log_filename
    else:
        debug_log_path = log_dir / default_log_name

    # Configure conditional dev/production logging
    if debug:
        # Development mode: Always log to file
        logger.add(
            str(debug_log_path),
            level="DEBUG",
            format=("{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"),
        )

        if has_console:
            # Also log to console if available
            logger.add(
                sys.stdout,
                level="DEBUG",
                format=(
                    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                    "<level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
                    "<level>{message}</level>"
                ),
                colorize=True,
            )
            logger.debug(
                f"Root logger configured - Debug mode enabled (console + file: {debug_log_path})"
            )
        else:
            logger.debug(f"Root logger configured - Debug mode enabled (file: {debug_log_path})")
    else:
        # Production mode: minimal logging
        if has_console:
            logger.add(
                sys.stdout,
                level="INFO",
                format=("<level>{level: <8}</level> | {name} - <level>{message}</level>"),
                colorize=True,
            )
            logger.info("Root logger configured - Production mode enabled")
        else:
            # Production windowed mode - disable logging to avoid errors
            # Logger is already removed, so no handlers = no logging
            pass  # Silent mode for production windowed builds


def setup_exception_handler(debug: bool = False) -> None:
    """
    Configure exception handlers to log crashes to dedicated crash files.
    Call this ONCE after setup_root_logger() at application startup.

    Args:
        debug: True if running in debug mode. If True, crashes will also be printed to stderr.

    Creates separate crash log files:
    - Mode run_dev: logs/crash_run_dev.log
    - Mode build_dev: logs/crash_build_dev.log
    - Mode production: crash.log (in exe parent directory)

    Normal logs continue in their respective files (run_dev.log, etc.)
    """

    # Determine crash log file path based on execution mode
    if getattr(sys, "frozen", False):
        # Frozen: crash log in the directory containing the exe
        crash_dir = Path(sys.executable).parent
        crash_filename = "crash_build_dev.log" if "dev" in crash_dir.name.lower() else "crash.log"
        crash_log_path = crash_dir / crash_filename
    else:
        # Development: crash log in logs directory
        crash_dir = Path("logs")
        crash_dir.mkdir(exist_ok=True)
        crash_log_path = crash_dir / "crash_run_dev.log"

    def exception_handler(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions by logging them to crash file."""
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't log keyboard interrupts
            # Use default exception handler to display the interrupt in the console
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Format the exception with full traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = "".join(tb_lines)

        # Log to crash file with critical level
        try:
            # Ensure crash log directory exists
            crash_dir.mkdir(parents=True, exist_ok=True)

            # Write crash info to dedicated crash file
            with open(crash_log_path, "a", encoding="utf-8") as f:
                f.write(f"\n{'=' * 80}\n")
                f.write(f"CRASH DETECTED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'=' * 80}\n")
                f.write(tb_text)
                f.write(f"{'=' * 80}\n\n")

            # Also log to normal logger if available
            logger.critical(f"Application crashed!\n{tb_text}")

            # In debug mode, ensure the crash is visible in the console (stderr)
            # This is critical for development in VS Code or terminal
            if debug and sys.stderr is not None:
                sys.__excepthook__(exc_type, exc_value, exc_traceback)

        except Exception as e:
            # Fallback if logging fails
            if sys.stderr is not None:
                print(f"Failed to log crash: {e}", file=sys.stderr)
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def thread_exception_handler(args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # ExceptHookArgs can have None for exc_value, handle that case
        if args.exc_value is None:
            return
        exception_handler(args.exc_type, args.exc_value, args.exc_traceback)

    # Install exception handlers for both main thread and secondary threads
    # sys.excepthook: Catches uncaught exceptions in the main thread
    # threading.excepthook: Catches uncaught exceptions in any thread
    # created with threading.Thread()
    # Without threading.excepthook, exceptions in threads would not be
    # logged to our crash files
    sys.excepthook = exception_handler
    threading.excepthook = thread_exception_handler

    logger.debug(f"Exception handler configured - Crash log: {crash_log_path}")
