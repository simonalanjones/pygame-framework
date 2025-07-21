from classes.states.state_base import StateBase
from classes.events.game_events import GameplayStartEvent

class StateGamePlaying(StateBase):
    def __init__(self, event_manager, controllers):
        super().__init__(event_manager, controllers)
        self.count_down = None


    def enter(self, change_to):
        super().enter(change_to)
        self.count_down = 180
        # any extra startup logic here

    def update(self, events):
        # your game-playing logic here
        super().update(events)
        if self.count_down > 0:
            self.count_down -= 1
            if self.count_down <= 0:
                self.event_manager.notify(GameplayStartEvent())



    def exit(self, next_state):
        super().exit(next_state)
        # any cleanup before leaving
