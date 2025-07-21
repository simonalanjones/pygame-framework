from classes.states.game_state import GameState
from lib.event_object import EventObject
from classes.events.state_events import EnteredStateEvent, ExitedStateEvent

class Controller(EventObject):
    def __init__(self):
        super().__init__()
        self.event_manager.add_listener(EnteredStateEvent, self._handle_entered_state)
        self.event_manager.add_listener(ExitedStateEvent, self._handle_exited_state)

    def add_listener(self, event_type, listener):
        self.event_manager.add_listener(event_type, listener)

    def _handle_entered_state(self, event):
        self.on_entered_state(event.state)

    def _handle_exited_state(self, event):
        self.on_exited_state(event.state)

    def on_entered_state(self, state: GameState):
        pass  # override in subclass if needed

    def on_exited_state(self, state: GameState):
        pass  # override in subclass if needed

    def register_callback(self, key, callback, name=None):
        self.callback_manager.register_callback(key, callback, name)

    def notify(self, event):
        self.event_manager.notify(event)
