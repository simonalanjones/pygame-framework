from lib.game_sprite import GameSprite
from lib.sprite_sheet import PlayerSpriteSheet


class PlayerMissile(GameSprite):
    def __init__(self, params):
        super().__init__()

        sprite_sheet = PlayerSpriteSheet()
        # this is the image we use to knock out the shield section with
        self.missile_image = sprite_sheet.get_sprite("missile_2x")
        self.image = sprite_sheet.get_sprite("missile")

        self.explode_frame = sprite_sheet.get_sprite("missile_explode")

        self.countdown = 0
        self.active = True
        self.rect = self.image.get_rect(
            x=params.get("player_x_position") + 8, y=params.get("player_y_position")
        )

    def remove(self):
        self.kill()

    def move_up(self):
        self.rect.y -= 4

    def get_y_position(self):
        return self.rect.y

    def explode(self, offset_rect=None):
        if self.active:
            self.kill()

            # self.rect.x -= 4
            # self.image = self.explode_frame
            # if offset_rect:
            #     self.rect = self.rect.move(offset_rect)

            # self.countdown = 15

    def update(self):
        # if self.countdown > 0:
        #     self.countdown -= 1
        #     if self.countdown <= 0:
        #         self.kill()
        # else:
        #     self.rect.y -= 4  # Move the missile vertically upwards
        #     if self.rect.y <= 42:
        #         self.explode(())

        return self.modify_pixel_colors(self.image)
