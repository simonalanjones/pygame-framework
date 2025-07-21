from classes.states.state_game_starts import StateGameStarts
from classes.states.state_game_playing import StateGamePlaying
from classes.states.state_game_over import StateGameOver
from classes.states.state_player_dies import StatePlayerDies
from classes.states.game_state import GameState

class StateMachine:
    def __init__(self, event_manager, registry):
        self.event_manager = event_manager
        self.registry = registry

        self.states = {
            GameState.START: StateGameStarts,
            GameState.PLAYING: StateGamePlaying,
            GameState.GAME_OVER: StateGameOver,
            GameState.PLAYER_DIES: StatePlayerDies,
        }

        self.state = None
        self.change_to(GameState.PLAYING)

    def get_state_name(self):
        return self.state.state_name if self.state else None

    def has_valid_state(self):
        return self.state is not None

    def get_state_controllers(self):
        return getattr(self.state, "controllers", [])

    def change_to(self, state_enum: GameState):
        if state_enum not in self.states:
            print(f"[StateMachine] Invalid state change requested: {state_enum}")
            return

        state_cls = self.states[state_enum]
        ctrls = self.registry.get_for(state_enum) or []

        if not ctrls:
            print(f"[StateMachine] No controllers listed for state: {state_enum.name}")

        self.state = state_cls(state_enum, ctrls)
        self.state.enter(self.change_to)

    def update(self, events):
        if self.state:
            self.state.update(events)
