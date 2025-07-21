# lib/event_manager.py
from typing import Callable
import types
from classes.events.base_event import BaseEvent


class EventManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EventManager()
        return cls._instance

    def __init__(self):
        self.listeners: dict[type, list[Callable]] = {}

    def add_listener(self, event_cls: type, listener: Callable):
        if not isinstance(event_cls, type) or not issubclass(event_cls, BaseEvent):
            raise TypeError(f"{event_cls} must be a subclass of BaseEvent")
        self.listeners.setdefault(event_cls, []).append(listener)

    def remove_listener(self, event_cls: type, listener: Callable):
        if event_cls in self.listeners:
            self.listeners[event_cls].remove(listener)

    def notify(self, event: object):
        if isinstance(event, type):
            raise TypeError(
                f"Expected an event instance, not a class. "
                f"Did you mean to call it? e.g. notify({event.__name__}())"
            )
        if not isinstance(event, BaseEvent):
            raise TypeError(
                f"Expected instance of BaseEvent, got {type(event).__name__}"
            )

        cls = type(event)
        for listener in self.listeners.get(cls, []):
            listener(event)

    def debug_listeners(self):
        print("Registered event listeners:")
        if not self.listeners:
            print("  (none)")
            return

        for event_cls, listeners in self.listeners.items():
            event_name = event_cls.__name__ if isinstance(event_cls, type) else str(event_cls)
            print(f"- {event_name}: {len(listeners)} listener(s)")

            for i, listener in enumerate(listeners, 1):
                if isinstance(listener, types.MethodType):
                    owner_class = listener.__self__.__class__.__name__
                    name = f"{owner_class}.{listener.__name__}"
                elif hasattr(listener, '__name__'):
                    name = listener.__name__
                else:
                    name = repr(listener)

                module = getattr(listener, '__module__', 'unknown')
                print(f"    {i}. {name} (module: {module})")
