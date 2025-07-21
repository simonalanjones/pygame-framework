import pygame
from lib.game_sprite import GameSprite


class Baseline(GameSprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((224, 1), pygame.SRCALPHA)
        # define the green color as (R, G, B) tuple
        self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 240

    def apply_bomb_damage(self, bomb_sprite):
        bomb_sprite.rect.y = 232
        self.image.set_at((bomb_sprite.rect.x + 2, 0), (128, 0, 0, 10))
        self.image.set_at((bomb_sprite.rect.x + 4, 0), (128, 0, 0, 10))
        self.image.set_at((bomb_sprite.rect.x, 0), (128, 0, 0, 10))

        bomb_sprite.explode()
