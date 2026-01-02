"""
Autostart Manager for Writing Assistant Pro

Manages the autostart functionality for Writing Assistant Pro.
Handles setting/removing autostart entries on Windows and Linux.
Synchronizes autostart state with application settings.
"""

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from ..error_handler import ConfigError, handle_error

# Bind logger for this module/static manager
logger = logger.bind(name="WritingAssistant.AutostartManager")

if TYPE_CHECKING:
    from ..config.manager import ConfigManager

try:
    if sys.platform.startswith("win32"):
        import winreg
    else:
        winreg = None
except ImportError:
    winreg = None


class AutostartManager:
    """
    Manages the autostart functionality for Writing Assistant Pro.
    Handles setting/removing autostart entries on Windows and Linux.
    Synchronizes autostart state with application settings.
    """

    # Constants
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    REGISTRY_KEY_COMPILED = "WritingAssistantPro"
    REGISTRY_KEY_DEV = "WritingAssistantProDevStartup"
    DESKTOP_FILE_NAME = "writing-assistant-pro.desktop"

    DESKTOP_ENTRY_TEMPLATE = """[Desktop Entry]
Type=Application
Name=Writing Assistant Pro
Comment=Writing Assistant Pro Application
Exec={exec_path}
Icon=writing-assistant-pro
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
Hidden=false
"""

    @staticmethod
    def is_compiled() -> bool:
        """
        Check if we're running from a compiled exe or source.
        """
        return hasattr(sys, "frozen") and hasattr(sys, "_MEIPASS")

    @staticmethod
    def get_startup_path() -> str | None:
        """
        Get the path that should be used for autostart.
        Returns None if running from source.
        """
        compiled = AutostartManager.is_compiled()

        if not compiled:
            # For development, we don't typically autostart the script directly
            # unless via a wrapper, but for now we return None or handle in get_startup_command
            return None

        return sys.executable

    @staticmethod
    def get_linux_autostart_dir() -> Path:
        """
        Get the autostart directory for Linux systems.
        Usually ~/.config/autostart/
        """
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            config_dir = Path(xdg_config_home)
        else:
            config_dir = Path.home() / ".config"

        autostart_dir = config_dir / "autostart"
        return autostart_dir

    @staticmethod
    def get_linux_desktop_file_path() -> Path:
        """
        Get the path for the desktop entry file on Linux.
        """
        autostart_dir = AutostartManager.get_linux_autostart_dir()
        return autostart_dir / AutostartManager.DESKTOP_FILE_NAME

    @staticmethod
    def _ensure_windows_registry_available() -> bool:
        """
        Check if Windows registry is available.
        """
        if winreg is None:
            logger.warning("Windows registry module not available")
            return False
        return True

    @staticmethod
    def _disable_windows_startup_entry(key_name: str) -> bool:
        """
        Disable a Windows startup entry by name.
        """
        if not AutostartManager._ensure_windows_registry_available():
            return True

        assert winreg is not None

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AutostartManager.REGISTRY_PATH,
                0,
                winreg.KEY_WRITE,
            ) as key:
                try:
                    winreg.DeleteValue(key, key_name)
                    logger.info(f"Disabled {key_name} startup entry")
                    return True
                except OSError:
                    # Value doesn't exist, that's fine
                    return True
        except Exception as e:
            logger.warning(f"Could not disable {key_name}: {e}")
            return False

    @staticmethod
    def disable_dev_startup_if_exists() -> bool:
        return AutostartManager._disable_windows_startup_entry(AutostartManager.REGISTRY_KEY_DEV)

    @staticmethod
    def disable_normal_startup_if_exists() -> bool:
        return AutostartManager._disable_windows_startup_entry(
            AutostartManager.REGISTRY_KEY_COMPILED
        )

    @staticmethod
    def get_dev_startup_command() -> str:
        """
        Get the command for development startup using UV.
        """
        project_root = Path(__file__).parent.parent.parent
        # Adjust this command to match how you want to launch in dev mode
        # For now, we'll use python main.py
        python_exe = sys.executable
        main_script = project_root / "main.py"
        command = f'"{python_exe}" "{main_script}"'
        return command

    @staticmethod
    def get_startup_command() -> str | None:
        """
        Get the command/path for autostart.
        Returns the exe path if compiled, or the dev command if in dev mode.
        """
        compiled = AutostartManager.is_compiled()
        if compiled:
            return AutostartManager.get_startup_path()
        else:
            return AutostartManager.get_dev_startup_command()

    @staticmethod
    def set_autostart_windows(enable: bool) -> bool:
        """
        Enable or disable autostart for Windows.
        """
        if not AutostartManager._ensure_windows_registry_available():
            return False

        assert winreg is not None

        try:
            command = AutostartManager.get_startup_command()
            if not command:
                logger.warning("Cannot determine startup command")
                return False

            compiled = AutostartManager.is_compiled()
            key_name = (
                AutostartManager.REGISTRY_KEY_COMPILED
                if compiled
                else AutostartManager.REGISTRY_KEY_DEV
            )

            if compiled:
                AutostartManager.disable_dev_startup_if_exists()
            else:
                AutostartManager.disable_normal_startup_if_exists()

            try:
                if enable:
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        AutostartManager.REGISTRY_PATH,
                        0,
                        winreg.KEY_WRITE,
                    )
                    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, command)
                    winreg.CloseKey(key)
                else:
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        AutostartManager.REGISTRY_PATH,
                        0,
                        winreg.KEY_WRITE,
                    )
                    try:
                        winreg.DeleteValue(key, key_name)
                    except OSError:
                        pass
                    winreg.CloseKey(key)

                logger.info(
                    f"Windows autostart {'enabled' if enable else 'disabled'} "
                    f"({'compiled' if compiled else 'dev'})"
                )
                return True

            except OSError as e:
                logger.exception(f"Failed to modify autostart registry: {e}")
                return False

        except Exception as e:
            logger.exception(f"Error managing Windows autostart: {e}")
            return False

    @staticmethod
    def set_autostart_linux(enable: bool) -> bool:
        """
        Enable or disable autostart for Linux.
        """
        try:
            compiled = AutostartManager.is_compiled()
            desktop_file_path = AutostartManager.get_linux_desktop_file_path()
            autostart_dir = AutostartManager.get_linux_autostart_dir()

            if enable:
                autostart_dir.mkdir(parents=True, exist_ok=True)

                exec_path = AutostartManager.get_startup_command()
                if not exec_path:
                    logger.warning("Cannot determine startup command")
                    return False

                desktop_content = AutostartManager.DESKTOP_ENTRY_TEMPLATE.format(
                    exec_path=exec_path
                )
                desktop_file_path.write_text(desktop_content)
                os.chmod(desktop_file_path, 0o755)

                logger.info(
                    f"Linux autostart enabled: {desktop_file_path} "
                    f"({'compiled' if compiled else 'dev'})"
                )
                return True
            else:
                if desktop_file_path.exists():
                    desktop_file_path.unlink()
                    logger.info(f"Linux autostart disabled: {desktop_file_path}")
                return True

        except Exception as e:
            logger.exception(f"Error managing Linux autostart: {e}")
            return False

    @staticmethod
    def set_autostart(enable: bool) -> bool:
        """
        Enable or disable autostart for Writing Assistant Pro.
        """
        if sys.platform.startswith("win32"):
            return AutostartManager.set_autostart_windows(enable)
        elif sys.platform.startswith("linux"):
            return AutostartManager.set_autostart_linux(enable)
        else:
            logger.warning(f"Autostart not supported on platform: {sys.platform}")
            return False

    @staticmethod
    def check_autostart_windows() -> bool:
        """
        Check if Writing Assistant Pro is set to start automatically on Windows.
        """
        if not AutostartManager._ensure_windows_registry_available():
            return False

        assert winreg is not None

        try:
            compiled = AutostartManager.is_compiled()
            key_name = (
                AutostartManager.REGISTRY_KEY_COMPILED
                if compiled
                else AutostartManager.REGISTRY_KEY_DEV
            )

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    AutostartManager.REGISTRY_PATH,
                    0,
                    winreg.KEY_READ,
                )
                value, _ = winreg.QueryValueEx(key, key_name)
                winreg.CloseKey(key)

                expected_command = AutostartManager.get_startup_command()
                if not expected_command:
                    return False
                return value == expected_command

            except OSError:
                return False

        except Exception as e:
            logger.exception(f"Error checking Windows autostart status: {e}")
            return False

    @staticmethod
    def check_autostart_linux() -> bool:
        """
        Check if Writing Assistant Pro is set to start automatically on Linux.
        """
        try:
            desktop_file_path = AutostartManager.get_linux_desktop_file_path()

            if not desktop_file_path.exists():
                return False

            content = desktop_file_path.read_text()
            expected_command = AutostartManager.get_startup_command()
            if not expected_command:
                return False
            return f"Exec={expected_command}" in content

        except Exception as e:
            logger.exception(f"Error checking Linux autostart status: {e}")
            return False

    @staticmethod
    def check_autostart() -> bool:
        """
        Check if Writing Assistant Pro is set to start automatically.
        """
        if sys.platform.startswith("win32"):
            return AutostartManager.check_autostart_windows()
        elif sys.platform.startswith("linux"):
            return AutostartManager.check_autostart_linux()
        else:
            return False

    @staticmethod
    def _needs_windows_migration() -> bool:
        """
        Check if Windows autostart entries need migration due to mode change.

        Returns:
            bool: True if migration is needed
        """
        try:
            compiled = AutostartManager.is_compiled()
            if not AutostartManager._ensure_windows_registry_available():
                return False

            assert winreg is not None

            # Check if the wrong key exists
            wrong_key = (
                AutostartManager.REGISTRY_KEY_DEV
                if compiled
                else AutostartManager.REGISTRY_KEY_COMPILED
            )
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    AutostartManager.REGISTRY_PATH,
                    0,
                    winreg.KEY_READ,
                ) as key:
                    winreg.QueryValueEx(key, wrong_key)
                    return True  # Wrong key exists, migration needed
            except OSError:
                return False  # Wrong key doesn't exist, no migration needed

        except Exception as e:
            logger.exception(f"Error checking Windows autostart migration need: {e}")
            return False

    @staticmethod
    def _needs_linux_migration() -> bool:
        """
        Check if Linux autostart entries need migration due to mode change.

        Returns:
            bool: True if migration is needed
        """
        try:
            compiled = AutostartManager.is_compiled()
            desktop_file_path = AutostartManager.get_linux_desktop_file_path()
            if not desktop_file_path.exists():
                return False

            content = desktop_file_path.read_text()
            if compiled:
                # In compiled mode, should not have python dev_script
                return "dev_script.py" in content or "main.py" in content
            else:
                # In dev mode, should not have exe path
                startup_path = AutostartManager.get_startup_path()
                if startup_path:
                    return f"Exec={startup_path}" in content
                return False

        except Exception as e:
            logger.exception(f"Error checking Linux autostart migration need: {e}")
            return False

    @staticmethod
    def _needs_autostart_migration() -> bool:
        """
        Check if autostart entries need migration due to mode change.

        Returns:
            bool: True if migration is needed
        """
        if sys.platform.startswith("win32"):
            return AutostartManager._needs_windows_migration()
        elif sys.platform.startswith("linux"):
            return AutostartManager._needs_linux_migration()
        else:
            return False

    # Not used
    @staticmethod
    def sync_with_settings(config_manager: "ConfigManager") -> bool:
        """
        Synchronize autostart state between system and settings.
        Updates settings to match system state if they differ.
        Also handles mode changes (dev <-> compiled) by migrating autostart entries.
        """
        try:
            system_state = AutostartManager.check_autostart()
            # Use .get() to avoid AttributeError if key doesn't exist
            settings_state = config_manager.get("start_on_boot", False)

            # Check if we need to migrate due to mode change
            if settings_state and AutostartManager._needs_autostart_migration():
                logger.info("Autostart mode migration needed, updating system entries")
                # Remove any conflicting entries and set the correct one for current mode
                success = AutostartManager.set_autostart(True)
                if success:
                    system_state = True  # Now it should be enabled
                else:
                    logger.warning("Failed to migrate autostart entry")

            if system_state != settings_state:
                # Update settings to match system state
                config_manager.set("start_on_boot", system_state)
                logger.debug(f"Synchronized start_on_boot setting: {system_state}")

            return True
        except Exception as e:
            handle_error(
                e, error_type=ConfigError, context="sync_with_settings", logger_instance=logger
            )
            return False

    @staticmethod
    def set_autostart_with_sync(enable: bool, config_manager: "ConfigManager") -> bool:
        """
        Set autostart state and synchronize with settings.
        """
        try:
            # Update system autostart
            success = AutostartManager.set_autostart(enable)

            if success:
                # Update settings to match
                config_manager.set("start_on_boot", enable)
                logger.debug(f"Set autostart to {enable} and updated settings")

            return success
        except Exception as e:
            handle_error(
                e, error_type=ConfigError, context="set_autostart_with_sync", logger_instance=logger
            )
            return False
