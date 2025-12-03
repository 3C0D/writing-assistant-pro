# Commitizen Workflow Guide

## Overview

This project uses Commitizen to enforce Conventional Commits and automate version bumping and changelog generation.

**References:**

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) - Best practices for changelogs

## Daily Workflow

### Option 1: Using VS Code Git UI (Recommended)

1. Stage your changes in VS Code
2. Write your commit message manually following Conventional Commits format:

   - `feat: add new feature` - New feature (bumps MINOR version)
   - `fix: correct bug` - Bug fix (bumps PATCH version)
   - `docs: update documentation` - Documentation only
   - `style: format code` - Code style changes
   - `refactor: restructure code` - Code refactoring
   - `test: add tests` - Adding tests
   - `chore: update deps` - Maintenance tasks

3. Commit using the VS Code button
4. The pre-commit hook will validate your message format

### Option 2: Using Commitizen Interactive Prompt

1. Stage your changes
2. Run the task "Commitizen: Create Commit" from VS Code Command Palette
3. Follow the interactive prompts
4. Commitizen will create a properly formatted commit

## Creating a Release

When you're ready to create a new version:

1. **Run the Bump Version task:**

   - Open Command Palette (Ctrl+Shift+P)
   - Select "Tasks: Run Task"
   - Choose "Commitizen: Bump Version"

2. **What happens automatically:**

   - Analyzes all commits since last version
   - Calculates new version based on commit types:
     - `feat:` commits → MINOR version bump (1.0.0 → 1.1.0)
     - `fix:` commits → PATCH version bump (1.0.0 → 1.0.1)
     - `BREAKING CHANGE:` → MAJOR version bump (1.0.0 → 2.0.0)
   - Updates:
     - `src/version.py` (`__version__`)
     - `pyproject.toml` (project version)
     - `pyproject.toml` (tool.commitizen.version)
   - Generates/updates `CHANGELOG.md`
   - Creates a commit: `bump: version X.Y.Z → A.B.C`
   - Creates a Git tag: `A.B.C`

3. **Push the tag to trigger release:**

   ```powershell
   git push origin --tags
   ```

   **💡 Tip:** You can auto-push tags during bump:

   ```powershell
   uv run cz bump --changelog --push
   ```

4. **GitHub Actions automatically:**
   - Builds the production executable
   - Creates a zip of `dist/production/`
   - Creates a GitHub Release with:
     - The zip file attached
     - Release notes from CHANGELOG

## Conventional Commits Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Common Examples

```bash
# Feature (MINOR bump)
feat: add keyboard shortcut customization

# Bug fix (PATCH bump)
fix: resolve systray icon not showing in production

# Breaking change (MAJOR bump) - Method 1: exclamation mark
feat!: redesign settings UI

# Breaking change (MAJOR bump) - Method 2: footer
feat: redesign settings UI

BREAKING CHANGE: Settings structure has changed

# Note: Adding ! after the type triggers a MAJOR version bump
# You can use it with any type: feat!, fix!, refactor!, etc.
```

### Types Reference

| Type       | Description      | Version Bump |
| ---------- | ---------------- | ------------ |
| `feat`     | New feature      | MINOR        |
| `fix`      | Bug fix          | PATCH        |
| `docs`     | Documentation    | none         |
| `style`    | Formatting       | none         |
| `refactor` | Code restructure | none         |
| `test`     | Tests            | none         |
| `chore`    | Maintenance      | none         |
| `perf`     | Performance      | PATCH        |
| `ci`       | CI/CD changes    | none         |

## Manual Version Bump

If you need to manually bump to a specific version:

```powershell
# Bump to specific version
uv run cz bump --increment MAJOR  # 1.0.0 → 2.0.0
uv run cz bump --increment MINOR  # 1.0.0 → 1.1.0
uv run cz bump --increment PATCH  # 1.0.0 → 1.0.1

# Or specify exact version
uv run cz bump --version 2.5.0

# Auto-push tags after bump
uv run cz bump --changelog --push
```

## Troubleshooting

### Pre-commit hook rejects my commit

Your commit message doesn't follow Conventional Commits format. Examples:

❌ Bad:

```
Updated the config file
```

✅ Good:

```
chore: update config file
```

### Version not updating in all files

Check `pyproject.toml` `[tool.commitizen]` configuration. Ensure `version_files` includes all necessary files.

### Tag already exists

If a tag already exists, delete it locally and remotely:

```powershell
# Delete local tag
git tag -d 1.0.0

# Delete remote tag
git push origin --delete 1.0.0

# Try bump again
uv run cz bump
```

## Using LLM to Generate Commit Messages

If you use an LLM assistant in VS Code (like GitHub Copilot Chat or similar), you can use this prompt:

```
Generate a conventional commit message for the following changes.
Use this format: <type>[optional scope]: <description>

Types:
- feat: new feature (MINOR version bump)
- fix: bug fix (PATCH version bump)
- docs: documentation only
- style: formatting, no code change
- refactor: code restructure
- test: adding tests
- chore: maintenance
- perf: performance improvement (PATCH version bump)

For breaking changes, add ! after type (e.g., feat!: ...) or add "BREAKING CHANGE:" in footer.

Changes:
[Paste your git diff or describe your changes here]

Provide only the commit message, nothing else.
```

**Example usage:**

1. Copy your staged changes or describe what you did
2. Paste the prompt to your LLM
3. Get a properly formatted commit message
4. Use it in VS Code Git UI
