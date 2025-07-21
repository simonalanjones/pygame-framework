from classes.config.base_config import BaseConfig


class MothershipConfig(BaseConfig):
    config_values = {
        # "cycles_with_explosion_frame": 60,
        # "cycles_with_bonus_text": 60,
        "cycles_until_spawn": 200,
        "qualifying_invader_y_position": 36,
        "spawn_left_position": (0, 48),
        "spawn_right_position": (224, 48),
        "points_table": [
            50,
            50,
            50,
            50,
            50,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            100,
            150,
            150,
            300,
        ],
    }
