from enum import Enum, auto

class GameState(Enum):
    START = auto()
    PLAYING = auto()
    PLAYER_DIES = auto()
    GAME_OVER = auto()
