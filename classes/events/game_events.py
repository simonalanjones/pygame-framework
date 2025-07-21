from dataclasses import dataclass
from classes.events.base_event import BaseEvent

@dataclass(frozen=True)
class GameplayStartEvent(BaseEvent):
    pass