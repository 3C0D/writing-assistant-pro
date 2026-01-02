"""Tests for event bus module"""

from src.core.event_bus import EventBus


def test_event_bus_subscribe_unsubscribe():
    """Test subscribing and unsubscribing to events"""
    bus = EventBus()

    callback_called = []

    def callback(data):
        callback_called.append(data)

    # Subscribe
    bus.on("test_event", callback)
    assert len(bus._listeners["test_event"]) == 1

    # Emit
    bus.emit("test_event", "test_data")
    assert callback_called == ["test_data"]

    # Unsubscribe
    bus.off("test_event", callback)
    assert len(bus._listeners["test_event"]) == 0


def test_event_bus_multiple_listeners():
    """Test multiple listeners for same event"""
    bus = EventBus()

    results = []

    def callback1(data):
        results.append(f"callback1: {data}")

    def callback2(data):
        results.append(f"callback2: {data}")

    bus.on("multi_event", callback1)
    bus.on("multi_event", callback2)

    bus.emit("multi_event", "data")

    assert len(results) == 2
    assert "callback1: data" in results
    assert "callback2: data" in results


def test_event_bus_error_handling():
    """Test error handling in callbacks"""
    bus = EventBus()

    def good_callback(data):
        pass

    def bad_callback(data):
        raise ValueError("Test error")

    bus.on("error_event", good_callback)
    bus.on("error_event", bad_callback)

    # Should not raise, should log error
    bus.emit("error_event", "data")

    # Good callback should still work
    assert len(bus._listeners["error_event"]) == 2


def test_event_bus_clear():
    """Test clearing listeners"""
    bus = EventBus()

    def callback1(data):
        pass

    def callback2(data):
        pass

    bus.on("event1", callback1)
    bus.on("event2", callback2)

    assert len(bus._listeners) == 2

    # Clear specific event
    bus.clear("event1")
    assert "event1" not in bus._listeners or len(bus._listeners["event1"]) == 0
    assert "event2" in bus._listeners

    # Clear all
    bus.clear()
    assert len(bus._listeners) == 0


def test_event_bus_no_data():
    """Test emitting events without data"""
    bus = EventBus()

    called = []

    def callback():
        called.append(True)

    bus.on("no_data_event", callback)
    bus.emit("no_data_event")

    assert len(called) == 1


def test_event_bus_decorator():
    """Test the decorator syntax"""
    from src.core import get_event_bus, on_event

    # Get global bus
    bus = get_event_bus()

    # Clear any existing listeners
    bus.clear()

    called = []

    @on_event("decorator_event")
    def decorated_callback(data=None):
        called.append(data)

    bus.emit("decorator_event", "decorated")

    assert len(called) == 1
    assert called[0] == "decorated"
