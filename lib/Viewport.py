import pygame
from lib.Camera import Camera
from classes.config.game_config import GameConfig


class Layer:
    def __init__(self, name, z_index):
        self.name = name
        self.z_index = z_index
        self.sprites = pygame.sprite.Group()
        self.config = GameConfig()

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def clear_sprites(self):
        self.sprites.empty()

    def get_sprites(self):
        return self.sprites

    def debug_sprites(self):
        print(f"Sprites in layer '{self.name}':")
        for sprite in self.sprites:
            print(sprite)
        print(f"Total number of sprites in layer '{self.name}': {len(self.sprites)}")


class Viewport:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.z_index = 0  # if you want to stack multiple viewports
        self.rect = pygame.Rect(x, y, width, height)
        # self.set_camera(camera)
        self.border_color = (0, 255, 0)
        self.layers = {}
        self.temp_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        self.config = GameConfig()
        self.screen_width, self.screen_height = self.config.get("original_screen_size")

    def get_sprites_in_layer(self, layer_name):
        if layer_name in self.layers:
            return self.layers[layer_name].get_sprites()
        else:
            raise ValueError(f"Layer '{layer_name}' does not exist.")

    def clear_sprites(self):
        for layer in self.layers.values():
            layer.clear_sprites()

    def debug_sprites(self):
        for layer in sorted(self.layers.values(), key=lambda l: l.z_index):
            layer.debug_sprites()

    def debug_layers(self):
        print(f"Layers in viewport '{self.name}':")
        for layer in sorted(self.layers.values(), key=lambda l: l.z_index):
            print(f"Layer '{layer.name}' with z-index {layer.z_index}")
        print(f"Total number of layers in viewport '{self.name}': {len(self.layers)}")

    def set_z_index(self, index):
        self.z_index = index

    def set_camera(self, camera):
        if isinstance(camera, Camera):
            self.camera = camera

    def add_layer(self, layer_name, z_index):
        self.layers[layer_name] = Layer(layer_name, z_index)

    def add_sprite_to_layer(self, layer_name, sprite):
        if layer_name in self.layers:
            self.layers[layer_name].add_sprite(sprite)
        else:
            raise ValueError(f"Layer '{layer_name}' does not exist.")

    def set_target(self, target):
        if "camera" in vars(self):
            # if self.camera:
            self.camera.set_target(target)
        else:
            print("no camera for viewport to track")

    def get_camera_rect(self):
        if "camera" in vars(self):
            query_rect = pygame.Rect(
                round(self.camera.camera.x),
                round(self.camera.camera.y),
                self.camera.camera.width,
                self.camera.camera.height,
            )
        else:
            query_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        return query_rect

    def update(self):
        if "camera" in vars(self):
            self.camera.update()

    def render(self):
        temp_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        if "camera" in vars(self):
            temp_surface.fill("#71ddee")

            for layer in sorted(self.layers.values(), key=lambda l: l.z_index):
                for sprite in layer.sprites:
                    sprite_name = sprite.__class__.__name__

                    if sprite_name == "Tile":
                        sprite_position = self.camera.apply(sprite, sprite.speed_factor)
                    else:
                        sprite_position = self.camera.apply(sprite, 1)
                    temp_surface.blit(sprite.image, sprite_position)

            border_rect = pygame.Rect(
                self.camera.camera_margin_x,
                self.camera.camera_margin_y,
                self.rect.width - 2 * self.camera.camera_margin_x,
                self.rect.height - 2 * self.camera.camera_margin_y,
            )

            pygame.draw.rect(temp_surface, (0, 0, 0), border_rect, 2)

        else:
            temp_surface.fill("#666666")
        return temp_surface
