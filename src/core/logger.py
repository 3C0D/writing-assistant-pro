"""
Centralized logging configuration for the application.
Migrated to loguru for modern, colored logging with better formatting.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_root_logger(debug: bool) -> None:
    """
    Configure the root logger for the entire application using loguru.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
    """
    # Remove default handler (console output)
    logger.remove()

    # Check if we're in windowed mode (no console, sys.stderr is None)
    has_console = sys.stderr is not None

    # Determine log file directory (next to exe when frozen, project root otherwise)
    if getattr(sys, "frozen", False):
        # Frozen: log in the directory containing the exe
        log_dir = Path(sys.executable).parent
    else:
        # Development: log in logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

    # Configure conditional dev/production logging
    if debug:
        # Development mode: Always log to file
        debug_log_path = log_dir / "debug.log"
        logger.add(
            str(debug_log_path),
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        )

        if has_console:
            # Also log to console if available
            logger.add(
                sys.stderr,
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
                sys.stderr,
                level="INFO",
                format="<level>{level: <8}</level> | {name} - <level>{message}</level>",
                colorize=True,
            )
            logger.info("Root logger configured - Production mode enabled")
        else:
            # Production windowed mode - disable logging to avoid errors
            # Logger is already removed, so no handlers = no logging
            pass  # Silent mode for production windowed builds
