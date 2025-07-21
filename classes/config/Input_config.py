from classes.config.base_config import BaseConfig
from pygame.locals import *


class InputConfig(BaseConfig):
    config_values = {
        "key_left": K_k,      # 'K' key pressed
        "key_right": K_l,     # 'L' key pressed
        "key_fire": K_SPACE,  # 'SPACE' key pressed
    }