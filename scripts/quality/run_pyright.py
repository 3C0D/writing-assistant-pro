"""
Pyright type checking script

Usage:
    uv run python scripts/run_pyright.py

This script runs Pyright to detect type errors in the codebase.
"""

import os
import subprocess
import sys

# Fix for Windows console encoding (emojis)
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
    Run Pyright type checker to detect type errors.
    """
    print("🔍 Running Pyright type checker...")
    print("=" * 70)

    # Run pyright
    result = subprocess.run(
        ["uv", "run", "pyright", "src"],
        capture_output=True,
        text=True,
    )

    # Display output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Check result
    if result.returncode == 0:
        print("=" * 70)
        print("✅ No type errors found!")
        return 0
    else:
        print("=" * 70)
        print("❌ Type errors detected. Please review the output above.")
        return result.returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
