# classes/models/player.py

from lib.game_sprite import GameSprite
from lib.sprite_sheet import PlayerSpriteSheet
from classes.events.player_events import PlayerExplosionCompleteEvent

PLAYER_SPEED = 60

class Player(GameSprite):
    ANIMATION_FRAME_THRESHOLD_LOW = 5
    ANIMATION_FRAME_THRESHOLD_HIGH = 10
    MAX_ANIMATION_COUNT = 6

    def __init__(self, params):
        super().__init__()

        self.explosion_frame_number = 0
        self.explosion_animation_count = 0
        self.is_exploding = False

        self.sprite_sheet = PlayerSpriteSheet()
        self.image = self.sprite_sheet.get_sprite("player")
        self.exploding_images = [
            self.sprite_sheet.get_sprite("player_explode1"),
            self.sprite_sheet.get_sprite("player_explode2"),
        ]

        self.rect = self.image.get_rect(
            x=params.get("player_x_position", 0),
            y=params.get("player_y_position", 0),
        )

        #self.event_manager.add_listener("player_explodes", self.explode)
        self.pos_x = float(self.rect.x)

    def move_left(self, dt):
        self.pos_x -= PLAYER_SPEED * dt
        self.rect.x = round(self.pos_x)

    def move_right(self, dt):
        self.pos_x += PLAYER_SPEED * dt
        self.rect.x = round(self.pos_x)

    def update(self):
        return self.update_exploding() if self.is_exploding else self.modify_pixel_colors(self.image)

    def explode(self):
        print('player.py explodes')
        self.is_exploding = True
        self.image = self.exploding_images[0]

    def update_exploding(self):
        if self.explosion_animation_count < self.MAX_ANIMATION_COUNT:
            self.explosion_frame_number += 1
            if self.explosion_frame_number == self.ANIMATION_FRAME_THRESHOLD_LOW:
                self.image = self.exploding_images[1]
            elif self.explosion_frame_number == self.ANIMATION_FRAME_THRESHOLD_HIGH:
                self.image = self.exploding_images[0]
                self.explosion_frame_number = 0
                self.explosion_animation_count += 1
            return self.modify_pixel_colors(self.image)
        else:
            print('done')
            self.notify(PlayerExplosionCompleteEvent())
            #self.kill()
            self.is_exploding = False
            return None

    def get_rect(self):
        return self.rect
