import sys
from pathlib import Path

import pytest

# Add project root to python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_config_file(tmp_path):
    """
    Fixture to provide a temporary config file path.
    This ensures tests don't mess with the real config.json.
    """
    # Create a path in the temporary directory
    config_path = tmp_path / "test_config.json"

    # Yield the path to the test (this is where the test runs)
    yield config_path
