from dataclasses import dataclass
from classes.events.base_event import BaseEvent

@dataclass(frozen=True)
class LeftInputKeyPressedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class LeftInputKeyReleasedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class RightInputKeyPressedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class RightInputKeyReleasedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class FireKeyPressedEvent(BaseEvent):
    pass

@dataclass(frozen=True)
class EscapeKeyPressed(BaseEvent):
    pass