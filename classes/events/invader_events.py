from dataclasses import dataclass
from classes.events.base_event import BaseEvent

@dataclass(frozen=True)
class InvaderSwarmCompleteEvent(BaseEvent):
    invader_count: int
