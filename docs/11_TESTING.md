# Automated Tests

## 📋 Overview

The project uses **pytest** for unit and integration tests. Tests ensure the stability of critical components like configuration, translation, state management, and event bus.

## 🎯 Goals

- Validate proper functioning of modules (Core & UI)
- Prevent regressions during refactoring
- Document expected behavior through tests
- Ensure resource safety and error handling

## 🏗️ Architecture

### `tests/` Directory (Unit & Integration Tests)

```
tests/
├── conftest.py              # Shared fixtures (temp config, etc.)
├── test_config.py           # Configuration and persistence
├── test_error_handler.py    # Standardized error handling
├── test_event_bus.py        # Inter-module communication (Pub/Sub)
├── test_resource_manager.py # Context managers and ResourceTracker
└── test_state.py            # Centralized state management (AppState/UIState)
```

### `scripts/tests/` Directory (Utility Scripts)

- `test_crash.py` : Special script to verify crashes are properly logged.

## 🚀 Running Tests

### From Visual Studio Code (Recommended)

**Using the integrated Test Explorer:**

1. **Open Explorer** : Click the arrow icon in the left sidebar (or `Ctrl+Shift+P` → "Testing: Focus on Test Explorer View")

2. **`tests/` Directory** :
   - You'll see all test files in `tests/`
   - Click ▶️ to run **all tests in the directory**
   - Click a specific test to run it individually
   - ✅ Green = passed, ❌ Red = failed

3. **"Run with coverage" Option** :
   - If VSC prompts to install `pytest-cov`, it's **optional**
   - **Without coverage** : Just runs tests (recommended for starters)
   - **With coverage** : Shows what % of code is tested (useful for improving tests)

**Advantages:**
- ✅ Clear visual interface
- ✅ See results immediately
- ✅ Run single test or all at once
- ✅ No command line needed

### Command Line

**All unit tests:**
```bash
uv run pytest tests/
```

**Specific file:**
```bash
uv run pytest tests/test_state.py
```

**Specific test:**
```bash
uv run pytest tests/test_config.py::test_config_defaults
```

**With detailed logs:**
```bash
uv run pytest -v -s
```

**Ignoring crash test:**
```bash
uv run pytest --ignore=scripts/tests/test_crash.py
```

### Crash Test (Special)

The crash test in `scripts/tests/test_crash.py` is **outside the `tests/` directory** because it's a utility script that verifies critical errors are properly logged.

**To run it:**
```bash
uv run python scripts/tests/test_crash.py
```

**Or via VSC task** : If you have tasks configured in `.vscode/tasks.json`

**Why separate?**
- It's a system integration test, not a unit test
- It creates a real crash to verify logging system
- It shouldn't pollute unit test results

## 📝 Logging in Tests

We use **loguru** for logging. In tests, you can verify logged messages if needed, but `pytest` generally captures standard output.

To specifically test crashes:

```bash
uv run python scripts/tests/test_crash.py
```

Then check `logs/crash_run_dev.log` to confirm the error was captured.

## 📝 Writing Tests

### Test Structure (AAA Pattern)

```python
def test_toggle_sidebar():
    # 1. Arrange
    from src.core import AppState
    state = AppState()

    # 2. Act
    state.update_ui_state(sidebar_visible=True)

    # 3. Assert
    assert state.ui_state.sidebar_visible is True
```

### Using Fixtures

Fixtures help create isolated test environments. Refer to `tests/conftest.py` for available fixtures (mock config, files, etc.).

## 🧪 Key Tests After Refactoring

### State Management (`test_state.py`)

Verifies that `AppState` and `UIState` maintain a single source of truth.

### Event Bus (`test_event_bus.py`)

Verifies that components can communicate decoupled via `emit` and `on`.

### Error Handler (`test_error_handler.py`)

Verifies that exceptions are properly captured, logged, and handled via `safe_execute` or `ErrorContext`.

## ⚠️ Best Practices

1. **Isolation** : Use `AppState` locally in tests rather than global bus when possible.
2. **Cleanup** : Use `ResourceTracker` or context managers to leave no temporary files.
3. **Clear assertions** : Use explicit messages in your assertions.
4. **Type Checking** : Always run `uv run python scripts/quality/run_pyright.py` after modifying tests.

## 🔗 References

- [pytest Documentation](https://docs.pytest.org/)
- [Loguru Documentation](https://github.com/Delgan/loguru)
