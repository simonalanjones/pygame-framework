from classes.config.base_config import BaseConfig


class BombConfig(BaseConfig):
    config_values = {
        "max_bombs": 1,
        "grace_period": 60,
    }
