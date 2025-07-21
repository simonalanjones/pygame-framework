from classes.states.state_base import StateBase


class StatePlayerDies(StateBase):
    def __init__(self, event_manager, controllers):
        super().__init__(event_manager, controllers)

    def enter(self, change_to):
        super().enter(change_to)
        # any extra startup logic here

    def update(self, events):
        super().update(events)
        # your game-playing logic here

    def exit(self, next_state):
        super().exit(next_state)
        # any cleanup before leaving
