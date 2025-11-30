#!/usr/bin/env python3
"""
Create GitHub release and upload assets from dist/production.

Prerequisites:
- GitHub CLI installed: `gh auth login`
- Assets built in dist/production/
- CHANGELOG.md present at project root (optional)

Usage:
    uv run python scripts/create_release.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Fix for Windows console encoding (emojis)
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass


def get_version() -> str:
    """Read version from src/version.py"""
    version_file = Path(__file__).parent.parent / "src" / "version.py"
    with open(version_file, encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    raise ValueError("Could not find __version__ in src/version.py")


def create_release():
    """Create GitHub release with assets from dist/production"""
    # Get version from source
    version_str = get_version()
    tag = f"v{version_str}"

    print(f"📦 Creating release for version {version_str}")

    # Verify dist/production exists and has files
    dist_path = Path(__file__).parent.parent / "dist" / "production"
    if not dist_path.exists():
        print("❌ Error: dist/production/ not found")
        print("   Please build the production executable first")
        sys.exit(1)

    assets = [f for f in dist_path.glob("*") if f.is_file()]
    if not assets:
        print("❌ Error: No assets found in dist/production/")
        sys.exit(1)

    print(f"📋 Found {len(assets)} asset(s):")
    for asset in assets:
        print(f"   - {asset.name}")

    # Create git tag
    print(f"\n🏷️  Creating and pushing tag {tag}...")
    try:
        subprocess.run(
            ["git", "tag", "-a", tag, "-m", f"Release {version_str}"],
            check=True,
        )
        subprocess.run(["git", "push", "origin", tag], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git tag creation failed: {e}")
        print("   Tag might already exist. Delete it first if needed:")
        print(f"   git tag -d {tag}")
        print(f"   git push origin :refs/tags/{tag}")
        sys.exit(1)

    # Create GitHub release using gh CLI
    print("\n🚀 Creating GitHub release...")

    # Build command
    cmd = [
        "gh",
        "release",
        "create",
        tag,
        "--title",
        f"Release {version_str}",
    ]

    # Add changelog if it exists
    changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
    if changelog_path.exists():
        cmd.extend(["--notes-file", str(changelog_path)])
    else:
        cmd.extend(["--notes", f"Release {version_str}"])

    # Add all files from dist/production as assets
    for asset in assets:
        cmd.append(str(asset))

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Release {tag} created with {len(assets)} asset(s)")
        print(f"   View at: https://github.com/3C0D/writing-assistant-pro/releases/tag/{tag}")
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub release creation failed: {e}")
        print("   Make sure GitHub CLI is authenticated: gh auth login")
        sys.exit(1)


if __name__ == "__main__":
    create_release()
