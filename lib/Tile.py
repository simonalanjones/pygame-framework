import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, pos, surf, opacity, groups, parallax_factor=1, is_destructible=False
    ):
        super().__init__(groups)
        self.damage = 0

        self.damage_images = []  # Initialize an empty list to store the damage images

        for i in range(1, 7):  # Loop through numbers 1 to 4
            damage_image = pygame.image.load(
                f"graphics/tiles/damage{i}.png"
            ).convert_alpha()
            self.damage_images.append(damage_image)  # Add the image to the list

        self.image = surf

        alpha = int(opacity * 255)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed_factor = parallax_factor
        self.is_destructible = is_destructible
        self.mask = pygame.mask.from_surface(self.image)

    def is_destructible(self):
        return self.is_destructible

    def take_damage(self):
        self.damage += 1
        if self.damage < 6:
            self.image = self.damage_images[self.damage]
            self.mask = pygame.mask.from_surface(self.image)
