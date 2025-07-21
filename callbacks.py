# callbacks.py
from enum import Enum, auto

class CallbackKey(Enum):
    GET_PLAYER = auto()
    SPAWN_PLAYER = auto()
    GET_BOMBS = auto()
    GET_LIVES_COUNT = auto()
