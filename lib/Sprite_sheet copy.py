import pygame


class SpriteSheet:
    def __init__(self):
        self.sprite_sheet = pygame.image.load("images/sprite_sheet.png").convert_alpha()
        self.sprite_lookup = {}

    def add_sprite(self, name, x, y, width, height):
        self.sprite_lookup[name] = (x, y, width, height)

    def get_sprite(self, name):
        sprite_rect = self.sprite_lookup.get(name)
        if sprite_rect:
            x, y, width, height = sprite_rect
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
            return sprite
        else:
            raise ValueError(f"Sprite with name '{name}' not found in the spritesheet.")


class InvaderSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()

        self.add_sprite("invader_small_frame1", 1, 1, 16, 8)
        self.add_sprite("invader_small_frame2", 1, 11, 16, 8)

        self.add_sprite("invader_mid_frame1", 19, 1, 16, 8)
        self.add_sprite("invader_mid_frame2", 19, 11, 16, 8)

        self.add_sprite("invader_large_frame1", 37, 1, 16, 8)
        self.add_sprite("invader_large_frame2", 37, 11, 16, 8)

        self.add_sprite("invader_explode_frame", 55, 1, 16, 8)


class BombSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()

        self.add_sprite("plunger_frame1", 21, 21, 3, 8)
        self.add_sprite("plunger_frame2", 26, 21, 3, 8)
        self.add_sprite("plunger_frame3", 31, 21, 3, 8)
        self.add_sprite("plunger_frame4", 36, 21, 3, 8)

        self.add_sprite("squiggly_frame1", 1, 21, 3, 8)
        self.add_sprite("squiggly_frame2", 6, 21, 3, 8)
        self.add_sprite("squiggly_frame3", 11, 21, 3, 8)
        self.add_sprite("squiggly_frame4", 16, 21, 3, 8)

        self.add_sprite("rolling_frame1", 41, 21, 3, 8)
        self.add_sprite("rolling_frame2", 46, 21, 3, 8)
        self.add_sprite("rolling_frame3", 51, 21, 3, 8)
        self.add_sprite("rolling_frame4", 56, 21, 3, 8)

        self.add_sprite("explode_frame", 61, 21, 6, 8)


class ShieldSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()

        self.add_sprite("shield_frame", 45, 31, 24, 16)


class MothershipSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()

        self.add_sprite("mothership_frame", 1, 39, 16, 8)
        self.add_sprite("explode_frame", 19, 39, 24, 8)


class PlayerSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()
        self.add_sprite("player", 1, 49, 16, 8)
        self.add_sprite("player_explode1", 19, 49, 16, 8)
        self.add_sprite("player_explode2", 37, 49, 16, 8)

        self.add_sprite("missile", 55, 49, 1, 8)
        self.add_sprite("missile_2x", 68, 49, 1, 8)
        self.add_sprite("missile_explode", 58, 49, 8, 8)


class FontSpriteSheet(SpriteSheet):
    def __init__(self):
        super().__init__()

        self.add_sprite("A", 1, 69, 8, 8)
        self.add_sprite("B", 11, 69, 8, 8)
        self.add_sprite("C", 21, 69, 8, 8)
        self.add_sprite("D", 31, 69, 8, 8)
        self.add_sprite("E", 41, 69, 8, 8)
        self.add_sprite("F", 51, 69, 8, 8)
        self.add_sprite("G", 61, 69, 8, 8)
        self.add_sprite("H", 71, 69, 8, 8)

        self.add_sprite("I", 1, 79, 8, 8)
        self.add_sprite("J", 11, 79, 8, 8)
        self.add_sprite("K", 21, 79, 8, 8)
        self.add_sprite("L", 31, 79, 8, 8)
        self.add_sprite("M", 41, 79, 8, 8)
        self.add_sprite("N", 51, 79, 8, 8)
        self.add_sprite("O", 61, 79, 8, 8)
        self.add_sprite("P", 71, 79, 8, 8)

        self.add_sprite("Q", 1, 89, 8, 8)
        self.add_sprite("R", 11, 89, 8, 8)
        self.add_sprite("S", 21, 89, 8, 8)
        self.add_sprite("T", 31, 89, 8, 8)
        self.add_sprite("U", 41, 89, 8, 8)
        self.add_sprite("V", 51, 89, 8, 8)
        self.add_sprite("W", 61, 89, 8, 8)
        self.add_sprite("X", 71, 89, 8, 8)

        self.add_sprite("Y", 1, 99, 8, 8)
        self.add_sprite("Z", 11, 99, 8, 8)
        self.add_sprite("0", 21, 99, 8, 8)
        self.add_sprite("1", 31, 99, 8, 8)
        self.add_sprite("2", 41, 99, 8, 8)
        self.add_sprite("3", 51, 99, 8, 8)
        self.add_sprite("4", 61, 99, 8, 8)
        self.add_sprite("5", 71, 99, 8, 8)

        self.add_sprite("6", 1, 109, 8, 8)
        self.add_sprite("7", 11, 109, 8, 8)
        self.add_sprite("8", 21, 109, 8, 8)
        self.add_sprite("9", 31, 109, 8, 8)

        self.add_sprite("<", 41, 109, 8, 8)
        self.add_sprite(">", 51, 109, 8, 8)
        self.add_sprite("=", 61, 109, 8, 8)
        self.add_sprite("*", 71, 109, 8, 8)

        self.add_sprite("?", 1, 119, 8, 8)
        self.add_sprite("-", 11, 119, 8, 8)
        self.add_sprite("%", 1, 59, 8, 8)  # index for upside down Y
