#!/usr/bin/env python3
"""
Writing Assistant Pro - Dev Build Script
Development build with PyInstaller (Console Mode)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Fix Unicode encoding for Windows console
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass

from utils import (
    PYINSTALLER_EXCLUSIONS,
    BuildTimer,
    clear_console,
    copy_required_files,
    get_executable_name,
    get_project_root,
    terminate_existing_processes,
)

# Configuration
DEFAULT_SCRIPT_NAME = "main.py"
MODE = "build-dev"


def clean_build_directories() -> None:
    """Clean build directories for a fresh build"""
    print("Cleaning build directories...")

    directories_to_clean = [Path("build"), Path("__pycache__")]
    for directory in directories_to_clean:
        if directory.exists():
            try:
                shutil.rmtree(directory)
                print(f"Cleaned: {directory}")
            except Exception as e:
                print(f"Warning: Could not clean {directory}: {e}")

    # Clean dist/dev
    dist_dev_dir = Path("dist/dev")
    if dist_dev_dir.exists():
        # In dev mode, we might want to keep config, but usually dev build is for testing
        # Let's keep it simple and clean everything for now, or preserve config if needed
        # User note: "Initially the DEV folder shares the same data for both
        # build DEV mode and standard dev mode"
        # So we should probably NOT delete the whole dir if it contains the shared config.
        # But for a clean build, we usually want to clean.
        # Let's clean but we will ensure config is preserved/copied back if we were smart,
        # but here we will just rely on copy_required_files to restore default config if missing.
        # Actually, if dev mode shares config, deleting it might lose dev settings.
        # Let's try to preserve config.json if it exists.

        config_path = dist_dev_dir / "config.json"
        has_config = config_path.exists()
        if has_config:
            # Backup config
            try:
                shutil.copy(config_path, "config.json.bak")
            except Exception:
                pass

        try:
            shutil.rmtree(dist_dev_dir)
            print(f"Cleaned: {dist_dev_dir}")
        except Exception as e:
            print(f"Warning: Could not clean {dist_dev_dir}: {e}")

        # Restore config if we backed it up (or just let copy_required_files handle it)
        # If we want to share config with "dev" mode (source), maybe we shouldn't delete it?
        # But PyInstaller needs a clean target usually.
        pass

    # Clean .spec files
    for file in Path(".").glob("*.spec"):
        try:
            file.unlink()
            print(f"Cleaned: {file}")
        except Exception as e:
            print(f"Warning: Could not clean {file}: {e}")


def run_build_dev() -> bool:
    """Run PyInstaller build for dev release"""
    # Find NiceGUI package location
    try:
        import nicegui

        nicegui_path = Path(nicegui.__file__).parent
        print(f"Found NiceGUI at: {nicegui_path}")
    except ImportError:
        print("Warning: Could not find NiceGUI package")
        nicegui_path = None

    # Build PyInstaller command with exclusions - use UV
    # Use onedir mode (default) instead of onefile to avoid NiceGUI runpy bug
    pyinstaller_command = [
        "uv",
        "run",
        "-m",
        "PyInstaller",
        "--console",  # Console mode for dev
        "--name=Writing Assistant Pro",
        "--distpath=dist/dev",
        "--clean",
        "--noconfirm",
    ]

    # Add NiceGUI data files if found
    if nicegui_path:
        separator = ";" if os.name == "nt" else ":"
        pyinstaller_command.extend(
            [
                "--add-data",
                f"{nicegui_path}{separator}nicegui",
            ]
        )

    # Add exclusions
    for module in PYINSTALLER_EXCLUSIONS:
        pyinstaller_command.extend(["--exclude-module", module])

    # Add main script
    pyinstaller_command.append(DEFAULT_SCRIPT_NAME)

    try:
        print("Starting PyInstaller dev build...")
        subprocess.run(pyinstaller_command, check=True)
        print("PyInstaller dev build completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed with error: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Install with: uv add --dev pyinstaller")
        return False


def launch_build(extra_args: list[str] | None = None) -> bool:
    """Launch the built executable."""
    exe_name = get_executable_name()
    # In onedir mode, exe is in dist/dev/Writing Assistant Pro/<exe_name>
    exe_path = Path("dist") / "dev" / "Writing Assistant Pro" / exe_name

    if not exe_path.exists():
        print(f"Error: Built executable not found at {exe_path}")
        return False

    # Build command with extra arguments
    cmd = [str(exe_path)]
    if extra_args:
        cmd.extend(extra_args)

    print(f"Launching {exe_path}...")
    try:
        # Use subprocess.run to launch and wait for the executable
        # This keeps the console open and shows the app output
        if sys.platform.startswith("win"):
            subprocess.run(cmd, shell=False)
        else:
            subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"Error launching executable: {e}")
        return False


def main():
    """Main function"""
    clear_console()
    print("===== Writing Assistant Pro - Dev Build (Console) =====")
    print()

    timer = BuildTimer()
    timer.start()

    try:
        # Ensure we are in the project root
        get_project_root()

        # Clean build directories
        clean_build_directories()

        # Copy required files
        # We pass "dev" as target to copy_required_files
        if not copy_required_files("dev"):
            print("\nFailed to copy required files!")
            return 1

        # Restore backup config if exists
        if Path("config.json.bak").exists():
            shutil.move("config.json.bak", "dist/dev/config.json")
            print("Restored existing configuration.")

        # Stop existing processes
        print("Terminating existing processes...")
        terminate_existing_processes(exe_name=get_executable_name())

        # Run build
        if not run_build_dev():
            print("\nBuild failed!")
            return 1

        print("\n===== Dev build completed =====")
        print("The executable and required files are in the 'dist/dev' directory.")

        # Launch the built application
        print()
        if not launch_build():
            print("\nFailed to launch built application!")
            return 1

        timer.print_duration("dev build")

        return 0

    except KeyboardInterrupt:
        print(f"\n{MODE} cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nUnexpected error in {MODE}: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
