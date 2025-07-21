import abc

from classes.states.game_state import GameState
from lib.event_object import EventObject
from classes.events.state_events import EnteredStateEvent, ExitedStateEvent


class StateBase(EventObject, metaclass=abc.ABCMeta):
    def __init__(self, game_state: GameState, controllers):
        super().__init__()
        self.state = game_state  # GameState enum
        self.controllers = controllers
        self.change_to = None
        self.debug = True
        self.registered_listeners = {}

        self._debug(f"Initialised state: {self.state.name}")


    @abc.abstractmethod
    def enter(self, change_to):
        self._debug(f"Entered state: {self.state.name}")
        self.event_manager.notify(EnteredStateEvent(state=self.state))
        self.change_to = change_to

    # child states will have their update method called
    @abc.abstractmethod
    def update(self, events):
        """
        Called on each loop tick with the current events.
        """
        pass

    def _notify(self, event_type, data=None):
        self.event_manager.notify(event_type, data)

    def add_listener(self, event_type, listener):
        if event_type not in self.registered_listeners:
            self.registered_listeners[event_type] = []
        self.registered_listeners[event_type].append(listener)
        self.event_manager.add_listener(event_type, listener)
        self._debug(f"Adding event {event_type} from  {listener}")

    @abc.abstractmethod
    def exit(self, next_state):
        self._debug(f"Exiting state: {self.state.name}")

        # Remove all listeners registered within this state
        for event_type, listeners in self.registered_listeners.items():
            for listener in listeners:
                self.event_manager.remove_listener(event_type, listener)
                self._debug(f"removing event {event_type} from  {listener}")

        self.event_manager.notify(ExitedStateEvent(state=self.state))
        print("next state:", next_state)
        if not self.change_to is None:
            self.change_to(next_state)
        else:
            print("unable to change:", self.change_to)

    def remove_controller(self, controller):
        if controller in self.controllers:
            self.controllers.remove(controller)
            self._debug(f"{controller} removed.")
        else:
            self._debug(f"{controller} not found in the list.")

    def _debug(self, debug_string):
        if self.debug:
            print(debug_string)

    # static helper for snake-casing class names:
    @staticmethod
    def _state_name(class_name):
        result = [class_name[0].lower()]

        for char in class_name[1:]:
            if char.isupper():
                result.extend(["_", char.lower()])
            else:
                result.append(char)

        return "".join(result)
