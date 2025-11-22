#!/usr/bin/env python3
"""
Writing Assistant Pro - Icon Converter
Scans PNG icons in assets/icons/ and converts them to ICO format
in assets/icons/icons/ if they don't already exist
"""

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

# Fix for Windows console encoding (emojis)
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass


def convert_png_to_ico(
    png_path: Path,
    ico_path: Path,
    sizes: list[tuple[int, int]] | None = None,
) -> bool:
    """
    Convert a PNG image to ICO format.

    Args:
        png_path: Path to the source PNG file
        ico_path: Path to the output ICO file
        sizes: List of icon sizes to include (default: [(256, 256)])

    Returns:
        True if conversion succeeded, False otherwise
    """
    if not png_path.exists():
        print(f"❌ Source PNG not found: {png_path}")
        return False

    if sizes is None:
        sizes = [(256, 256)]

    try:
        print(f"🔄 Converting {png_path.name} → {ico_path.name}...")
        img = Image.open(png_path)
        img.save(ico_path, format="ICO", sizes=sizes)
        print(f"   ✓ Saved to: {ico_path.relative_to(Path.cwd())}")
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False


def main():
    """Scan PNG files and convert missing ICO files"""
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    # Define directories
    source_dir = project_root / "assets" / "icons"
    target_dir = source_dir / "icons"

    print("===== Writing Assistant Pro - Icon Converter =====")
    print()
    print(f"Source directory: {source_dir.relative_to(project_root)}")
    print(f"Target directory: {target_dir.relative_to(project_root)}")
    print()

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Find all PNG files in source directory (not recursive)
    png_files = list(source_dir.glob("*.png"))

    if not png_files:
        print("⚠️  No PNG files found in source directory")
        return 0

    print(f"Found {len(png_files)} PNG file(s):")
    for png_file in png_files:
        print(f"  - {png_file.name}")
    print()

    # Process each PNG file
    converted_count = 0
    skipped_count = 0
    failed_count = 0

    for png_path in png_files:
        # Determine corresponding ICO path
        ico_path = target_dir / png_path.with_suffix(".ico").name

        # Check if ICO already exists
        if ico_path.exists():
            print(f"⏭️  Skipping {png_path.name} (ICO already exists)")
            skipped_count += 1
            continue

        # Convert PNG to ICO
        if convert_png_to_ico(png_path, ico_path, sizes=[(256, 256)]):
            converted_count += 1
        else:
            failed_count += 1

    # Print summary
    print()
    print("=" * 50)
    print("Summary:")
    print(f"  ✓ Converted: {converted_count}")
    print(f"  ⏭️  Skipped:   {skipped_count}")
    if failed_count > 0:
        print(f"  ❌ Failed:    {failed_count}")
    print("=" * 50)

    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
