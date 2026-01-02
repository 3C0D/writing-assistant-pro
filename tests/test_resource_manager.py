"""Tests for resource manager module"""

import tempfile
from pathlib import Path

from src.core.resource_manager import (
    ResourceTracker,
    safe_file_read,
    safe_file_write,
    safe_json_read,
    safe_json_write,
)


def test_safe_file_read_write():
    """Test safe file reading and writing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.txt"

        # Write
        with safe_file_write(file_path) as f:
            f.write("Hello, World!")

        # Read
        with safe_file_read(file_path) as content:
            assert content == "Hello, World!"


def test_safe_json_read_write():
    """Test safe JSON reading and writing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"

        # Write
        data = {"key": "value", "number": 42}
        with safe_json_write(file_path, data):
            pass

        # Read
        with safe_json_read(file_path) as loaded:
            assert loaded == data


def test_safe_file_read_not_found():
    """Test safe file read with non-existent file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "nonexistent.txt"

        try:
            with safe_file_read(file_path):
                pass
            import pytest

            pytest.fail("Should have raised exception")
        except Exception:
            assert True


def test_resource_tracker():
    """Test ResourceTracker"""

    class MockResource:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    with ResourceTracker() as tracker:
        resource1 = MockResource()
        resource2 = MockResource()

        tracker.add("res1", resource1, "close")
        tracker.add("res2", resource2, "close")

        assert not resource1.closed
        assert not resource2.closed

    # After context exit, resources should be closed
    assert resource1.closed
    assert resource2.closed


def test_resource_tracker_custom_method():
    """Test ResourceTracker with custom cleanup method"""

    class MockResource:
        def __init__(self):
            self.cleaned = False

        def cleanup(self):
            self.cleaned = True

    with ResourceTracker() as tracker:
        resource = MockResource()
        tracker.add("res", resource, "cleanup")

    assert resource.cleaned
