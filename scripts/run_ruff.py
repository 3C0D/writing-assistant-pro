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
    try:
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

    except KeyboardInterrupt:
        print("\n⏹️  Script interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"💥 An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
