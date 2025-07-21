from classes.states.state_base import StateBase


class StateGameStarts(StateBase):
    def __init__(self, event_manager, controllers):
        super().__init__(event_manager, controllers)

    def enter(self, change_to):
        super().enter(change_to)
        print("here in enter")

    def update(self, events):
        super().update(events)

    def exit(self, next_state):
        super().exit(next_state)
        # any cleanup before leaving