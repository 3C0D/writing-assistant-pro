# Ruff Setup Guide

## Overview

Ruff is a fast Python linter and code formatter that serves as a drop-in replacement for tools like Flake8, isort, and Black. It provides comprehensive code quality checks and formatting capabilities with significantly better performance.

## What's Already Configured

Your project includes the complete Ruff setup:

- **Python Package**: `ruff` is listed as a dependency in `pyproject.toml`
- **Project Configuration**: Ruff rules and settings are configured in `pyproject.toml`
- **VSCode Extension**: Extension settings are configured in `.vscode/settings.json`
- **VSCode Task**: Ready-to-use VSCode task "Run Ruff" configured in `.vscode/tasks.json`
- **Pre-commit Hooks**: Automated Ruff checks on git commits configured in `.pre-commit-config.yaml`
- **Script**: Ready-to-use script for running Ruff on the entire project

## Four Ways to Use Ruff

### 1. **VSCode Extension (Per-File Automatic)**

**What it does:**
- Runs automatically when you save a Python file
- Checks and fixes only the current file being edited
- Provides real-time feedback with error squiggles in the editor
- Organizes imports and fixes formatting on save

**Required Extension:**
- Install **"Ruff"** by Charlie Marsh (charliermarsh.ruff) in VSCode
- Extension ID: `charliermarsh.ruff`

**What it installs:**
- The extension itself
- Automatically downloads the Ruff binary for your platform
- No additional setup required

**How it works:**
- Configuration is read from `pyproject.toml` in your project
- Uses the same rules as the script method
- Runs: `ruff check --fix <current_file>` on save
- Also runs: `ruff format <current_file>` if format on save is enabled

**Current Settings in .vscode/settings.json:**
```json
{
    "ruff.enable": true,
    "ruff.organizeImports": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    }
}
```

### 2. **VSCode Task (All Files Comprehensive)**

**What it does:**
- Checks and fixes ALL Python files in the project
- Provides comprehensive project-wide linting report
- Best for final checks before commits or releases
- Shows complete summary of all issues found

**How to use:**

**Option A: VSCode Task (Recommended)**
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Tasks: Run Task" and select "Run Ruff"
- Or use keyboard shortcut `Ctrl+Shift+P` → "Run Ruff"

**Option B: Terminal Command**
```bash
uv run python scripts/run_ruff.py
```

**What it does:**
- Scans all Python files in the `src/` directory
- Applies all Ruff rules from `pyproject.toml`
- Shows detailed output with file paths and line numbers
- Applies automatic fixes where possible

**Example output:**
```
Checking all Python files...
src/core/app.py:15:1: F401 Unused import `os`
src/ui/interface.py:42:5: E501 Line too long (101 > 100 characters)
src/utils/helpers.py:23:9: B006 Do not use mutable defaults as function arguments

Found 3 errors.
```

### 3. **Pre-commit Hooks (Automatic Git Integration)**

**What it does:**
- Automatically runs Ruff checks when you create git commits
- Prevents commits that don't pass Ruff quality checks
- Applies automatic fixes when possible
- Ensures code quality standards across the entire team

**How to set up:**
1. The `.pre-commit-config.yaml` file is already created in your project root
2. Install pre-commit: `uv run pre-commit install`
3. Ruff will now run automatically on every commit

**What it runs:**
- `ruff check --fix` - Linting with automatic fixes
- `ruff format` - Code formatting
- Both tools run on all staged Python files

