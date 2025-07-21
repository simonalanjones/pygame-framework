import os
from classes.config.base_config import BaseConfig

class AudioConfig(BaseConfig):
    config_values = {
        "mothership": "sounds/mothership.wav",
        "mothership_bonus": "sounds/mothership_bonus.wav",
        "player_explodes": "sounds/player_destroyed.wav",
        "extra_life": "sounds/extra_life.wav",
        "move_1": "sounds/move1.wav",
        "move_2": "sounds/move2.wav",
        "move_3": "sounds/move3.wav",
        "move_4": "sounds/move4.wav",

        "fleet_sound_delay": 52,
        "fleet_sound_dict": {50: 52, 43: 46, 36: 39, 28: 34, 22: 28, 17: 24, 13: 21, 10: 19, 8: 16, 7: 14, 6: 13, 5: 12,
                        4: 11, 3: 9, 2: 7, 1: 5}
    }

