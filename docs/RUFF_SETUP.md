# Ruff Setup Guide

## What is Ruff?

Ruff is a fast Python linter and formatter that replaces tools like Black, Flake8, and isort.

It does two things:

- **Format**: Visual style (indentation, spaces, quotes)
- **Check**: Code errors (unused imports, bugs, style violations)

## How to use Ruff in this project

### 1. VSCode Extension (everyday use)

**What it does:**

- Formats code automatically
- Organizes imports when you press **Ctrl+S manually** (not on auto-save)
- Shows errors in real-time with red squiggles

**Setup:**

1. Install extension: "Ruff" by Charlie Marsh (`charliermarsh.ruff`)
2. Already configured in `.vscode/settings.json`

**That's it.** Just code normally and press Ctrl+S.

---

### 2. VSCode Task (before commits)

**What it does:**

- Checks ALL Python files in `src/`
- Shows all errors and fixes them automatically
- Use before committing to verify entire project

**How to run:**

- `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Ruff"

**Command:** `uv run ruff check src/ --fix`

---

### 3. Pre-commit Hook (automatic checks)

**What it does:**

- Runs Ruff automatically before each git commit
- Blocks commits if code doesn't pass checks
- Applies automatic fixes

**Setup:**

1. Add `pre-commit` to dependencies in `pyproject.toml`
2. Run: `uv sync`
3. Run once: `uv run pre-commit install`. This sets up the pre-commit hook git in your repository

**After setup:** Just commit normally. Ruff runs automatically.

---

## Current Configuration

Located in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "C4", "B"]
ignore = []
```

**What these rules check:**

- **E/W**: Python style (PEP 8)
- **F**: Logical errors, unused imports/variables
- **I**: Import organization
- **UP**: Python syntax upgrades
- **C4**: Better comprehensions
- **B**: Bug patterns

**Line length**: 100 characters (enforced)

---

## When to use what?

| Situation | Method | When |
|-----------|--------|------|
| **Writing code** | VSCode Extension | Always active |
| **Before commit** | VSCode Task | Manual check |
| **Git commit** | Pre-commit hook | Automatic |

---

## Troubleshooting

**Extension not working?**

- Check extension is installed: "Ruff" by Charlie Marsh
- Restart VSCode

**Pre-commit not running?**

- Run: `uv run pre-commit install`
- Check `.pre-commit-config.yaml` exists

**Task not found?**

- `Ctrl+Shift+P` → "Tasks: Run Task"
- Check `.vscode/tasks.json` has "Run Ruff" task

---

## Optional: Add more rules

To enable additional checks, edit `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "C4", "B", "D", "N", "S"]
```

**Additional rules:**

- **D**: Docstring conventions
- **N**: Naming conventions
- **S**: Security issues

Restart VSCode after changes.
