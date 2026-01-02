# Error Handling in Writing Assistant Pro

## Overview

This document explains the error handling system implemented in Writing Assistant Pro, its current purpose, future goals, and how it integrates with Loguru.

## Current Implementation

### The Error Handler Module (`src/core/error_handler.py`)

The error handling system provides a **standardized way to manage exceptions** throughout the application. It consists of:

#### 1. **Base Exception Class: `AppError`**

```python
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
```

**Arguments:**
- `message` (str): Human-readable error message
- `code` (str | None): Unique identifier for error type
- `details` (Any): Additional debugging context

#### 2. **Specific Error Classes**

```python
class ConfigError(AppError):  # Configuration errors
class HotkeyError(AppError):  # Hotkey registration errors
class InputError(AppError):   # Input source errors
class UIError(AppError):      # User interface errors
```

#### 3. **Error Handling Functions**

**`handle_error()` - Standardized error handler:**
```python
def handle_error(
    error: Exception,
    *,
    logger_instance: Any = None,
    reraise: bool = False,
    fallback: Any = None,
    error_type: type[AppError] | None = None,
    context: str = "",
) -> Any:
```

**`safe_execute()` - Execute functions safely:**
```python
def safe_execute(
    func: Callable, *args, error_handler: Callable | None = None, **kwargs
) -> tuple[bool, Any]:
```

**`ErrorContext()` - Context manager:**
```python
with ErrorContext("loading config", reraise=True) as ctx:
    config = load_config()
if ctx.last_error:
    print(f"Error occurred: {ctx.last_error}")
```

## How It Works Currently

### Integration with Loguru

The system uses **Loguru** for all logging operations:

```python
from loguru import logger

def handle_error(...):
    logger_instance = logger.bind(name="WritingAssistant.ErrorHandler")
    logger_instance.error(f"Error{context_str}: {error}", exc_info=True)
```

**What `exc_info=True` does:**
- Includes complete exception information in logs
- Adds stack trace, file location, and line number
- Provides full context for debugging

### Example Usage

#### Basic Error Handling with Fallback
```python
from src.core import handle_error, ConfigError

try:
    config = load_config()
except Exception as e:
    # Logs error with stack trace and context
    # Returns fallback value
    # Can convert to AppError type
    config = handle_error(
        e,
        context="loading config",
        error_type=ConfigError,
        code="CONFIG001",
        fallback={}
    )
```

#### Re-raising Errors with Exception Chain
```python
try:
    handle_error(
        ValueError("original error"),
        error_type=ConfigError,
        code="CONFIG001",
        reraise=True
    )
except ConfigError as e:
    print(e)  # ConfigError: original error (code: CONFIG001)
    print(e.__cause__)  # ValueError: original error
```

#### Using ErrorContext
```python
with ErrorContext("loading config", fallback="default") as ctx:
    config = load_config()

if ctx.last_error:
    print(f"Erreur : {ctx.last_error}")
    print(f"Résultat : {ctx.result}")  # "default"
```

#### Safe Execute
```python
# Basic usage
success, result = safe_execute(my_function, arg1, arg2)

# With custom handler
def my_handler(error):
    handle_error(error, context="custom", error_type=CustomError, fallback="default")

success, result = safe_execute(my_function, error_handler=my_handler)
```

### Logging Output Format

With Loguru configured:
```
2026-01-01 15:59:42.108 | ERROR | src.core.error_handler:handle_error:96 - Error [loading config]: FileNotFoundError
Traceback (most recent call last):
  File "src/core/config/manager.py", line 45, in load
    saved_config = load_json_file(self._config_file)
  ...
FileNotFoundError: Configuration file not found
```

## Key Improvements and Fixes

### 1. **Exception Chain Preservation**
```python
# BEFORE (BUG):
if error_type and not isinstance(error, AppError):
    error = error_type(str(error), details=traceback.format_exc())
if reraise:
    raise error from error  # ❌ from error = nouvelle exception!

# AFTER (FIXED):
original_error = error  # ✅ Garde référence originale
if error_type and not isinstance(error, AppError):
    error = error_type(str(error), details=traceback.format_exc())
if reraise:
    raise error from original_error  # ✅ Chaîne correcte
```

### 2. **ErrorContext Fallback Logic**
```python
# BEFORE (BUG):
def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
        if self.fallback is not None:
            self.result = self.fallback  # ❌ Utilisé sans erreur!
    # ...

# AFTER (FIXED):
def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
        return True  # ✅ Pas d'erreur, pas de fallback

    # Erreur survenue
    self.last_error = error
    if self.fallback is not None:
        self.result = self.fallback  # ✅ Utilisé SEULEMENT en cas d'erreur
    return True
```

### 3. **Enhanced ErrorContext**
```python
class ErrorContext:
    def __init__(self, context, reraise=False, fallback=None):
        self.fallback = fallback
        self.last_error = None  # ✅ Nouveau
        self.result = None      # ✅ Nouveau

    def __enter__(self):
        self.logger.debug(f"Entering context '{self.context}'")  # ✅ Nouveau
        return self
```

## Why This System Exists

### Problem It Solves

**Without this system:**
```python
try:
    config = load_config()
except Exception as e:
    print(f"Error: {e}")
    # No context, no stack trace in logs, inconsistent handling
```

