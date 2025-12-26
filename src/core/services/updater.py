"""Update checking service using GitHub Releases API"""

from __future__ import annotations

import requests
from loguru import logger
from packaging import version

from src.version import __version__

logger = logger.bind(name="WritingAssistant.Services.Updater")

# GitHub repository configuration
GITHUB_REPO = "3C0D/writing-assistant-pro"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def check_for_updates() -> dict[str, str | bool]:
    """
    Check if new version available on GitHub releases.

    Returns:
        Dictionary with:
        - "available": bool - True if update is available
        - "version": str - Latest version number (if available)
        - "url": str - GitHub release page URL (if available)
        - "notes": str - Release notes excerpt (if available)
        - "error": str - Error message (if error occurred)
    """
    try:
        logger.info(f"Checking for updates (current: {__version__})...")
        response = requests.get(GITHUB_API, timeout=5)
        response.raise_for_status()

        latest = response.json()
        latest_version = latest["tag_name"].lstrip("v")

        logger.debug(f"Latest version on GitHub: {latest_version}")

        if version.parse(latest_version) > version.parse(__version__):
            logger.info(f"Update available: {latest_version} > {__version__}")
            return {
                "available": True,
                "version": latest_version,
                "url": latest["html_url"],
                "notes": latest.get("body", "")[:300],  # Truncate
            }

        logger.info("Already up to date")
        return {"available": False}

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to check for updates: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error checking updates: {e}")
        return {"error": str(e)}
