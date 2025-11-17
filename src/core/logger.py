"""
Centralized logging configuration for the application.
Migrated to loguru for modern, colored logging with better formatting.
"""

import sys

from loguru import logger


def setup_root_logger(debug: bool) -> None:
    """
    Configure the root logger for the entire application using loguru.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (detailed logs with colors), False for minimal logs
    """
    # Remove default handler (console output)
    logger.remove()

    # Configure conditional dev/production logging
    if debug:
        # Development mode: detailed, colored logs with timestamps
        logger.add(
            sys.stderr,
            level="DEBUG",
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
            ),
            colorize=True,
        )
        logger.debug("Root logger configured - Debug mode enabled with colored output")
    else:
        # Production mode: clean, minimal logs without timestamps
        logger.add(
            sys.stderr,
            level="INFO",
            format="<level>{level: <8}</level> | {name} - <level>{message}</level>",
            colorize=True,
        )
        logger.info("Root logger configured - Production mode enabled")
