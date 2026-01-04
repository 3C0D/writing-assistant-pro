# Coding Guidelines for Writing Assistant Pro

## 📋 Overview

This document provides comprehensive guidelines for maintaining code quality, consistency, and best practices in the Writing Assistant Pro project. It serves as a reference for both human developers and AI assistants to ensure rigorous standards are maintained.

---

## 🛠️ Technology Stack & Tools

### Core Technologies

- **Python 3.13+**: Primary language
- **Flet 0.24+**: UI framework for cross-platform desktop applications
- **Loguru**: Advanced logging system
- **Pyright**: Static type checking
- **Ruff**: Linting and code formatting
- **Pre-commit**: Git hooks for quality assurance
- **UV**: Package management and script execution

### Key Libraries & Patterns

- **Event Bus**: Decoupled communication between components (`src/core/event_bus.py`)
- **Error Reporting**: Comprehensive error handling with `error_handler.py` and `AppError` classes
- **Translation System**: Multi-language support via gettext (6-7 languages: en, fr, it, es, de, pt, ru, zh, ja)
- **Configuration Management**: Centralized config with JSON persistence (`ConfigManager`)
- **Hotkey System**: Global keyboard shortcuts with scancode-based capture
- **Systray Integration**: System tray functionality via pystray
- **Input Source Management**: Clipboard and text selection detection
- **Resource Management**: Safe file/image handling with context managers

### Quality Assurance Tools

- **Ruff**: Linting and formatting (configured in `pyproject.toml`)
- **Pyright**: Type checking with basic mode
- **Pre-commit**: Automated quality checks before commits
- **Commitizen**: Conventional commit messages

---

## 📁 Project Structure

```
writing-assistant-pro/
├── src/
│   ├── core/                    # Core business logic
│   │   ├── config/             # Configuration management
│   │   │   ├── manager.py      # ConfigManager with JSON persistence
│   │   │   └── config.json     # Default configuration
│   │   ├── managers/           # System managers
│   │   │   ├── hotkey.py       # HotkeyManager (global hotkeys)
│   │   │   ├── window.py       # WindowManager (visibility, toggling)
│   │   │   ├── systray.py      # SystrayManager (system tray)
│   │   │   └── autostart.py    # AutostartManager (boot startup)
│   │   ├── services/           # Business services
│   │   │   ├── hotkey_capture.py  # Scancode-based key capture
│   │   │   ├── input_source.py    # Clipboard/selection detection
│   │   │   ├── logger.py       # Loguru configuration
│   │   │   ├── translation.py  # i18n with gettext
│   │   │   └── updater.py      # GitHub release checker
│   │   ├── utils/              # Utility functions
│   │   │   ├── json_helpers.py # JSON load/save helpers
│   │   │   └── paths.py        # Path resolution utilities
│   │   ├── event_bus.py        # Pub/sub event system
│   │   ├── error_handler.py    # Error handling & reporting
│   │   ├── state.py            # Application state (AppState, UIState)
│   │   ├── enums.py            # Enums (AttachmentID, EventType, etc.)
│   │   └── resource_manager.py # Safe resource context managers
│   └── ui/
│       ├── app.py              # Main Flet application
│       ├── design_system.py    # Design tokens (colors, spacing, typography)
│       ├── components/         # Reusable UI components
│       │   ├── common.py       # Common factories (icon_button, styled_container)
│       │   ├── navigation_rail.py  # Left navigation rail
│       │   ├── sidebar.py          # Collapsible sidebar
│       │   ├── top_action_bar.py   # Floating action buttons
│       │   └── input/          # Input-related components
│       │       ├── prompt_bar.py       # Main input area
│       │       ├── attachment_zone.py  # File/image attachments
│       │       └── source_indicator.py # Source toggle buttons
│       ├── dialogs/            # Modal dialogs
│       │   ├── hotkey_dialog.py    # Hotkey capture dialog
│       │   └── update_dialog.py    # Update notification dialogs
│       ├── services/           # UI-specific services
│       │   └── file_handler.py     # File processing for attachments
│       └── views/              # Main views
│           ├── main_view.py        # Main content view
│           ├── settings_view.py    # Settings view (class-based)
│           └── about_view.py       # About view
├── scripts/
│   ├── quality/                # Quality checks
│   │   ├── run_ruff.py        # Ruff linting & formatting
│   │   └── run_pyright.py     # Pyright type checking
│   ├── dev_build/              # Development & build scripts
│   └── translation_management/ # Translation updates
├── tests/                      # Unit tests
├── translations/               # i18n files (gettext)
├── docs/                       # Documentation
└── main.py                     # Application entry point
```

