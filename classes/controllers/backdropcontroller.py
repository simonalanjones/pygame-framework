import os
import pygame
from pygame.locals import *
from lib.controller import Controller
from lib.drawable import Drawable 


class BackdropController(Controller):
    def __init__(self):
        super().__init__()

        image_path = os.path.join("graphics", "invaders_moon_bg.png")
        self.image_surface = pygame.image.load(image_path).convert_alpha()
        self.image_surface = pygame.transform.scale(self.image_surface , (224*4, 256*4))

    def update(self, events, dt=0):
        pass  # Nothing needed here for a static background

    def get_drawables(self):
        return [
            Drawable(self.image_surface, (-200, 900), z_index=-1, scale=False)
        ]
