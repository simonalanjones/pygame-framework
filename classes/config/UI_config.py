from classes.config.base_config import BaseConfig


class UIConfig(BaseConfig):
    config_values = {
        "score_label_text": "SCORE",
        "score_label_position": (60, 16),
        "score_value_position": (60, 32),
        "hiscore_label_text": "HI-SCORE",
        "hiscore_label_position": (118, 16),
        "hiscore_value_position": (118, 32),
        "game_over_position": (78, 48)
        # "tints": [
        #     {"position": (0, 0), "size": (224, 32), "color": (255, 255, 255)},
        #     {"position": (0, 32), "size": (224, 32), "color": (255, 0, 0)},
        #     {"position": (0, 64), "size": (224, 120), "color": (255, 255, 255)},
        #     {"position": (0, 184), "size": (224, 56), "color": (0, 255, 0)},
        #     {"position": (0, 240), "size": (24, 16), "color": (255, 255, 255)},
        #     {"position": (24, 240), "size": (112, 16), "color": (0, 255, 0)},
        #     {"position": (136, 240), "size": (88, 16), "color": (255, 255, 255)},
        # ],
    }
