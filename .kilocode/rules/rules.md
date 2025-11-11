# Project Development Rules

## Script Execution

- **Always use UV**: When launching any script, always use `uv run python <script_name>` instead of direct `python` commands
- **Example**: `uv run python scripts/run_dev.py` instead of `python scripts/run_dev.py`
- **Use del for file deletion**: On Windows, use `del <filename>` instead of `rm <filename>` for deleting files

## Code Language

- **English only**: All code and comments must be in English, never in French
- **No French in code**: Variable names, function names, comments, strings must be English

## File Organization

- **Keep root clean**: Only essential files at project root
- **Use proper directories**: src/, tests/, translations/, scripts/, docs/
- **No mixed files**: Don't mix different file types in same directory

## Development Guidelines

- **Modular design**: Keep separation between UI, core logic, and data
- **Test coverage**: Add tests for new functionality
- **Clean commits**: One logical change per commit
- **Documentation**: Update docs when structure changes

## Project Structure Guidelines

- **Use established structure**: Follow the existing project organization
- **Consistent naming**: Use snake_case for Python files
- **Proper imports**: Standard library → Third party → Local modules

## Maintenance

- **Regular organization**: Review and refactor as needed
- **Keep tests updated**: Ensure all new code has appropriate tests
- **Monitor dependencies**: Keep project dependencies current

---

**Remember**: These rules prevent technical debt and ensure consistent development practices.
