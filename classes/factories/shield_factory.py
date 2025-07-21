from classes.models.shield import Shield
from classes.config.shield_config import ShieldConfig
from classes.containers.shield_container import ShieldContainer
from lib.sprite_sheet import ShieldSpriteSheet


class ShieldFactory:
    def __init__(self):
        self.shield_image = ShieldSpriteSheet().get_sprite("shield_frame")
        self.shield_positions = ShieldConfig().get("positions")
        self.shield_container = ShieldContainer()

    def create_shields(self):
        for position in self.shield_positions:
            x, y = position
            shield = Shield(x, y, self.shield_image)
            self.shield_container.add(shield)

        return self.shield_container