---

## 🎯 Coding Standards

### 1. Language & Comments

- **Comments**: Always in **English**
- **Code**: Follow PEP 8 conventions
- **Type Hints**: Required for all functions and methods
- **Docstrings**: Required for public functions/classes

### 2. Import Organization

Imports must be organized in this order:

```python
# 1. Standard library imports
from __future__ import annotations
import os
from collections.abc import Callable

# 2. Third-party imports
import flet as ft
from loguru import logger

# 3. Project imports (core first, then ui)
from src.core import (
    AppState,
    ConfigManager,
    EventType,
    _,
)
from src.ui.components import (
    RAIL_WIDTH,
    create_navigation_rail,
)

# 4. TYPE_CHECKING imports (if needed)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.managers.hotkey import HotkeyManager
```

### 3. Error Handling

**Always use the centralized error reporting system:**

```python
from src.core.error_handler import error_handler, AppError, handle_error

# For critical functions
@error_handler
def critical_function():
    # Errors are automatically caught and reported
    pass

# For manual error handling
try:
    risky_operation()
except Exception as e:
    handle_error(e, context="operation_name", error_type=AppError)

# Custom error types
class MyError(AppError):
    pass

handle_error(e, error_type=MyError, context="specific_context")
```

**Error Context**: Always provide meaningful context for debugging.

### 4. Logging

**Use Loguru for all logging:**

```python
from loguru import logger

# In classes
self.log = logger.bind(name="ClassName")

# Log levels
self.log.debug("Detailed information for debugging")
self.log.info("General information about operations")
self.log.warning("Something unexpected but not critical")
self.log.error("Error occurred but application continues")
self.log.critical("Critical failure requiring attention")

# With context
self.log.info(f"Processing file: {filename}")
self.log.error(f"Failed to load config: {e}", exc_info=True)
```

### 5. Event Bus

**Use for decoupled communication:**

```python
from src.core import EventType, emit_event, get_event_bus, on_event

# Subscribe in class
bus = get_event_bus()
bus.on(EventType.LANGUAGE_CHANGED, self._handle_language_change)

# Emit events
emit_event(EventType.LANGUAGE_CHANGED, {"language": "fr"})

# Decorator style
@on_event(EventType.WINDOW_SHOWN)
def handle_window_shown(data):
    # Called when window is shown
    pass
```

**Event Types**: Use `EventType` enum, never magic strings.

### 6. Configuration

**Access config through AppState:**

```python
# ✅ Correct
self.state.config.DARK_MODE
self.state.config.HOTKEY_COMBINATION

# ❌ Wrong
import config  # Don't import config directly
from src.core.config import config  # Don't access globally
```

**ConfigManager**: Handles persistence automatically via `set()` and attribute access.

### 7. Translations

**Always use translation function:**

```python
from src.core import _

# In code
text = _("Hello World")

# In UI components
ft.Text(_("Settings"))

# With formatting
message = _("Hotkey: {display}").format(display=display)
```

**Translation Workflow**: After adding strings, run `uv run python scripts/translation_management/update_translations.py`

### 8. State Management

**Use centralized state:**

```python
from src.core import AppState, UIState

# Access state
self.state.config.DARK_MODE
self.state.ui_state.settings_visible
self.state.input_state.has_selection

# Update state (triggers events if needed)
self.state.config.DARK_MODE = new_mode
emit_event(EventType.THEME_CHANGED, {"dark_mode": new_mode})
```

---

## 🔧 Development Workflow

### 1. Code Quality Checks

Before committing, always run:

