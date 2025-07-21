from lib.controller import Controller
from classes.config.audio_config import AudioConfig
from classes.states.game_state import GameState

class SoundController(Controller):
    #audio_config = AudioConfig
    #states = (GameState.PLAYING, GameState.PLAYER_DIES)
    def __init__(self):
        super().__init__()
        audio_config = AudioConfig()

        self.move1_sound = audio_config.get("move1_sound")


        ## set up channels

    def update(self, dt):
        pass