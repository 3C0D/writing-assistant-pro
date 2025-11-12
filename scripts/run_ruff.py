import subprocess
import sys


def main():
    """
    Run ruff commands sequentially to fix and format code.
    """
    try:
        # Run ruff check with --fix to automatically fix issues
        result_check_fix = subprocess.run(
            ["uv", "run", "ruff", "check", "--fix", "."], capture_output=True, text=True
        )
        if result_check_fix.returncode != 0:
            print("Error during ruff check --fix:")
            print(result_check_fix.stderr)
            sys.exit(1)

        # Run ruff format to format the code
        result_format = subprocess.run(
            ["uv", "run", "ruff", "format", "."], capture_output=True, text=True
        )
        if result_format.returncode != 0:
            print("Error during ruff format:")
            print(result_format.stderr)
            sys.exit(1)

        # Run final ruff check to verify everything is correct
        result_check_final = subprocess.run(
            ["uv", "run", "ruff", "check", "."], capture_output=True, text=True
        )
        if result_check_final.returncode != 0:
            print("Error during final ruff check:")
            print(result_check_final.stderr)
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
