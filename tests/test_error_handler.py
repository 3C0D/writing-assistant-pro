"""Tests for error handler module"""

import pytest

from src.core.error_handler import (
    AppError,
    ConfigError,
    ErrorContext,
    HotkeyError,
    InputError,
    UIError,
    handle_error,
    safe_execute,
)


def test_app_error():
    """Test base AppError class"""
    error = AppError("Test message", code="TEST001", details={"key": "value"})

    assert error.message == "Test message"
    assert error.code == "TEST001"
    assert error.details == {"key": "value"}
    assert "AppError: Test message (code: TEST001)" in str(error)


def test_error_subclasses():
    """Test error subclasses"""
    assert issubclass(ConfigError, AppError)
    assert issubclass(HotkeyError, AppError)
    assert issubclass(InputError, AppError)
    assert issubclass(UIError, AppError)

    config_error = ConfigError("Config failed")
    assert isinstance(config_error, AppError)


def test_handle_error_with_fallback():
    """Test handle_error returns fallback"""
    error = ValueError("Test error")
    result = handle_error(error, fallback="fallback_value")
    assert result == "fallback_value"


def test_handle_error_reraise():
    """Test handle_error reraises"""
    error = ValueError("Test error")

    with pytest.raises(ValueError):
        handle_error(error, reraise=True)


def test_handle_error_with_error_type():
    """Test handle_error converts to AppError"""
    error = ValueError("Test error")
    result = handle_error(error, error_type=ConfigError, fallback="fallback")

    # Should return fallback but error should be converted
    assert result == "fallback"


def test_safe_execute_success():
    """Test safe_execute with successful function"""

    def func(x, y):
        return x + y

    success, result = safe_execute(func, 2, 3)

    assert success is True
    assert result == 5


def test_safe_execute_failure():
    """Test safe_execute with failing function"""

    def func():
        raise ValueError("Failed")

    success, result = safe_execute(func)

    assert success is False
    assert result is None


def test_safe_execute_with_custom_handler():
    """Test safe_execute with custom error handler"""

    def func():
        raise ValueError("Failed")

    errors = []

    def custom_handler(e):
        errors.append(e)

    success, result = safe_execute(func, error_handler=custom_handler)

    assert success is False
    assert len(errors) == 1
    assert str(errors[0]) == "Failed"


def test_error_context_success():
    """Test ErrorContext with successful operation"""
    with ErrorContext("test operation"):
        result = 42

    assert result == 42


def test_error_context_suppresses():
    """Test ErrorContext suppresses errors"""
    with ErrorContext("test operation", reraise=False):
        raise ValueError("Test error")

    # Should not raise
    assert True


def test_error_context_reraise():
    """Test ErrorContext reraises errors"""
    with pytest.raises(ValueError):
        with ErrorContext("test operation", reraise=True):
            raise ValueError("Test error")
