import pygame

class MySprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, dt):
        self.rect.x += 100 * dt  # Moves right
