#!/usr/bin/env python3
"""
Writing Assistant Pro - Build Utilities
Common functions shared across build and launch scripts
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory"""
    script_dir = Path(__file__).parent  # scripts/
    project_root = script_dir.parent  # project root
    os.chdir(project_root)
    return project_root


def ensure_icon_exists() -> Path | None:
    """
    Get the icon path from assets/icons/app_icon.png.
    PyInstaller supports PNG icons on all platforms.
    """
    project_root = get_project_root()
    png_path = project_root / "assets" / "icons" / "app_icon.png"

    if not png_path.exists():
        print(f"❌ Icon not found at {png_path}")
        return None

    print(f"✓ Icon found at: {png_path}")
    return png_path


def check_data(mode: str) -> None:
    """
    Checks data file path to provide feedback to the user based on build mode.
    Implements the logic:
    - build-dev -> dist/dev/data_dev.json
    - build-final -> dist/production/data.json
    """

    if mode == "build-final":
        print("Setting up production settings...")
        dist_dir = Path("dist/production")
        data_filename = "data.json"
        settings_type = "production"
    else:  # build-dev
        print("Setting up development settings...")
        dist_dir = Path("dist/dev")
        data_filename = "data_dev.json"
        settings_type = "development"

    data_path = dist_dir / data_filename
    cwd = Path(".")

    if data_path.exists():
        print(f"Using existing {settings_type} settings from: {cwd / data_path}")
    else:
        print(
            f"No existing {settings_type} settings found. "
            "Application will create settings on first run."
        )
        print(f"Settings will be saved to: {cwd / data_path}")


def clear_console() -> None:
    """Clear console screen (cross-platform)"""
    os.system("cls" if os.name == "nt" else "clear")


def copy_required_files(build_type: str, target_dir: str) -> bool:
    """
    Copy required files for build to the specified target directory.

    Args:
        build_type (str): Type of build ('development' or 'production')
        target_dir (str): Target directory name (e.g., 'dev', 'production')
    """
    # Create target directory
    dist_target_dir = Path(f"dist/{target_dir}")
    dist_target_dir.mkdir(parents=True, exist_ok=True)
    cwd = Path(".")

    # Only copy what actually exists in the CURRENT project structure
    # We do NOT copy legacy assets from src/config if they don't exist
    items_to_copy = [
        (Path("styles"), dist_target_dir / "styles"),
        (Path("translations"), dist_target_dir / "translations"),
        (Path("src/core/config.json"), dist_target_dir / "config.json"),
        (Path("assets/icons"), dist_target_dir / "assets/icons"),
    ]

    print(f"Copying required files for {build_type} build to {cwd}/dist/{target_dir}/...")

    for src, dst in items_to_copy:
        try:
            if not src.exists():
                # config.json might not exist yet, that's fine
                if src.name == "config.json":
                    continue
                print(f"Warning: File/directory not found: {src}")
                continue

            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        except Exception as e:
            print(f"Error copying {src}: {e}")
            return False

    # Log logic reminder
    if build_type == "development":
        print("Note: build-dev mode - settings will be saved to dist/dev/data_dev.json")
    else:  # production
        print("Note: final-dev mode - settings will be saved to dist/production/data.json")

    return True


def get_executable_name(base_name: str = "Writing Assistant Pro") -> str:
    """Get the correct executable name for the current platform"""
    if sys.platform.startswith("win"):
        return f"{base_name}.exe"
    return base_name


