"""
Event Bus for Writing Assistant Pro

Provides a pub/sub pattern for handling application events.
Reduces coupling between components and centralizes event handling.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from loguru import logger


class EventBus:
    """
    Event bus implementation for pub/sub pattern.

    Usage:
        event_bus = EventBus()

        # Subscribe
        event_bus.on("window_shown", callback)

        # Emit
        event_bus.emit("window_shown", data)
    """

    def __init__(self):
        self._listeners: dict[str, list[Callable]] = defaultdict(list)
        self._logger = logger.bind(name="WritingAssistant.EventBus")

    def on(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type"""
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
            self._logger.debug(f"Subscribed to {event_type}: {callback.__name__}")

    def off(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type"""
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            self._logger.debug(f"Unsubscribed from {event_type}: {callback.__name__}")

    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit an event to all subscribers"""
        if event_type not in self._listeners:
            return

        self._logger.debug(f"Emitting {event_type} to {len(self._listeners[event_type])} listeners")

        for callback in self._listeners[event_type]:
            try:
                if data is not None:
                    callback(data)
                else:
                    callback()
            except Exception as e:
                self._logger.error(f"Error in callback for {event_type}: {e}", exc_info=True)

    def clear(self, event_type: str | None = None) -> None:
        """Clear all listeners or specific event type"""
        if event_type:
            self._listeners[event_type].clear()
            self._logger.debug(f"Cleared listeners for {event_type}")
        else:
            self._listeners.clear()
            self._logger.debug("Cleared all listeners")


# Global event bus instance
_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def emit_event(event_type: str, data: Any = None) -> None:
    """Convenience function to emit events"""
    get_event_bus().emit(event_type, data)


def on_event(event_type: str) -> Callable:
    """
    Decorator for subscribing to events.

    This provides a more pythonic and convenient way to subscribe to events
    compared to the traditional event_bus.on() method.

    Usage:
        # Traditional method
        def my_callback(data):
            print(data)
        event_bus.on("window_shown", my_callback)

        # Using decorator (more elegant)
        @on_event("window_shown")
        def my_callback(data):
            print(data)

    The decorator automatically registers the function as a listener when
    the function is defined, eliminating the need for explicit registration.

    Args:
        event_type: The name of the event to subscribe to

    Returns:
        A decorator function that registers the callback and returns it unchanged
    """

    def decorator(func: Callable) -> Callable:
        # Register the function with the global event bus
        get_event_bus().on(event_type, func)
        # Return the original function unchanged (allows normal usage)
        return func

    return decorator
