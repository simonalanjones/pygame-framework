# classes/events/collision_events.py
from dataclasses import dataclass
from classes.events.base_event import BaseEvent
from typing import Any

@dataclass(frozen=True)
class SpriteCollisionEvent(BaseEvent):
    sprite1: Any
    sprite2: Any
    collision_area: Any
