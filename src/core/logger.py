"""
Centralized logging configuration for the application.
"""

import logging
import sys


def setup_logger(debug: bool, name: str = "WritingAssistant") -> logging.Logger:
    """
    Configure and return a logger for the application.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
        name: Logger name

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    if debug:
        # DEBUG mode: detailed logs with timestamp and level
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        # Production mode: simple logs
        log_level = logging.INFO
        log_format = "%(levelname)s - %(message)s"
    
    # Create a handler to display logs in the console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    # Configure the logger
    logger.setLevel(log_level)
    logger.addHandler(handler)
    
    if debug:
        logger.debug("DEBUG Mode enabled - Detailed logging")
    
    return logger