```bash
# Format and lint
uv run python scripts/quality/run_ruff.py

# Type checking
uv run python scripts/quality/run_pyright.py
```

### 2. Testing

```bash
# Run all tests
uv run python -m pytest

# Run specific test
uv run python -m pytest tests/test_config.py

# Run with coverage
uv run python -m pytest --cov=src
```

### 3. Translation Updates

After adding new translatable strings:

```bash
uv run python scripts/translation_management/update_translations.py
```

### 4. Development Server

```bash
uv run python main.py --debug
```

### 5. Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## 🏗️ Architecture Patterns

### 1. State Management

- **AppState**: Central state container (config, input_state, ui_state)
- **UIState**: UI-specific state (visibility flags, theme)
- **ConfigManager**: Persistent configuration with JSON storage
- **InputState**: Input source detection state

### 2. View Pattern

Views are created as functions or classes:

```python
# Function-based view
def create_main_content(...) -> ft.Container:
    return ft.Container(...)

# Class-based view
class SettingsView:
    def __init__(self, config, ...):
        self.config = config

    def build(self) -> ft.Container:
        return ft.Container(...)
```

### 3. Component Pattern

Reusable UI components with factory functions:

```python
def create_top_action_bar(...) -> ft.Row:
    """Create top action bar with theme toggle and hide button."""
    return ft.Row(...)
```

### 4. Service Pattern

Business logic services:

```python
class InputSourceService:
    def __init__(self, shared_input_state: InputState):
        self._shared_state = shared_input_state

    def detect_sources(self) -> InputState:
        # Business logic here
        pass
```

### 5. Manager Pattern

System managers with lifecycle:

```python
class HotkeyManager:
    def __init__(self, config):
        self.config = config

    def register(self, callback):
        # Registration logic
        pass

    def cleanup(self):
        # Cleanup logic
        pass
```

### 6. Resource Management

Use context managers for safe resource handling:

```python
from src.core.resource_manager import safe_image_open, safe_file_read

with safe_image_open(Path("image.png")) as image:
    # Use image
    pass

with safe_file_read(Path("file.txt")) as content:
    # Use content
    pass
```

---

## 🚫 Anti-Patterns to Avoid

### 1. ❌ Code Duplication

- **NEVER** duplicate methods across files
- If a method is needed in multiple places, create a shared service/component
- **Example**: Hotkey display logic exists ONLY in `SettingsView`, not in `app.py`

### 2. ❌ Local Imports

```python
# ❌ Wrong
def some_method():
    from src.core.service import function  # Local import

# ✅ Correct
from src.core.service import function  # Top-level import

def some_method():
    function()
```

### 3. ❌ Dead Code

- Remove unused methods/variables immediately
- Use Ruff to detect automatically
- **Current status**: `app.py` reduced from 778 to 367 lines ✅

### 4. ❌ Tight Coupling

- Use event bus for communication
- Pass dependencies via constructor, not global imports
- **Example**: `SettingsView` receives `hotkey_manager` and `window_manager` via constructor

### 5. ❌ Direct Config Access

```python
# ❌ Wrong
from src.core.config import config  # Global access

# ✅ Correct
self.state.config  # Through state
```

### 6. ❌ Magic Strings

- Always use enums for constants
- **Example**: `EventType.LANGUAGE_CHANGED` instead of `"language_changed"`

### 7. ❌ Mixed Responsibilities

- One file = one responsibility
- **Example**: `app.py` handles app lifecycle, `SettingsView` handles settings UI

---

## 📊 Code Quality Metrics

### Current Standards

| Metric               | Target   | Status   |
| -------------------- | -------- | -------- |
| Pyright errors       | 0        | ✅       |
| Ruff errors          | 0        | ✅       |
| Main app lines       | ~400-450 | ✅ (367) |
| Type coverage        | 100%     | ✅       |
| Translation coverage | 100%     | ✅       |

### Monitoring

- **Pyright**: Run before every commit
- **Ruff**: Run before every commit
- **Line count**: Monitor main files
- **Test coverage**: Maintain >80%

---

## 🔄 Refactoring Guidelines

### When to Refactor

