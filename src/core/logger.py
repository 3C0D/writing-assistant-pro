"""
Centralized logging configuration for the application.
"""

import logging
import sys


def setup_root_logger(debug: bool) -> None:
    """
    Configure the root logger for the entire application.
    Call this ONCE at application startup.

    Args:
        debug: True to enable DEBUG mode (detailed logs), False for minimal logs
    """
    root_logger = logging.getLogger()
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    if debug:
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        log_level = logging.INFO
        log_format = "%(name)s - %(levelname)s - %(message)s"
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    
    if debug:
        root_logger.debug("Root logger configured - Debug mode enabled")
