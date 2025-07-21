from classes.events.input_events import FireKeyPressedEvent
from lib.controller import Controller
from classes.containers.player_missile_container import PlayerMissileContainer
from classes.states.game_state import GameState


class PlayerMissileController(Controller):
    states = (GameState.PLAYING, GameState.PLAYER_DIES)

    def __init__(self):
        super().__init__()
        self.ready_flag = False
        self.rendering_order = 1
        self.shot_counter = 0
        self.player_missile_container = PlayerMissileContainer()
        self.register_listeners()
        self.register_callbacks()

    def get_surface(self):
        return self.player_missile_container

    def get_shot_counter(self):
        return self.shot_counter

    # check all the conditions before allowing a new missile
    def can_player_fire_missile(self):
        return True
        # and not self.callback("mothership_is_exploding")
        # return (
        #     self.player_missile_container.find_missile_sprite() == None
        #     and self.ready_flag
        #     and not self.player_missile_container.find_missile_explosion()
        # )

    def update(self, events, dt=0):
        self.player_missile_container.update()

    def register_listeners(self):
        # self.event_manager.add_listener("invader_hit", self.on_missile_not_ready)
        # self.event_manager.add_listener("invader_removed", self.on_missile_ready)
        # self.event_manager.add_listener(
        #     "entered_state_game_playing", self.on_missile_ready
        # )
        self.add_listener(FireKeyPressedEvent, self.on_fire_pressed)
        # self.event_manager.add_listener("mothership_exit", self.on_mothership_exit)

    def register_callbacks(self):
        self.callback_manager.register_callback(
            "get_shot_counter", self.get_shot_counter
        )

    def on_fire_pressed(self, _):
        if self.can_player_fire_missile():
            player = self.callback_manager.callback("get_player")
            params = {
                "player_x_position": player.rect.x,
                "player_y_position": player.rect.y,
            }
            self.player_missile_container.add_missile_sprite(params)
            self.shot_counter = (self.shot_counter + 1) % 16

    def on_mothership_exit(self, _):
        self.shot_counter = 0

    def on_missile_not_ready(self, _):
        self.ready_flag = False

    def on_missile_ready(self, _):
        self.ready_flag = True
