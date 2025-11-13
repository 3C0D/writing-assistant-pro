# Ruff Setup Guide

## Overview

Ruff is a fast Python linter and code formatter that serves as a drop-in replacement for tools like Flake8, isort, and Black. It provides comprehensive code quality checks and formatting capabilities with significantly better performance.

## How to Run Ruff

To run Ruff on this project, execute the dedicated script:

```bash
uv run python scripts/run_ruff.py
```

This script is configured to check all Python files in the project and apply the current Ruff configuration from `pyproject.toml`.

## What Ruff Does

Ruff performs multiple code quality checks simultaneously:

- **Linting**: Identifies potential bugs, style violations, and code smells
- **Import sorting**: Organizes import statements according to PEP 8
- **Code formatting**: Applies consistent formatting rules (using `--fix`)
- **Error detection**: Catches syntax errors and logical issues

## Output Explanation

When running Ruff, you'll see output in the terminal showing:

- File paths being checked
- Specific rule violations with error codes
- Line and column numbers for each issue
- Descriptions of what needs to be fixed

Example output:

```
src/core/app.py:15:1: F401 Unused import `os`
src/ui/interface.py:42:5: E501 Line too long (89 > 88 characters)
Found 2 errors.
```

## Current Rules Enabled

The project currently enables the following rule categories in `pyproject.toml`:

- **E**: pycodestyle errors - Basic Python style violations (indentation, line length, etc.)
- **W**: pycodestyle warnings - Less critical style issues
- **F**: Pyflakes - Logical errors and unused imports/variables
- **I**: isort - Import sorting and organization
- **UP**: pyupgrade - Automatic Python syntax upgrades (e.g., f-strings, type hints)
- **B**: flake8-bugbear - Additional bug and design problem detection
- **C4**: flake8-comprehensions - Comprehension-related improvements

### Rule Categories Utility

- **E/W**: Ensure consistent code style and readability
- **F**: Prevent common bugs from unused code
- **I**: Maintain organized import statements
- **UP**: Modernize code to use newer Python features
- **B**: Catch subtle bugs and anti-patterns
- **C4**: Optimize list/dict comprehensions for better performance

## Modifying pyproject.toml

To add or modify Ruff rules, edit the `[tool.ruff]` section in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
select = ["E", "W", "F", "I", "UP", "B", "C4"]  # Add new rule codes here
ignore = ["E501"]  # Exclude specific rules if needed

[tool.ruff.isort]
known-first-party = ["src"]
```

### Adding New Rules

To enable additional rules, add their codes to the `select` array. For example, to add pydocstyle documentation checks:

```toml
select = ["E", "W", "F", "I", "UP", "B", "C4", "D"]
```

## Suggested Future Rules

Consider enabling these additional rule categories for enhanced code quality:

- **D**: pydocstyle - Documentation string conventions
- **N**: pep8-naming - Enforce naming conventions (snake_case, CamelCase)
- **S**: flake8-bandit - Security vulnerability detection
- **T10**: flake8-debugger - Prevent debug statements in production
- **SIM**: flake8-simplify - Simplify complex code patterns
- **ERA**: eradicate - Remove commented-out code
- **PD**: pandas-vet - Pandas-specific best practices (if using pandas)
- **RUF**: Ruff-specific rules - Additional Ruff-developed checks

Each category provides specific benefits:

- **D**: Ensures comprehensive documentation
- **N**: Maintains consistent naming across the codebase
- **S**: Identifies potential security issues
- **T10**: Prevents accidental debug code commits
- **SIM**: Simplifies overly complex expressions
- **ERA**: Keeps code clean by removing dead code
- **PD**: Optimizes pandas usage patterns
- **RUF**: Catches additional code quality issues
