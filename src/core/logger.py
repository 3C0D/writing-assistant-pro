"""
Centralized logging configuration for the application.
Migrated to loguru for modern, colored logging with better formatting.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_root_logger(debug: bool, log_filename: str | None = None) -> None:
    """
    Configure the root logger for the entire application using loguru.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
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
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        )

        if has_console:
            # Also log to console if available
            logger.add(
                sys.stdout,
                level="DEBUG",
                format=(
                    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
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
                format="<level>{level: <8}</level> | {name} - <level>{message}</level>",
                colorize=True,
            )
            logger.info("Root logger configured - Production mode enabled")
        else:
            # Production windowed mode - disable logging to avoid errors
            # Logger is already removed, so no handlers = no logging
            pass  # Silent mode for production windowed builds