def kill_existing_exe_process(process_name: str) -> None:
    """Terminate an existing process by its name."""
    try:
        if sys.platform.startswith("win"):
            command = ["taskkill", "/F", "/IM", process_name]
            result = subprocess.run(command, check=False, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Terminated existing process: {process_name}")
            elif "not found" in result.stderr.lower() or "cannot find" in result.stderr.lower():
                print(f"No existing process found for: {process_name}")
        else:
            command = ["pkill", "-x", process_name]
            result = subprocess.run(command, check=False, capture_output=True)
            if result.returncode == 0:
                print(f"Terminated existing process: {process_name}")
    except Exception as e:
        print(f"Warning: Error while trying to kill process {process_name}: {e}")


def kill_python_script_process(script_name: str) -> None:
    """Terminate a Python script process by its command line."""
    try:
        if sys.platform.startswith("win"):
            # Method 1: Use tasklist + taskkill for more reliable process detection
            # First, get the list of processes with command lines
            list_command = [
                "wmic",
                "process",
                "where",
                f"name='python.exe' and commandline like '%{script_name}%'",
                "get",
                "processid",
                "/format:value",
            ]

            result = subprocess.run(list_command, check=False, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout:
                # Extract process IDs
                pids = []
                for line in result.stdout.split("\n"):
                    if line.startswith("ProcessId=") and line.strip() != "ProcessId=":
                        pid = line.split("=")[1].strip()
                        if pid:
                            pids.append(pid)

                if pids:
                    # Kill each process by PID
                    killed_count = 0
                    for pid in pids:
                        kill_cmd = ["taskkill", "/F", "/PID", pid]
                        kill_result = subprocess.run(
                            kill_cmd, check=False, capture_output=True, text=True
                        )
                        if kill_result.returncode == 0:
                            killed_count += 1

                    if killed_count > 0:
                        print(
                            f"Successfully terminated {killed_count} Python process(es) "
                            f"running: {script_name}"
                        )
                    else:
                        print(
                            f"Found Python processes for {script_name} but failed to terminate them"
                        )
                else:
                    print(f"No existing Python process found for: {script_name}")
            else:
                print(f"No existing Python process found for: {script_name}")

        else:
            # For macOS and Linux, use more precise matching
            # Use pgrep to find processes first, then pkill
            grep_command = ["pgrep", "-f", f"python.*{script_name}"]
            result = subprocess.run(grep_command, check=False, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout.strip():
                # Found processes, now kill them
                kill_command = ["pkill", "-f", f"python.*{script_name}"]
                kill_result = subprocess.run(
                    kill_command, check=False, capture_output=True, text=True
                )

                if kill_result.returncode == 0:
                    pids = result.stdout.strip().split("\n")
                    print(
                        f"Successfully terminated {len(pids)} Python process(es) "
                        f"running: {script_name}"
                    )
                else:
                    print(f"Found Python processes for {script_name} but failed to terminate them")
            else:
                print(f"No existing Python process found for: {script_name}")

    except Exception as e:
        print(f"Warning: Error while trying to kill Python script process {script_name}: {e}")


def terminate_existing_processes(
    exe_name: str | None = None, script_name: str | None = None
) -> None:
    """Terminate any existing Writing Assistant Pro processes (both exe and script)"""
    print("Checking for existing processes...")

    # Kill Python script first (to avoid conflicts)
    if script_name:
        print(f"Looking for Python script processes: {script_name}")
        kill_python_script_process(script_name)

    if exe_name:
        print(f"Looking for: {exe_name}")
        kill_existing_exe_process(exe_name)

    time.sleep(0.5)
    print("Process termination check completed.")


class BuildTimer:
    """A simple timer class to measure build duration"""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        print("Build timer started...")

    def stop(self):
        """Stop the timer and return elapsed time"""
        if self.start_time is None:
            return 0.0

        self.end_time = time.time()
        return self.end_time - self.start_time

    def print_duration(self, build_type: str = "build"):
        """Print the build duration in a formatted way"""
        if self.start_time is None:
            return

        if self.end_time is None:
            elapsed = self.stop()
        else:
            elapsed = self.end_time - self.start_time

        if elapsed < 60:
            time_str = f"{elapsed:.1f} seconds"
        elif elapsed < 3600:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} and {seconds:.1f} seconds"
        else:
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = elapsed % 60
            time_str = (
                f"{hours} hour{'s' if hours > 1 else ''}, "
                f"{minutes} minute{'s' if minutes > 1 else ''} and "
                f"{seconds:.1f} seconds"
            )

        print(f"{build_type.capitalize()} completed in {time_str}")


# PyInstaller exclusions
PYINSTALLER_EXCLUSIONS = [
    "tkinter",
    "unittest",
    "IPython",
    "jedi",
    "email_validator",
    "cryptography",
    "psutil",
    "pyzmq",
    "tornado",
    "matplotlib",
    "numpy",
    "pandas",
    "scipy",
]
