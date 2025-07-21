from classes.containers.invader_container import InvaderContainer
from classes.factories.invader_factory import InvaderFactory
from classes.states.game_state import GameState
from lib.controller import Controller
from classes.events.invader_events import InvaderSwarmCompleteEvent
from classes.events.player_events import PlayerDiedEvent

class InvaderController(Controller):
    states = (GameState.PLAYING, GameState.PLAYER_DIES)
    def __init__(self):
        super().__init__()

        self.countdown = 0

        invader_factory = InvaderFactory()
        self.invader_generator = invader_factory.create_invader_swarm()
        self.invader_container = InvaderContainer()
        self.register_callbacks(self.invader_container)
        self.is_moving = False
        self.swarm_complete = False
        self.add_listener(PlayerDiedEvent, self.on_stop_event)
        #self.debug = DebugOverlay.get_instance()
        #self.debug.add_watch("Lowest invader Y", lambda: self.invader_container.get_lowest_invader_y())

    def on_stop_event(self, _):
        self.is_moving = False

    def update(self, events: list, dt: float = 0) -> None:

        if self.swarm_complete:
            if self.countdown > 0:
                self.countdown -= 1
                if self.countdown <= 0:
                    self.release_non_active()

            if self.is_moving:
                self.invader_container.update()

        else:
            self.generate_next_invader()

    
    def get_surface(self):
        return self.invader_container
    


    def generate_next_invader(self):
        try:
            self.invader_container.add_invader(next(self.invader_generator))
        except StopIteration:
            if not self.swarm_complete:
                self.swarm_complete = True
                self.is_moving = True
                self.notify(InvaderSwarmCompleteEvent(len(self.invader_container)))


    def register_callbacks(self, container):
        self.register_callback("get_invaders", container.sprites)

        self.register_callback(
            "get_landed_state", container.invaders_have_landed
        )
         
        self.register_callback(
            "get_invader_count", container.get_invader_count
        )

        self.register_callback(
            "get_invaders_with_clear_path", container.get_invaders_with_clear_path
        )

        self.register_callback(
            "get_lowest_invader_y", container.get_lowest_invader_y
        )
