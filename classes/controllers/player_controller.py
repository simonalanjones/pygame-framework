# classes/controllers/player_controller.py

from lib.controller import Controller
from classes.containers.player_container import PlayerContainer
from classes.states.game_state import GameState
from classes.events.input_events import (
    LeftInputKeyPressedEvent, RightInputKeyPressedEvent,
    LeftInputKeyReleasedEvent, RightInputKeyReleasedEvent
)
from classes.events.invader_events import InvaderSwarmCompleteEvent
from classes.events.player_events import PlayerExplosionCompleteEvent



class PlayerController(Controller):
    states = (GameState.PLAYING, GameState.PLAYER_DIES)

    def __init__(self):
        super().__init__()
        self.movement_enabled = False
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.lives = 3
        self.player_container = PlayerContainer()
        self.register_listeners()
        self.register_callbacks()

    def update(self, events, dt=0):
        self.player_container.update(self.left_key_pressed, self.right_key_pressed, dt)

    def get_surface(self):
        return self.player_container if self.player_container.active else None

    def get_player(self):
        return self.player_container.get_player()

    def on_swarm_complete(self, _):
        self.player_container.activate()
        self.movement_enabled = True


    def on_explode_player(self, _):
        self.movement_enabled = False
        self.left_key_pressed = False
        self.right_key_pressed = False

    def on_player_explosion_complete(self, _):
        print('explosion complete')
        if self.lives > 0:
            self.lives -= 1

    def register_listeners(self):
        self.add_listener(InvaderSwarmCompleteEvent, self.on_swarm_complete)
        self.add_listener(LeftInputKeyPressedEvent, self.on_move_left)
        self.add_listener(RightInputKeyPressedEvent, self.on_move_right)
        self.add_listener(LeftInputKeyReleasedEvent, self.on_move_left_exit)
        self.add_listener(RightInputKeyReleasedEvent, self.on_move_right_exit)
        self.add_listener(PlayerExplosionCompleteEvent, self.on_player_explosion_complete)


    def register_callbacks(self):
        self.register_callback("get_lives_count", lambda: self.lives)





    def on_move_left(self, _):
        self.left_key_pressed = True

    def on_move_left_exit(self, _):
        self.left_key_pressed = False

    def on_move_right(self, _):
        self.right_key_pressed = True

    def on_move_right_exit(self, _):
        self.right_key_pressed = False
