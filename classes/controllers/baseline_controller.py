from lib.controller import Controller
from classes.states.game_state import GameState
from classes.containers.baseline_container import BaselineContainer
from classes.models.baseline import Baseline
from classes.events.invader_events import InvaderSwarmCompleteEvent
from classes.events.collision_events import SpriteCollisionEvent

class BaselineController(Controller):

    states = (GameState.PLAYING, GameState.PLAYER_DIES)

    def __init__(self):
        super().__init__()
        self.baseline = Baseline()
        self.baseline_container = BaselineContainer()
        self.baseline_container.add(self.baseline)

        self.event_manager.add_listener(
            SpriteCollisionEvent,
            self.on_collision
        )

    def on_collision(self, evt: SpriteCollisionEvent) -> None:
        pass

    def get_surface(self):
        return self.baseline_container

    def update(self, events, dt=0):
        self.baseline_container.update()
