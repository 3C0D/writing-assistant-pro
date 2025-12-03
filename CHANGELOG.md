## v1.2.0 (2025-12-03)

### Feat

- Add i18n translation system documentation, development and build guides, and a UI design system file, updating the architecture.

## v1.1.0 (2025-12-03)

### Feat

- Add VS Code tasks for development and document the multi-OS release process.
- Add release workflow, commitizen integration, and initial project documentation structure.

## v1.0.0 (2025-12-02)

### BREAKING CHANGE

- Replace logging.getLogger() with logger.bind() from loguru across all modules. Update hotkey from ctrl+space to ctrl+. in configuration and user documentation.
- Requires watchdog>=6.0.0 dependency
- Removed pynput dependency - applications must use keyboard library for hotkeys
- Module imports have changed due to restructuring (e.g., from styles import -> from src.core.styles import)

### Feat

- add update checking mechanism and internationalization support with new update service, UI, and translation files
- Add system tray management, PyInstaller file, and update .gitignore.
- add initial UI application structure, design system, core components, and development documentation.
- Implement initial Flet UI structure with design system, application, sidebar, and navigation components.
- Add complete project documentation and remove config.json.
- Add pre-commit documentation and adjust hook steps to avoid unstaged files
- Configure pre-commit hooks for push and add associated documentation and VS Code settings.
- Introduce core components for hotkey, systray, autostart, and app lifecycle management.
- Implement Flet UI and add translation debugging tools
- introduce Flet UI, system tray, app icon, and initial internationalization setup
- introduce Flet UI framework with initial app structure and core services, including config, logging, window, and hotkey management.
- Add build scripts and Flet UI components with core modules.
- Initialize application structure, add build scripts, and configure development environment.
- Add main application structure and build/packaging scripts.
- Implement initial UI structure with header, main interface, theme styles, and style documentation.
- Implement core application architecture, UI structure, configuration management, and development tooling.
- **styles**: add CSS hot reload functionality with watchdog integration
- **ui**: add hidden window with global hotkey support

### Fix

- correct line length violation in build_dev.py

### Refactor

- **core**: migrate from standard logging to loguru and update hotkey to ctrl+.
- **ui**: enhance header with background color and button z-index Add blue background to header and ensure hide button appears on top with z-index styling.
- **core**: extract window configuration to window manager
- **core**: move startup window hide logic to window manager and adjust hotkey interval
- **core**: convert hotkey management to class-based system
- **core**: move hotkey setup to delayed function and update linting config
- **core**: refactor window startup and management logic
- **ui**: extract UI components into separate modules
- **core**: convert HotkeyManager class to setup_hotkey function
- **core**: extract window and hotkey management into separate modules
- **core**: simplify logging configuration in app initialization
- **core**: restructure app by moving main class to core module
- **deps**: move webview import to top-level and remove conditional imports
- consolidate codebase with window management improvements and English standardization
- **core**: consolidate imports through main src.core module
- **core**: restructure project layout and add internationalization support
