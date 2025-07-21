from lib.controller import Controller
from classes.states.game_state import GameState
from classes.factories.shield_factory import ShieldFactory


class ShieldController(Controller):
    states = (GameState.PLAYING, GameState.PLAYER_DIES)
    def __init__(self):
        super().__init__()
        self.rendering_order = -1
        self.shield_container = ShieldFactory().create_shields()

    def get_surface(self):
        return self.shield_container

    def game_ready(self):
        return

    def update(self, events, dt=0):
        self.shield_container.update()
