import pygame
from pygame.locals import *
from lib.controller import Controller
from lib.drawable import Drawable 
from lib.sprite import MySprite

class TestController(Controller):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.x2 = 0

        self.red_surface = pygame.Surface((100, 100))
        self.red_surface.fill((255, 0, 0))  # RGB red

        self.blue_surface = pygame.Surface((100, 100))
        self.blue_surface.fill((0, 0, 255))  # RGB blue

        self.sprite = MySprite((100, 150))  # Start position
        self.sprite_group = pygame.sprite.Group(self.sprite)

    def game_ready(self):
        self.add_listener(
            "escape_button_pressed", self.on_escape_button_pressed
        )
        print('Game ready')

    def on_escape_button_pressed(self,data):
        print(data)

    def update(self, events, dt=0):
        self.x += 60 * dt
        self.x2 += 1
        self.sprite_group.update(dt)

    def get_drawables(self):
        return [
            Drawable(self.blue_surface, (self.x2, 100), z_index=-9, scale=True),
            Drawable(self.sprite.image, self.sprite.rect.topleft, z_index=10,scale=False)
        ]
        # surface = pygame.Surface((224, 256))
        # surface.fill((255, 255, 0))  # Bright yellow
        # return [Drawable(surface, (-10, -10), z_index = 100, scale=True)]
