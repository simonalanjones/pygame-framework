from lib.game_sprite import GameSprite
from lib.sprite_sheet import PlayerSpriteSheet


class PlayerMissileExplosion(GameSprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_sheet = PlayerSpriteSheet()
        self.image = sprite_sheet.get_sprite("missile_explode")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count_down = 30

    def update(self):
        self.count_down -= 1
        if self.count_down <= 0:
            self.kill()
        return self.modify_pixel_colors(self.image)
