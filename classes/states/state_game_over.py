from classes.states.state_base import StateBase


class StateGameOver(StateBase):
    def __init__(self):
        super().__init__()
        self.controllers = ["Tilemap"]

    def enter(self, state_machine):
        super().enter(state_machine)
        print("in state game over")
