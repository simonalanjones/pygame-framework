import os
from classes.config.base_config import BaseConfig


class GameConfig(BaseConfig):
    config_values = {
        "original_screen_size": (224, 256),
        "larger_screen_size": (224 * 4, 256 * 4),
        "bg_image_path": os.path.join("graphics", "invaders_moon_bg.png"),
        "max_fps": 60,
        "top_left": (0, 0),
    }
