#!/usr/bin/env python3
"""
Writing Assistant Pro - Final Build Script
Cross-platform final release build with environment setup
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Fix for Windows console encoding (emojis)
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass

# Import utilities
from utils import (
    PYINSTALLER_EXCLUSIONS,
    BuildTimer,
    check_data,
    clear_console,
    copy_required_files,
    get_executable_name,
    get_project_root,
    terminate_existing_processes,
)

# Configuration
DEFAULT_SCRIPT_NAME = "main.py"
MODE = "build-final"


def copy_required_files_production() -> bool:
    """Copy required files for final release build to dist/production/"""
    return copy_required_files("production", "production")


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

    # Clean dist/production
    dist_prod_dir = Path("dist/production")
    if dist_prod_dir.exists():
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

    # Build icon path
    icon_path = Path("src/config/icons/app_icon.ico")

    # Build PyInstaller command with exclusions - use UV
    pyinstaller_command = [
        "uv",
        "run",
        "-m",
        "PyInstaller",
        "--windowed",  # No console
        f"--icon={icon_path}",
        "--name=Writing Assistant Pro",
        "--distpath=dist/production",
        "--clean",
        "--noconfirm",
        "--collect-all",
        "flet",  # Flet assets
        DEFAULT_SCRIPT_NAME,
    ]

    # Add exclusions
    for module in PYINSTALLER_EXCLUSIONS:
        pyinstaller_command.extend(["--exclude-module", module])

    try:
        print("Starting PyInstaller final build...")
        subprocess.run(pyinstaller_command, check=True)
        print("PyInstaller final build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed: {e}")
        return False


def main():
    """Main function"""
    clear_console()
    print("===== Writing Assistant Pro - Final Release Build =====")
    print()

    timer = BuildTimer()
    timer.start()

    try:
        get_project_root()

        # Clean build directories
        clean_build_directories()

        # Copy required files
        if not copy_required_files_production():
            print("\nFailed to copy required files!")
            return 1

        # Stop existing processes
        print("Terminating existing processes...")
        terminate_existing_processes(exe_name=get_executable_name())

        check_data(MODE)

        # Run build
        if not run_build_final():
            print("\nBuild failed!")
            return 1

        print("\n===== Final release build completed =====")
        print("The executable and required files are in the 'dist/production' directory.")

        timer.print_duration("final release build")

        return 0

    except KeyboardInterrupt:
        print(f"\n{MODE} cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nUnexpected error in {MODE}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