1. Code duplication detected
2. Method exceeds 50 lines
3. File exceeds 500 lines
4. More than 3 levels of nesting
5. Mixed responsibilities

### Refactoring Process

1. **Analyze**: Use `list_code_definition_names` and `search_files`
2. **Plan**: Create new structure in separate files
3. **Move**: Use `replace_in_file` to move code
4. **Clean**: Remove old code and dead imports
5. **Verify**: Run quality checks
6. **Test**: Ensure functionality unchanged

### Example: Extracting to View

```python
# Before: 500+ lines in app.py
# After: app.py (300 lines) + settings_view.py (200 lines)
```

---

## 📝 Documentation Standards

### Required Documentation

1. **README.md**: Project overview and quick start
2. **ARCHITECTURE.md**: High-level architecture
3. **docs/CODING_GUIDELINES.md**: This file
4. **docs/REFACTORING_PLAN.md**: Refactoring history
5. **docs/CLEANUP_TASKS.md**: Post-refactoring cleanup

### Documentation Updates

- Update docs when architecture changes
- Keep examples current
- Remove obsolete documentation
- Document new patterns/tools

---

## 🎯 AI Assistant Guidelines

### When AI Assists This Project

#### ✅ DO:

1. **Use existing patterns**: Check how similar things are done
2. **Run quality checks**: Always run ruff and pyright
3. **Respect structure**: Follow the project architecture
4. **Use event bus**: For component communication
5. **Use error handler**: For all error handling
6. **Use translation function**: For all user-facing text
7. **Remove dead code**: Clean up after refactoring
8. **Update documentation**: Keep docs current

#### ❌ DON'T:

1. **Create local imports**: Always top-level imports
2. **Duplicate code**: Extract to shared components
3. **Ignore type hints**: Always use proper typing
4. **Skip quality checks**: Run ruff/pyright
5. **Use global variables**: Use state management
6. **Mix concerns**: One file = one responsibility
7. **Forget translations**: All UI text must be translatable

### AI Workflow Checklist

- [ ] Read relevant files first
- [ ] Check existing patterns
- [ ] Plan refactoring approach
- [ ] Create new files if needed
- [ ] Move code carefully
- [ ] Remove old code
- [ ] Run quality checks
- [ ] Update documentation
- [ ] Test functionality

---

## 🔍 Quality Assurance

### Pre-Commit Checklist

- [ ] Ruff format & lint passed
- [ ] Pyright type check passed
- [ ] No dead code
- [ ] No local imports
- [ ] All strings translatable
- [ ] Documentation updated
- [ ] Tests passing

### Code Review Points

1. **Structure**: Follows project architecture?
2. **Quality**: Passes all checks?
3. **Patterns**: Uses established patterns?
4. **Error handling**: Proper error reporting?
5. **Logging**: Appropriate log messages?
6. **Comments**: Clear English comments?
7. **Types**: Full type coverage?

---

## 📚 Additional Resources

### Internal Documentation

- `docs/01_GETTING_STARTED.md` - Setup guide
- `docs/02_DEVELOPMENT.md` - Development guide
- `docs/03_BUILD_SYSTEM.md` - Build process
- `docs/04_LOGGING.md` - Logging details
- `docs/05_TRANSLATION.md` - Translation system
- `docs/06_SYSTRAY.md` - System tray features
- `docs/08_CONFIGURATION.md` - Configuration details
- `docs/11_TESTING.md` - Testing guide
- `docs/ERROR_HANDLING.md` - Error handling patterns

### External Resources

- [Flet Documentation](https://flet.dev/docs/)
- [Loguru Documentation](https://loguru.readthedocs.io/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## 🎯 Success Criteria

A well-maintained project should have:

- ✅ Zero linting errors
- ✅ Zero type errors
- ✅ Clear architecture
- ✅ Comprehensive documentation
- ✅ Consistent patterns
- ✅ Test coverage
- ✅ No dead code
- ✅ Proper error handling
- ✅ Full internationalization
- ✅ Maintainable code size

_Last Updated: 2026-01-05_
_Version: 1.1.0_
_Project: Writing Assistant Pro_
