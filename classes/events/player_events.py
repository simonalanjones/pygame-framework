from dataclasses import dataclass
from classes.events.base_event import BaseEvent

@dataclass(frozen=True)
class PlayerDiedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class PlayerExplosionCompleteEvent(BaseEvent):
    pass