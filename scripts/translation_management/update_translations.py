#!/usr/bin/env python3
"""
Update translations using Babel (gettext)

Usage:
    uv run python scripts/translation_management/update_translations.py

This script automates the complete translation workflow:
1. Extract translatable strings from source code
2. Update/initialize translation files (.po)
3. Compile to binary format (.mo)
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


def run_command(cmd, description, project_root):
    """Execute a command and handle errors"""
    print(f"\n{'=' * 70}")
    print(f"▶️  {description}")
    print(f"{'=' * 70}\n")

    result = subprocess.run(cmd, shell=True, cwd=str(project_root))

    if result.returncode != 0:
        print(f"\n❌ Error during: {description}")
        sys.exit(1)

    print(f"\n✅ {description} - OK\n")


def main():
    """Main workflow"""
    project_root = Path(__file__).parent.parent.parent
    translations_dir = project_root / "translations"
    src_dir = project_root / "src"

    print("\n" + "=" * 70)
    print("🌐 UPDATING TRANSLATIONS WITH BABEL")
    print("=" * 70 + "\n")

    # Step 1: Extract
    extract_cmd = (
        f'uv run pybabel extract -F babel.cfg -k _ -o "{translations_dir}/template.pot" "{src_dir}"'
    )
    run_command(extract_cmd, "🔍 Extracting translatable texts", project_root)

    # Step 2: Update/Initialize languages
    languages = ["en", "fr", "it"]
    domain = "writing_assistant"

    for lang in languages:
        po_file = translations_dir / lang / "LC_MESSAGES" / f"{domain}.po"

        if po_file.exists():
            # Update existing language
            update_cmd = (
                f'uv run pybabel update -d "{translations_dir}" '
                f'-i "{translations_dir}/template.pot" -l {lang} -D {domain}'
            )
            run_command(update_cmd, f"🔄 Updating {lang.upper()} translations", project_root)
        else:
            # Initialize new language
            init_cmd = (
                f'uv run pybabel init -d "{translations_dir}" '
                f'-i "{translations_dir}/template.pot" -l {lang} -D {domain}'
            )
            run_command(init_cmd, f"✨ Initializing {lang.upper()} language", project_root)

    # Step 3: Compile
    compile_cmd = f'uv run pybabel compile -d "{translations_dir}" -D writing_assistant'
    run_command(compile_cmd, "⚙️  Compiling translations (.po → .mo)", project_root)

    print("\n" + "=" * 70)
    print("✅ TRANSLATIONS UPDATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nFiles generated in: {translations_dir}/")
    print("\nNext steps:")
    print("1. Edit .po files to add translations")
    print("2. Run this script again to compile")
    print("3. Restart the application\n")


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
