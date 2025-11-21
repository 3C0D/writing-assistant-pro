#!/usr/bin/env python3
"""
Writing Assistant Pro - Flet Dev Build Script
Cross-platform development build with environment setup
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
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
    ensure_icon_exists,
    get_executable_name,
    get_project_root,
    terminate_existing_processes,
)

# ===== GLOBAL CONFIGURATION =====
DEFAULT_SCRIPT_NAME = "main.py"
MODE = "build-dev"
CONSOLE_MODE_DEFAULT = True  # True = console visible by default


def copy_required_files_dev() -> bool:
    """Copy required files for the development build to dist/dev/."""
    return copy_required_files("development", "dev")


def clean_dev_cache() -> None:
    """Clean PyInstaller cache and build directories for dev build."""
    print("🧹 Cleaning PyInstaller cache...")

    # Clean build and __pycache__ directories
    directories_to_clean = [Path("build"), Path("__pycache__")]
    for directory in directories_to_clean:
        if directory.exists():
            try:
                shutil.rmtree(directory)
                print(f"   Cleaned: {directory}")
            except Exception as e:
                print(f"   Warning: Could not clean {directory}: {e}")

    # Clean .spec files
    current_dir = Path(".")
    for file in current_dir.glob("*.spec"):
        try:
            file.unlink()
            print(f"   Cleaned: {file}")
        except Exception as e:
            print(f"   Warning: Could not clean {file}: {e}")

    print("   Cache cleanup completed!")


def run_dev_build(console_mode: bool = False, clean_build: bool = False) -> bool:
    """Run PyInstaller build for development"""

    if clean_build:
        print("🧹  Manual clean build requested")
        clean_dev_cache()
        print()

    # Build icon path
    icon_path = ensure_icon_exists()
    if not icon_path:
        print("Error: Icon file not found and could not be generated.")
        return False

    # Build PyInstaller command with exclusions - use UV
    pyinstaller_command = [
        "uv",
        "run",
        "-m",
        "PyInstaller",
        "--onedir",
        "--console" if console_mode else "--windowed",
        f"--icon={icon_path}",
        "--name=Writing Assistant Pro",
        "--distpath=dist/dev",  # Output to dist/dev/
        "--noconfirm",
        "--collect-all",
        "flet",  # Flet assets
    ]

    if clean_build:
        pyinstaller_command.append("--clean")

    # Add exclusions
    for module in PYINSTALLER_EXCLUSIONS:
        pyinstaller_command.extend(["--exclude-module", module])

    # Add main script
    pyinstaller_command.append(f"{DEFAULT_SCRIPT_NAME}")

    try:
        mode_text = "console" if console_mode else "windowed"
        print(f"Starting PyInstaller development build ({mode_text} mode)...")
        subprocess.run(pyinstaller_command, check=True)
        print(f"PyInstaller development build completed successfully ({mode_text} mode)!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed with error: {e}")
        return False
    except FileNotFoundError:
        print("Error: PyInstaller not found. Please install it with: uv add --dev pyinstaller")
        return False


def launch_build(extra_args: list[str] | None = None) -> bool:
    """Launch the built executable, killing any existing instance first."""
    exe_name = get_executable_name()
    exe_path = Path("dist") / "dev" / exe_name

    if not exe_path.exists():
        print(f"Error: Built executable not found at {exe_path}")
        return False

    # Build command with extra arguments
    cmd = [str(exe_path)]
    if extra_args:
        cmd.extend(extra_args)

    print(f"Launching {exe_path} with args: {' '.join(extra_args) if extra_args else 'none'}...")
    try:
        if sys.platform.startswith("win"):
            process = subprocess.Popen(cmd, shell=False)
        else:
            process = subprocess.Popen(cmd)

        # Wait briefly to ensure the process starts
        time.sleep(1)

        # Check if process is still running
        if process.poll() is None:
            print(f"✓ Application launched successfully (PID: {process.pid})")
            return True
        else:
            print(f"❌ Application exited immediately with code: {process.returncode}")
            return False

    except Exception as e:
        print(f"Error launching executable: {e}")
        return False


def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Writing Assistant Pro - Development Build")

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--console",
        action="store_true",
        help="Force console mode (logs visible in real-time)",
    )
    mode_group.add_argument(
        "--windowed",
        action="store_true",
        help="Force windowed mode (logs written to file)",
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Force clean build (clear PyInstaller cache)",
    )

    parser.add_argument(
        "extra_args", nargs="*", help="Extra arguments to pass to the built executable"
    )
    args = parser.parse_args()

    clear_console()
    print("===== Writing Assistant Pro - Development Build =====")
    print()

    timer = BuildTimer()
    timer.start()

    # Determine console mode
    if args.console:
        console_mode = True
        print("🖥️  Console mode forced via --console argument")
    elif args.windowed:
        console_mode = False
        print("🪟  Windowed mode forced via --windowed argument")
    else:
        console_mode = CONSOLE_MODE_DEFAULT
        print(f"⚙️  Using default mode: {'console' if console_mode else 'windowed'}")

    extra_args = args.extra_args or None

    try:
        get_project_root()

        # Copy required files
        if not copy_required_files_dev():
            print("\nFailed to copy required files!")
            return 1

        # Stop existing processes
        print("Terminating existing processes...")
        terminate_existing_processes(
            exe_name=get_executable_name(),
            script_name=DEFAULT_SCRIPT_NAME,
        )

        # Setup development settings
        check_data(MODE)

        # Run build
        if not run_dev_build(console_mode=console_mode, clean_build=args.clean):
            print("\nBuild failed!")
            return 1

        # Move built application files from nested folder to dist/dev
        print("Moving built application to 'dist/dev' directory...")
        source_dir = Path("dist/dev/Writing Assistant Pro")
        target_dir = Path("dist/dev")

        if source_dir.exists():
            for item in source_dir.iterdir():
                target_path = target_dir / item.name

                # Remove if already exists
                if target_path.exists():
                    if target_path.is_dir():
                        shutil.rmtree(target_path)
                    else:
                        target_path.unlink()

                shutil.move(str(item), str(target_path))

            source_dir.rmdir()
        else:
            print(
                f"Warning: Source directory {source_dir} not found. "
                "Build might have failed or structure is different."
            )

        # Kill any processes that might have been started during testing
        print("Terminating existing processes before launch...")
        terminate_existing_processes(
            exe_name=get_executable_name(),
            script_name=DEFAULT_SCRIPT_NAME,
        )

        # Launch the built application
        print()
        if not launch_build(extra_args=extra_args):
            print("\nFailed to launch built application!")
            return 1

        print("\n===== Development build completed and launched =====")
        timer.print_duration("development build")

        return 0

    except KeyboardInterrupt:
        print(f"\n{MODE} cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nUnexpected error in {MODE}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
