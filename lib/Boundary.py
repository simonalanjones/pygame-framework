import pygame


class Boundary:
    def __init__(self, position, size):
        # Create a pygame.Rect directly
        self.rect = pygame.Rect(position, size)

    def draw(self, surface):
        # Draw a line around the edge of the rectangle
        pygame.draw.rect(
            surface, (255, 0, 0), self.rect, 2
        )  # Red color, 2-pixel border

    def check_collision(self, sprite):
        # Optional: Check for collision with a pygame.sprite.Sprite
        return self.rect.colliderect(sprite.rect)
