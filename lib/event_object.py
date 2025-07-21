# lib/event_object.py

from lib.event_manager import EventManager
from lib.callback_manager import CallbackManager


class EventObject:
    def __init__(self):
        self.event_manager    = EventManager.get_instance()
        self.callback_manager = CallbackManager.get_instance()