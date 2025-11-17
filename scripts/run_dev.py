"""
Development script - Launches main.py with --debug argument

Usage:
    uv run python scripts/run_dev.py
"""

import os
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


def main():
    """Launch main.py in debug mode"""
    print("🚀 Starting in DEV mode...")
    print("─" * 50)

    main_path = Path(__file__).parent.parent / "main.py"
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
