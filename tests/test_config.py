from src.core.config import ConfigManager


def test_config_defaults(temp_config_file):
    """Test that ConfigManager loads default values."""
    # Initialize with our temporary file
    config = ConfigManager(config_file=str(temp_config_file))

    assert config.LANGUAGE == "fr"
    assert config.DEBUG is False
    assert config.WINDOW_SIZE == [800, 600]


def test_config_persistence(temp_config_file):
    """Test that values are saved and reloaded."""
    # 1. Create config and change a value
    config1 = ConfigManager(config_file=str(temp_config_file))
    config1.DARK_MODE = True

    # 2. Create a new instance pointing to the same file
    config2 = ConfigManager(config_file=str(temp_config_file))

    # 3. Verify the value persisted
    assert config2.DARK_MODE is True


def test_config_attribute_access(temp_config_file):
    """Test attribute-style access."""
    config = ConfigManager(config_file=str(temp_config_file))

    # Test getting
    assert config.get("language") == "fr"
    assert config.LANGUAGE == "fr"

    # Test setting
    config.DEBUG = True
    assert config.get("debug") is True
