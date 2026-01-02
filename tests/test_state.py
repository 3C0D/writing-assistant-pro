"""Tests for state management module"""

from src.core import AppState, ConfigManager, UIState
from src.core.services.input_source import InputState


def test_ui_state_defaults():
    """Test UIState default values"""
    ui_state = UIState()

    assert ui_state.sidebar_visible is False
    assert ui_state.settings_visible is False
    assert ui_state.dark_mode is True
    assert ui_state.language == "fr"


def test_ui_state_update():
    """Test UIState update method"""
    ui_state = UIState()

    ui_state.sidebar_visible = True
    ui_state.settings_visible = True

    assert ui_state.sidebar_visible is True
    assert ui_state.settings_visible is True


def test_app_state_defaults():
    """Test AppState default values"""
    state = AppState(
        config=ConfigManager(),
        input_state=InputState(),
        ui_state=UIState(),
        attachments=[],
    )

    assert state.config is not None
    assert state.input_state is not None
    assert state.ui_state is not None
    assert state.attachments == []


def test_app_state_update_config():
    """Test AppState config update"""
    state = AppState(
        config=ConfigManager(),
        input_state=InputState(),
        ui_state=UIState(),
        attachments=[],
    )

    # Mock config update
    state.config.set("test_key", "test_value")

    assert state.config.get("test_key") == "test_value"


def test_app_state_ui_update():
    """Test AppState UI state update"""
    state = AppState(
        config=ConfigManager(),
        input_state=InputState(),
        ui_state=UIState(),
        attachments=[],
    )

    state.update_ui_state(sidebar_visible=True, settings_visible=True)

    assert state.ui_state.sidebar_visible is True
    assert state.ui_state.settings_visible is True


def test_app_state_attachments():
    """Test AppState attachment management"""
    state = AppState(
        config=ConfigManager(),
        input_state=InputState(),
        ui_state=UIState(),
        attachments=[],
    )

    # Add attachment
    class MockAttachment:
        def __init__(self, id, content):
            self.id = id
            self.content = content

    att1 = MockAttachment("att1", "content1")
    att2 = MockAttachment("att2", "content2")

    state.add_attachment(att1)
    state.add_attachment(att2)

    assert len(state.attachments) == 2

    # Remove attachment
    state.remove_attachment("att1")
    assert len(state.attachments) == 1
    assert state.attachments[0].id == "att2"

    # Clear attachments
    state.clear_attachments()
    assert len(state.attachments) == 0