**Configuration in `.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**Benefits:**
- 🚫 **Prevents bad code**: Stops commits that fail quality checks
- 🔄 **Automatic fixes**: Applies style corrections automatically
- 👥 **Team consistency**: Ensures everyone follows the same standards
- 🔍 **Zero friction**: Runs transparently in the background

### 4. **Terminal Script (All Files Comprehensive)**

**What it does:**
- Identical to VSCode Task but executed directly in terminal
- Checks and fixes ALL Python files in the project
- Provides comprehensive project-wide linting report

**How to use:**
```bash
cd /path/to/project
uv run python scripts/run_ruff.py
```

**Advantages:**
- Complete control over execution
- Accessible from any terminal
- Easy integration with CI/CD scripts

## Current Ruff Configuration

Your project has these rules enabled in `pyproject.toml`:

### Linting Rules
- **E**: pycodestyle errors - Basic Python style violations
- **W**: pycodestyle warnings - Less critical style issues  
- **F**: Pyflakes - Logical errors and unused imports/variables
- **I**: isort - Import sorting and organization
- **UP**: pyupgrade - Automatic Python syntax upgrades
- **B**: flake8-bugbear - Additional bug and design pattern detection
- **C4**: flake8-comprehensions - Comprehension improvements

### Formatting Rules
- **Line length**: 100 characters
- **Target Python version**: 3.13 (updated from 3.11)
- **Quotes**: Double quotes
- **Indentation**: Spaces
- **Line ending**: Auto (platform-specific)

### Excluded Rules
- **None**: All configured rules are now active (previously E501 was excluded)

## Which Method to Use When?

### Use **Pre-commit Hooks** when:
- 🚫 **Preventing bad commits**: Automatically block commits that fail quality checks
- 🔄 **Automatic fixes**: Apply style corrections without manual intervention  
- 👥 **Team enforcement**: Ensure consistent code quality across all team members
- 🔍 **Background safety**: Run checks transparently during normal git workflow

### Use **VSCode Extension** when:
- ✏️ **Writing code**: Get immediate feedback as you type
- 💾 **Saving files**: Automatic fixes and formatting on save
- 🔍 **Debugging**: See issues highlighted directly in the editor
- 🎯 **Quick fixes**: Fix one file at a time during development

### Use **VSCode Task** when:
- 📋 **Full project review**: Check entire codebase before commits
- 📊 **Comprehensive reporting**: Get complete overview of all issues
- 🏁 **Final checks**: Verify code quality before releases
- 🔧 **Bulk fixes**: Apply fixes to multiple files simultaneously

### Use **Terminal Script** when:
- 🤖 **CI/CD integration**: Automation in pipelines
- 🔄 **Custom scripts**: Integration with other tools
- 📊 **Programmatic analysis**: Processing by other scripts

## What Ruff Does

### 1. Linting
- Identifies potential bugs and logical errors
- Enforces Python style conventions (PEP 8)
- Catches common mistakes and anti-patterns

### 2. Import Sorting
- Organizes imports according to PEP 8
- Groups standard library, third-party, and local imports
- Removes unused imports automatically

### 3. Code Formatting
- Applies consistent formatting rules
- Fixes indentation and spacing issues
- Normalizes quote styles and line breaks

### 4. Auto-fixes
- Automatically corrects fixable issues
- No manual intervention required for style fixes
- Safe, deterministic transformations

## Modifying Rules

To add or modify Ruff rules, edit the `[tool.ruff.lint]` section in `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "C4", "B"]  # Add new rule codes here
ignore = []  # Currently all rules are active
```

### Recommended Additional Rules

Consider enabling these rule categories for enhanced code quality:

```toml
select = ["E", "W", "F", "I", "UP", "C4", "B", "D", "N", "S", "T10", "SIM", "ERA", "PD", "RUF"]
```

**Benefits:**
- **D**: Documentation string conventions
- **N**: Naming conventions enforcement
- **S**: Security vulnerability detection
- **T10**: Debug statement prevention
- **SIM**: Code simplification suggestions
- **ERA**: Dead code removal
- **PD**: Pandas-specific best practices
- **RUF**: Ruff-specific advanced checks

## Tips for Best Results

1. **Keep VSCode extension active** for immediate feedback
2. **Set up pre-commit hooks** for automatic quality checks on commits
3. **Run VSCode task before commits** for comprehensive checks
4. **Use consistent Python version** (3.13+ as configured)
5. **Review auto-fixes** to ensure they don't break functionality
6. **Configure editor rulers** for visual line length guidance (already set: 88 and 120 characters)

## Troubleshooting

### Extension Not Working?
1. Ensure the "Ruff" extension is installed and enabled
2. Restart VSCode after installation
3. Check that `ruff` is available in your Python environment
4. Verify `pyproject.toml` exists and is valid

### Pre-commit Hooks Not Running?
1. Ensure you've installed pre-commit: `uv run pre-commit install`
2. Check that `.pre-commit-config.yaml` exists in project root
3. Verify git repository is initialized
4. Test manually: `uv run pre-commit run --all-files`

### Script Not Found?
1. Ensure you're in the project root directory
2. Check that `scripts/run_ruff.py` exists
3. Run with `uv run python scripts/run_ruff.py` (not plain `python`)

### Configuration Not Applied?
1. Ensure rules are added to `[tool.ruff.lint]` section in `pyproject.toml`
2. Verify syntax of the TOML file
3. Restart VSCode after configuration changes
