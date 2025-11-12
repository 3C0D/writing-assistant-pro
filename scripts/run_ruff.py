import subprocess
import sys


def main():
    """
    Run ruff commands sequentially to fix and format code.
    """
    try:
        # Run ruff check with --fix to automatically fix issues
        print("Running ruff check --fix...")
        result_check_fix = subprocess.run(["uv", "run", "ruff", "check", "--fix", "."], text=True)
        if result_check_fix.returncode != 0:
            print("Error during ruff check --fix")
            sys.exit(1)

        # Run ruff format to format the code
        print("Running ruff format...")
        result_format = subprocess.run(["uv", "run", "ruff", "format", "."], text=True)
        if result_format.returncode != 0:
            print("Error during ruff format")
            sys.exit(1)

        # Run final ruff check to verify everything is correct
        print("Running final ruff check...")
        result_check_final = subprocess.run(["uv", "run", "ruff", "check", "."], text=True)
        if result_check_final.returncode != 0:
            print("Error during final ruff check")
            sys.exit(1)

        print("Ruff corrections and formatting completed successfully.")

    except KeyboardInterrupt:
        print("Script interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
