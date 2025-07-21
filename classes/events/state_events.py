# events/state_events.py
from dataclasses import dataclass
from classes.states.game_state import GameState
from classes.events.base_event import BaseEvent

@dataclass
class EnteredStateEvent(BaseEvent):
    state: GameState

@dataclass
class ExitedStateEvent(BaseEvent):
    state: GameState
