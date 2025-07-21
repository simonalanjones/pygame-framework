import random
import pygame
from lib.game_sprite import GameSprite


class Shield(GameSprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.original_image = image.convert_alpha()  # Store the original image
        self.image = image.copy()  # Create a copy for modification
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # create the mask from the shield image
        # used in collision detection
        self.modify_pixel_colors(self.image)
        self.mask = pygame.mask.from_surface(self.image)

    def get_local_position(self, global_position, shield_rect):
        # Converts global position to local position inside the shield
        local_x = global_position[0] - shield_rect.x
        local_y = global_position[1] - shield_rect.y
        return (local_x, local_y)

    def adjust_position(self, position, offset):
        # Adjusts position by adding offset
        adjusted_x = position[0] + offset[0]
        adjusted_y = position[1] + offset[1]
        return (adjusted_x, adjusted_y)

    def apply_explosion_damage(self, modified_surface, explosion_sprite, shield_rect):
        # Applies explosion damage to the shield
        explosion_global_position = explosion_sprite.rect.topleft
        local_explosion_position = self.get_local_position(
            explosion_global_position, shield_rect
        )
        modified_surface.blit(
            explosion_sprite.image,
            local_explosion_position,
            special_flags=pygame.BLEND_RGBA_SUB,
        )

    def apply_missile_damage(self, modified_surface, missile_sprite, shield_rect):
        # Applies missile damage to the shield
        missile_global_position = missile_sprite.rect.topleft
        # Adjust missile position if needed
        missile_global_position = self.adjust_position(missile_global_position, (0, 2))
        local_missile_position = self.get_local_position(
            missile_global_position, shield_rect
        )
        modified_surface.blit(
            missile_sprite.image,
            local_missile_position,
            special_flags=pygame.BLEND_RGBA_SUB,
        )

    def missile_damage(self, missile_sprite):
        # Applies damage to the shield surface
        shield_rect = self.rect
        modified_shield_surface = self.image.copy()

        # Apply explosion damage
        explosion_sprite = self.callback_manager.callback(
            "get_player_missile_explosion"
        )
        self.apply_explosion_damage(
            modified_shield_surface, explosion_sprite, shield_rect
        )

        # Apply missile damage
        missile_sprite = self.callback_manager.callback("get_player_missile")
        self.apply_missile_damage(modified_shield_surface, missile_sprite, shield_rect)

        # Update the shield image and mask
        self.image = modified_shield_surface
        self.mask = pygame.mask.from_surface(modified_shield_surface)

    def bomb_collision(self, bomb_sprite):
        shield_rect = self.rect
        global_position = bomb_sprite.rect.topleft

        # Convert global position to local position inside the shield
        local_position = (
            global_position[0] - shield_rect.x,
            global_position[1] - shield_rect.y,
        )

        bomb_type = bomb_sprite.bomb_type
        # if bomb_type == "plunger":
        #     y_adjust = -4
        # else:
        #     y_adjust = 2

        y_adjust = 2

        modified_shield_surface = self.image.copy()
        modified_shield_surface.blit(
            self.modify_pixel_colors(bomb_sprite.explode_frame),
            # (local_position[0], 0 - y_adjust),
            (local_position[0], local_position[1]),
            special_flags=pygame.BLEND_RGBA_SUB,
        )
        self.image = modified_shield_surface
        # update the sprite mask so future collisions
        # use the mask rather than a basic rect
        self.mask = pygame.mask.from_surface(
            self.modify_pixel_colors(modified_shield_surface)
        )

    def invader_damage(self, invader_sprite):
        shield_rect = self.rect
        invader_rect = invader_sprite.rect
        overlap_rect = shield_rect.clip(invader_rect)
        overlap_rect.x -= shield_rect.x
        overlap_rect.y -= shield_rect.y

        overlap_surface = pygame.Surface(overlap_rect.size, pygame.SRCALPHA)
        overlap_surface.fill((255, 255, 255))

        modified_shield_surface = self.image.copy()
        modified_shield_surface.blit(
            overlap_surface,
            overlap_rect,
            special_flags=pygame.BLEND_RGBA_SUB,
        )
        self.image = modified_shield_surface
        self.mask = pygame.mask.from_surface(modified_shield_surface)
