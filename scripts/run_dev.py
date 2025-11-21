"""
Development script - Launches main.py with --debug argument

Usage:
    uv run python scripts/run_dev.py
"""

import os
import subprocess
import sys
from pathlib import Path

from utils import check_data, copy_required_files

# Fix Unicode encoding for Windows console
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass

# Configuration
DEFAULT_SCRIPT_NAME = "main.py"
MODE = "development"


def main():
    """Launch main.py in debug mode"""
    print(f"🚀 Starting in {MODE} mode...")
    print("─" * 50)

    # Setup development environment
    if not copy_required_files("development", "dev"):
        print("⚠️  Failed to copy required files")

    check_data("build-dev")  # Use build-dev mode to setup data_dev.json path logic

    main_path = Path(__file__).parent.parent / DEFAULT_SCRIPT_NAME
    result = subprocess.run(["uv", "run", "python", str(main_path), "--debug"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
