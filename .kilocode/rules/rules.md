# Project Development Rules

**Target Platform**: Windows, Linux, and Mac

## Code Language

- **English only**: All code, comments, and documentation must be in English
- **No French**: Variable names, function names, comments, and strings must be English
- **Consistent terminology**: Use standard English terms across the codebase

## Script Execution

- **Always use UV**: Use `uv run python <script_name>` for running any Python script
- **Never use raw Python**: Don't use `python <script>` directly
- **Unicode encoding fix**: When creating new scripts, always add the following code at the beginning to fix Unicode issues on Windows:

  ```python
    # Fix Unicode encoding for Windows console
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if os.name == "nt":
        subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except AttributeError:
        pass
  ```

## File Organization

- **Keep root clean**: Only essential files at project root (main.py, pyproject.toml, README.md, etc.)
- **Use proper directories**:
  - `src/` → Source code (core, ui)
  - `scripts/` → Utilities and tools
  - `tests/` → Test files
  - `translations/` → i18n files
  - `docs/` → Documentation
  - `styles/` → CSS files
- **One concern per module**: Keep UI, core logic, and data in separate modules
- **Refactoring principle**: Share responsibilities between modules, but keep logic quick to understand

## Development Guidelines

- **Modular design**: Maintain clear separation between UI, business logic, and data layers
- **Code clarity**: Choose clarity over cleverness - make code easy to understand
- **Single Responsibility**: Each module should have one clear purpose
- **Test coverage**: Add tests for new functionality
- **Documentation**: Update docs when structure or APIs change
- **Clean commits**: One logical change per commit with clear messages

## Project Structure

- **Follow established patterns**: Use the existing directory structure as a template
- **Consistent naming**: Use snake_case for Python files and functions
- **Import order**:
  1. Standard library
  2. Third-party packages
  3. Local application modules

## Code Quality

- **Regular reviews**: Check code organization periodically
- **Prevent technical debt**: Apply these rules consistently
- **Update dependencies**: Keep packages current and secure
- **Maintain tests**: Ensure all new code has appropriate test coverage
- **Code linting**: Run `uv run python scripts/run_ruff.py` at the end of each code modification to check and correct automatically
- **Application testing**: To check if the application works after modifications, run `uv run python scripts/run_dev.py`

---

**Why these rules matter**: They prevent technical debt, ensure consistent practices, and make the codebase easy for new developers to understand.
