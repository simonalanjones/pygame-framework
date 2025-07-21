from lib.controller import Controller
from classes.states.game_state import GameState
from classes.factories.bomb_factory import BombFactory
from classes.containers.bomb_container import BombContainer
from classes.models.invader import Invader
from classes.models.bomb import Bomb
from classes.events.player_events import PlayerDiedEvent
import random


class BombController(Controller):
    states = (GameState.PLAYING, GameState.PLAYER_DIES)

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.enabled = True
        self.reload_time = 60  # reload speed

        self.bomb_types = ("plunger", "squiggly", "rolling")
        self.bomb_factory = BombFactory()
        self.bomb_container = BombContainer()
        self.add_listener(PlayerDiedEvent, self.on_stop_event)

    def on_entered_state(self, state: GameState):
        if state == GameState.PLAYING:
            print("[PlayerController] Game has entered PLAYING state")


        # self.event_manager.add_listener("player_explodes", self.on_stop_event)
        # self.event_manager.add_listener("invaders_landed", self.on_stop_event)
        #
        # self.event_manager.add_listener(
        #     "entered_state_game_playing", self.on_game_playing
        # )

    def get_surface(self):
        return self.bomb_container

    # we need access to invaders to determine which can drop bombs
    def get_invaders(self):
        if self.callback_manager.callback_exists("get_invaders"):
            return self.callback_manager.callback("get_invaders")
        return None

    def get_invaders_with_clear_path(self):
        if self.callback_manager.callback_exists("get_invaders_with_clear_path"):
            return self.callback_manager.callback("get_invaders_with_clear_path")
        return None

    def get_score(self):
        if self.callback_manager.callback_exists("get_score"):
            return self.callback_manager.callback("get_score")
        return None

    def get_player(self):
        if self.callback_manager.callback_exists("get_player"):
            return self.callback_manager.callback("get_player")
        return None

    def get_max_bombs(self):
        score = self.get_score()
        if not score:
            return 1
        if int(score) > 300:
            return 2
        else:
            return 1

    def on_game_playing(self, data):
        self.reload_time = 120

    def on_stop_event(self, data):
        self.enabled = False

    def on_player_ready(self):
        self.enabled = True

    def update(self, events, dt=0):
        if len(self.bomb_container.get_bombs()) < self.get_max_bombs():
            if self.reload_time <= 0:
                self.create_new_bomb()

            else:
                self.reload_time -= 1

        self.counter += 1
        if self.counter == 2:
            self.counter = 0
            self.bomb_container.update()

    def create_new_bomb(self):
        invaders = self.get_invaders()
        if invaders and self.enabled == True:
            bomb = self.create_bomb()
            if isinstance(bomb, Bomb):
                self.bomb_container.add(bomb)
                self.reload_time = 30

    # bomb creation involves knowledge of invaders and what's already in the container group
    # putting that in a factory or the container feels off
    def create_bomb(self):
        def get_next_bomb_type():
            if self.bomb_container.has_rolling_shot():
                bomb_type = random.choice(self.bomb_types[:2])
            else:
                bomb_type = random.choice(self.bomb_types)
            return bomb_type

        bomb_type = get_next_bomb_type()
        invader = self.find_attacking_invader(bomb_type)
        if isinstance(invader, Invader):
            return self.bomb_factory.create_bomb(invader, bomb_type)
        return None

    def find_attacking_invader(self, bomb_type):
        invaders_with_clear_path = self.get_invaders_with_clear_path()

        def is_valid_target(invader):
            return invader.active

        def is_rolling_bomb():
            return bomb_type == "rolling" and self.get_player() is not None

        if is_rolling_bomb():
            player_rect = self.get_player().get_rect()
            valid_invaders = [
                invader
                for invader in invaders_with_clear_path
                if player_rect.x <= (invader.rect.x + 8) <= (player_rect.x + 16)
                   and is_valid_target(invader)
            ]
            if valid_invaders:
                return random.choice(valid_invaders)
        else:
            if invaders_with_clear_path:
                return random.choice(invaders_with_clear_path)

        # Return None if no valid invader is found
        return None