**With this system:**
```python
try:
    config = load_config()
except Exception as e:
    handle_error(e, context="loading config", fallback={})
    # ✅ Standardized format
    # ✅ Complete stack trace
    # ✅ Context information
    # ✅ Consistent across application
```

### Benefits

1. **Standardization**: All errors handled the same way
2. **Debugging**: Complete stack traces and context
3. **Flexibility**: Can return fallback values or re-raise
4. **Categorization**: Error codes for programmatic handling
5. **Production-ready**: Structured logging for monitoring
6. **Exception chains**: Preserves original error context

## Current Usage Status

### Where It's Used

- **Tests**: `tests/test_error_handler.py` - Comprehensive test coverage
- **Core modules**: Available for import throughout the application
- **Logging**: Integrated with Loguru's logging system

### Where It's NOT Used (Yet)

The system is **implemented but not widely adopted** in the main application code. Most of the application currently uses standard Python exceptions or direct logging.

## Future Goals

### 1. **Widespread Adoption**

Replace scattered error handling with the standardized system:

```python
# Current (scattered):
try:
    hotkey = register_hotkey()
except Exception as e:
    logger.error(f"Hotkey error: {e}")
    return False

# Future (standardized):
try:
    hotkey = register_hotkey()
except Exception as e:
    handle_error(e, error_type=HotkeyError, code="HOTKEY001")
    return False
```

### 2. **Error Code Registry**

Create a centralized error code system:

```python
ERROR_CODES = {
    "CONFIG001": "Configuration file not found",
    "HOTKEY001": "Hotkey already registered",
    "INPUT001": "Unsupported input format",
    "UI001": "UI component not found",
    # etc.
}
```

### 3. **User-Friendly Error Messages**

Map technical errors to user-friendly messages:

```python
def get_user_message(error: AppError) -> str:
    if error.code == "CONFIG001":
        return "Configuration file is missing. Using default settings."
    # ...
```

### 4. **Error Recovery Strategies**

Implement automatic recovery based on error type:

```python
def handle_error_with_recovery(error: AppError):
    if error.code.startswith("CONFIG"):
        return load_default_config()
    elif error.code.startswith("HOTKEY"):
        return disable_hotkey()
    # ...
```

### 5. **Enhanced Logging with Loguru**

Leverage Loguru's advanced features:

```python
# Structured logging
logger.error(
    "Error occurred",
    extra={
        "error_code": error.code,
        "context": context,
        "user_id": user_id,
        "timestamp": time.time()
    }
)

# Conditional logging based on environment
if debug_mode:
    logger.debug("Detailed error info", exc_info=True)
else:
    logger.error(f"Error: {error.message}")
```

## Loguru's Default System

### What Loguru Provides Out-of-the-Box

```python
from loguru import logger

# Basic logging
logger.info("Information message")
logger.error("Error message")

# Exception logging
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed")  # Automatically includes exc_info
```

### Configuration Options

```python
# Remove default handler
logger.remove()

# Add custom handler
logger.add(
    "app.log",
    format="{time} | {level} | {name} | {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="1 month",
    compression="zip",
    backtrace=True,
    diagnose=True
)
```

### Why We Need Both

**Loguru alone:**
- Provides logging infrastructure
- Handles formatting and output
- Manages log files and rotation

**Error handler + Loguru:**
- Standardizes error creation and handling
- Adds error codes and categorization
- Provides fallback mechanisms
- Enables programmatic error handling
- Creates a consistent error interface
- **Preserves exception chains** (critical for debugging)

## Implementation Strategy

### Phase 1: Foundation ✅
- Create error classes
- Implement basic handlers
- Set up tests
- **Fix critical bugs** (exception chains, fallback logic)

### Phase 2: Integration (Future)
- Replace scattered error handling
- Add error codes to all modules
- Implement recovery strategies

### Phase 3: User Experience (Future)
- Map technical errors to user messages
- Add error notifications
- Implement retry mechanisms

### Phase 4: Monitoring (Future)
- Error analytics
- Performance impact tracking
- Alerting for critical errors

## Testing

The module includes comprehensive tests:

```bash
uv run pytest tests/test_error_handler.py -v -s
```

**Tests cover:**
- ✅ Basic error handling
- ✅ Fallback values
- ✅ Exception re-raising
- ✅ Error type conversion
- ✅ Safe execution
- ✅ Context manager behavior
- ✅ Exception chain preservation
- ✅ ErrorContext result storage

## Conclusion

The error handling system is a **foundational infrastructure** that provides:

1. **Standardization** for consistent error management
2. **Debugging capabilities** with complete context
3. **Flexibility** for different error scenarios
4. **Future extensibility** for advanced features
5. **Proper exception chains** for debugging

**Important fixes implemented:**
- ✅ `raise error from original_error` preserves exception chains
- ✅ `ErrorContext` fallback only used when errors occur
- ✅ `ErrorContext.result` provides access to fallback values
- ✅ `__enter__` logs context entry for debugging

While currently underutilized in the main application, it provides the **tools needed** for robust error management as the application grows. The integration with Loguru ensures that errors are not only handled properly but also logged in a structured, searchable format suitable for both development and production environments.
