#!/usr/bin/env python3
"""
Writing Assistant Pro - Final Build Script
Production build with PyInstaller
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
MODE = "build-final"


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

    # Clean dist/prod
    dist_prod_dir = Path("dist/prod")
    if dist_prod_dir.exists():
        # Preserve config.json if it exists
        config_path = dist_prod_dir / "config.json"
        has_config = config_path.exists()
        if has_config:
            try:
                shutil.copy(config_path, "config.json.bak")
                print("Backed up existing config.json")
            except Exception as e:
                print(f"Warning: Could not backup config: {e}")

        try:
            shutil.rmtree(dist_prod_dir)
            print(f"Cleaned: {dist_prod_dir}")
        except Exception as e:
            print(f"Warning: Could not clean {dist_prod_dir}: {e}")

    # Clean .spec files
    for file in Path(".").glob("*.spec"):
        try:
            file.unlink()
            print(f"Cleaned: {file}")
        except Exception as e:
            print(f"Warning: Could not clean {file}: {e}")


def run_build_final() -> bool:
    """Run PyInstaller build for final release"""
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
        "--windowed",
        "--name=Writing Assistant Pro",
        "--distpath=dist/prod",
        "--clean",
        "--noconfirm",
    ]

    # Add NiceGUI data files if found (required for NiceGUI to work)
    if nicegui_path:
        separator = ";" if os.name == "nt" else ":"
        pyinstaller_command.extend(
            [
                "--add-data",
                f"{nicegui_path}{separator}nicegui",
            ]
        )

    # Note: styles, translations, and config.json are NOT included in the exe
    # They are copied to dist/prod/ by copy_required_files()
    # This allows users to modify them without recompiling

    # Add exclusions
    for module in PYINSTALLER_EXCLUSIONS:
        pyinstaller_command.extend(["--exclude-module", module])

    # Add main script
    pyinstaller_command.append(DEFAULT_SCRIPT_NAME)

    try:
        print("Starting PyInstaller final build...")
        subprocess.run(pyinstaller_command, check=True)
        print("PyInstaller final build completed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed with error: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Install with: uv add --dev pyinstaller")
        return False


def main():
    """Main function"""
    clear_console()
    print("===== Writing Assistant Pro - Final Release Build =====")
    print()

    timer = BuildTimer()
    timer.start()

    timer = BuildTimer()
    timer.start()

    try:
        # Ensure we are in the project root
        get_project_root()

        # Clean build directories
        clean_build_directories()

        # Copy required files
        # We pass "prod" as target to copy_required_files
        if not copy_required_files("prod"):
            print("\nFailed to copy required files!")
            return 1

        # Restore backup config if exists
        if Path("config.json.bak").exists():
            try:
                # We overwrite the default config copied by copy_required_files
                shutil.move("config.json.bak", "dist/prod/config.json")
                print("Restored existing configuration.")
            except Exception as e:
                print(f"Warning: Could not restore config: {e}")

        # Stop existing processes
        print("Terminating existing processes...")
        terminate_existing_processes(exe_name=get_executable_name())

        # Run build
        if not run_build_final():
            print("\nBuild failed!")
            return 1

        print("\n===== Final release build completed =====")
        print("The executable and required files are in the 'dist/prod' directory.")

        timer.print_duration("final release build")

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
