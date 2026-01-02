"""
Error Handling Module for Writing Assistant Pro

Provides standardized error handling patterns and utilities.
"""

from __future__ import annotations

import traceback
from collections.abc import Callable
from typing import Any

from loguru import logger


class AppError(Exception):
    """
    Base exception for application errors.

    This class provides a standardized way to create and handle errors
    throughout the application with support for error codes and additional details.

    Attributes:
        message (str): Human-readable error message for developers and logging
        code (str | None): Unique identifier for error type (e.g., "CONFIG001", "HOTKEY001")
                          Used for programmatic error handling and categorization
        details (Any): Additional context information for debugging (e.g., stack traces,
                      configuration values, file paths, state information)
    """

    def __init__(self, message: str, code: str | None = None, details: Any = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details

    def __str__(self) -> str:
        base = f"{self.__class__.__name__}: {self.message}"
        if self.code:
            base += f" (code: {self.code})"
        return base


class ConfigError(AppError):
    """Configuration-related errors"""

    pass


class HotkeyError(AppError):
    """Hotkey-related errors"""

    pass


class InputError(AppError):
    """Input source-related errors"""

    pass


class UIError(AppError):
    """UI-related errors"""

    pass


def handle_error(
    error: Exception,
    *,
    logger_instance: Any = None,
    reraise: bool = False,
    fallback: Any = None,
    error_type: type[AppError] | None = None,
    context: str = "",
) -> Any:
    """
    Standardized error handling function.

    Args:
        error: The exception to handle
        logger_instance: Logger instance to use (defaults to module logger)
        reraise: Whether to re-raise the exception
        fallback: Value to return on error
        error_type: Convert to this AppError type
        context: Additional context for logging

    Returns:
        fallback value if not reraising, otherwise raises the error
    """
    if logger_instance is None:
        logger_instance = logger.bind(name="WritingAssistant.ErrorHandler")

    # Log the error
    context_str = f" [{context}]" if context else ""
    logger_instance.error(f"Error{context_str}: {error}", exc_info=True)

    # Keep reference to original error for exception chain
    original_error = error

    # Convert to AppError if needed
    if error_type and not isinstance(error, AppError):
        error = error_type(str(error), details=traceback.format_exc())

    # Reraise or return fallback
    if reraise:
        raise error from original_error
    return fallback


def safe_execute(
    func: Callable, *args, error_handler: Callable | None = None, **kwargs
) -> tuple[bool, Any]:
    """
    Execute a function safely and return success status + result.

    Args:
        func: Function to execute
        *args: Positional arguments for func
        error_handler: Custom error handler function (can be handle_error or custom)
        **kwargs: Keyword arguments for func

    Returns:
        Tuple of (success: bool, result: Any)

    Usage:
        # Basic usage
        success, result = safe_execute(my_function, arg1, arg2)

        # With custom error handler
        def my_handler(error):
            handle_error(error, context="custom", error_type=CustomError)

        success, result = safe_execute(my_function, error_handler=my_handler)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        if error_handler:
            # If error_handler is handle_error, it will return fallback
            # But we need to capture it
            fallback = error_handler(e)
            # If the handler returned something, use it as result
            if fallback is not None:
                return False, fallback
        else:
            handle_error(e)
        return False, None


class ErrorContext:
    """
    Context manager for error handling with automatic logging.

    Usage:
        with ErrorContext("loading config", reraise=True) as ctx:
            config = load_config()
        if ctx.last_error:
            print(f"Error occurred: {ctx.last_error}")
    """

    def __init__(
        self, context: str, logger_instance: Any = None, reraise: bool = False, fallback: Any = None
    ):
        self.context = context
        self.logger = logger_instance or logger.bind(name="WritingAssistant.ErrorContext")
        self.reraise = reraise
        self.fallback = fallback
        self.last_error = None
        self.result = None

    def __enter__(self):
        self.logger.debug(f"Entering context '{self.context}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No error occurred
            return True

        error = exc_val
        self.logger.error(
            f"Error in context '{self.context}': {error}", exc_info=(exc_type, exc_val, exc_tb)
        )

        if self.reraise:
            return False  # Re-raise

        # Store the error for potential later use
        self.last_error = error
        # Use fallback ONLY when error occurs and is suppressed
        if self.fallback is not None:
            self.result = self.fallback
        # Return True to suppress exception
        return True
