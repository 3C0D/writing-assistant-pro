"""
Resource Management Module for Writing Assistant Pro

Provides context managers for safe resource handling.
"""

from __future__ import annotations

import io
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from loguru import logger

from .error_handler import handle_error


@contextmanager
def safe_image_open(image_path: Path) -> Generator[Any]:
    """
    Context manager for safely opening and closing PIL images.

    Usage:
        with safe_image_open(Path("image.png")) as image:
            # Use image
            pass
        # Image automatically closed
    """
    from PIL import Image

    image = None
    try:
        image = Image.open(image_path)
        yield image
    except Exception as e:
        handle_error(e, context=f"open_image_{image_path}", logger_instance=logger)
        raise
    finally:
        if image:
            try:
                image.close()
            except Exception:
                pass


@contextmanager
def safe_file_read(file_path: Path, encoding: str = "utf-8") -> Generator[str]:
    """
    Context manager for safely reading files.

    Usage:
        with safe_file_read(Path("file.txt")) as content:
            # Use content
            pass
        # File automatically closed
    """
    try:
        with open(file_path, encoding=encoding) as f:
            content = f.read()
            yield content
    except Exception as e:
        handle_error(e, context=f"read_file_{file_path}", logger_instance=logger)
        raise


@contextmanager
def safe_file_write(file_path: Path, encoding: str = "utf-8") -> Generator[io.TextIOWrapper]:
    """
    Context manager for safely writing to files.

    Usage:
        with safe_file_write(Path("file.txt")) as f:
            f.write("content")
        # File automatically closed and flushed
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding=encoding) as f:
            yield f
    except Exception as e:
        handle_error(e, context=f"write_file_{file_path}", logger_instance=logger)
        raise


@contextmanager
def safe_json_read(file_path: Path) -> Generator[Any]:
    """
    Context manager for safely reading JSON files.

    Usage:
        with safe_json_read(Path("data.json")) as data:
            # Use data
            pass
    """
    import json

    try:
        with safe_file_read(file_path) as content:
            data = json.loads(content)
            yield data
    except Exception as e:
        handle_error(e, context=f"read_json_{file_path}", logger_instance=logger)
        raise


@contextmanager
def safe_json_write(file_path: Path, data: Any, indent: int = 4) -> Generator[None]:
    """
    Context manager for safely writing JSON files.

    Usage:
        with safe_json_write(Path("data.json"), {"key": "value"}):
            pass  # File written and closed
    """
    import json

    try:
        with safe_file_write(file_path) as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        yield
    except Exception as e:
        handle_error(e, context=f"write_json_{file_path}", logger_instance=logger)
        raise


@contextmanager
def temp_working_directory(path: Path) -> Generator[Path]:
    """
    Context manager for temporarily changing working directory.

    Usage:
        with temp_working_directory(Path("/some/path")):
            # Working directory is now /some/path
            pass
        # Working directory restored
    """
    import os

    original_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original_cwd)


class ResourceTracker:
    """
    Track resources and ensure proper cleanup.

    Usage:
        tracker = ResourceTracker()
        tracker.add("file_handle", file_handle, "close")
        # ... use resources
        tracker.cleanup()
    """

    def __init__(self):
        self.resources: dict[str, tuple[Any, str]] = {}
        self.logger = logger.bind(name="WritingAssistant.ResourceTracker")

    def add(self, name: str, resource: Any, cleanup_method: str = "close") -> None:
        """Add a resource to track"""
        self.resources[name] = (resource, cleanup_method)
        self.logger.debug(f"Tracking resource: {name}")

    def cleanup(self) -> None:
        """Clean up all tracked resources"""
        for name, (resource, method) in self.resources.items():
            try:
                cleanup_func = getattr(resource, method, None)
                if cleanup_func:
                    cleanup_func()
                    self.logger.debug(f"Cleaned up resource: {name}")
            except Exception as e:
                handle_error(e, context=f"resource_cleanup_{name}", logger_instance=self.logger)

        self.resources.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False
