"""
Ruff linting and formatting script

Usage:
    uv run python scripts/run_ruff.py

This script runs Ruff commands sequentially to fix and format code:
1. Check and auto-fix issues
2. Format code
3. Final verification
"""

import os
import subprocess
import sys

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
    """
    Run ruff commands sequentially to fix and format code.
    """
    # Run ruff check with --fix to automatically fix issues
    print("🔍 Running ruff check --fix...")
    result_check_fix = subprocess.run(["uv", "run", "ruff", "check", "--fix", "."], text=True)
    if result_check_fix.returncode != 0:
        print("❌ Error during ruff check --fix")
        sys.exit(1)

    # Run ruff format to format the code
    print("✨ Running ruff format...")
    result_format = subprocess.run(["uv", "run", "ruff", "format", "."], text=True)
    if result_format.returncode != 0:
        print("❌ Error during ruff format")
        sys.exit(1)

    # Run final ruff check to verify everything is correct
    print("🔎 Running final ruff check...")
    result_check_final = subprocess.run(
        ["uv", "run", "ruff", "check", "."], capture_output=True, text=True
    )
    if result_check_final.returncode != 0:
        print("⚠️  Manual fixes required:")
        print(result_check_final.stdout)
        sys.exit(1)

    print("✅ Ruff corrections and formatting completed successfully.")


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
