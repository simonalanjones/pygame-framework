import pygame
from pytmx.util_pygame import load_pygame
from lib.event_object import Event_object
from lib import Quadtree
from typing import List
from lib.Tile import Tile
from lib.Quadtree import Quadtree


class TilemapManager(Event_object):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TilemapManager()
        return cls._instance

    def __init__(self):

        super().__init__()
        self.world_width = 0
        self.world_height = 0
        self.cache = {}
        self.debug = False
        # self.tmx_file = "big-map256x256.tmx"
        self.tmx_file = "map32x32.tmx"
        self.tile_size: int = 16
        # self.layer_names = ["foreground", "midground", "background"]
        # self.layer_names = ["foreground"]
        # self.parallax_factors = {"background": 0.5, "midground": 0.75, "foreground": 1}
        self.layer_names = ["foreground", "foreground-far"]
        self.parallax_factors = {"foreground": 1, "foreground-far": 1}

    def load_map(self, tmx_file, layer_names, tile_size, parallax_factors):

        self.tmx_data = load_pygame(tmx_file)
        self.layer_names = layer_names
        self.tile_size = tile_size
        self.tile_layers = {name: pygame.sprite.Group() for name in layer_names}

        self.quadtrees = {}
        self.world_width, self.world_height = self.build_layers()
        self.cache = {name: {"rect": None, "sprites": None} for name in layer_names}
        return [self.world_width, self.world_height]

    def get_data(self):
        return self.tmx_data

    def build_layers(self):
        max_x, max_y = 0, 0

        for layer in self.tmx_data.visible_layers:

            if layer.name in self.layer_names:
                parallax_factor = self.parallax_factors[layer.name]
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_size, y * self.tile_size)

                    # Retrieve the tile properties
                    tile_properties = self.tmx_data.get_tile_properties_by_gid(
                        layer.data[y][x]
                    )

                    # Example: Check for a custom property called 'destructable'
                    is_destructible = (
                        tile_properties.get("is_destructible", False)
                        if tile_properties
                        else False
                    )
                    if is_destructible:
                        print(layer.data[y][x])
                        print("found")

                    # this is going to automatically add the Tile into the named group
                    Tile(
                        pos=pos,
                        surf=surf,
                        opacity=layer.opacity,
                        parallax_factor=parallax_factor,
                        groups=self.tile_layers[layer.name],
                        is_destructible=is_destructible,
                    )

                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y

        world_width = (max_x + 1) * self.tile_size
        world_height = (max_y + 1) * self.tile_size

        for name in self.layer_names:
            boundary = pygame.Rect(0, 0, world_width, world_height)

            self.quadtrees[name] = Quadtree(boundary, 4)

            sprite_group = pygame.sprite.Group()
            for sprite in self.tile_layers[name]:
                sprite_group.add(sprite)
            self.quadtrees[name].insert_group(sprite_group)

        return world_width, world_height

    def get_world_dimensions(self):
        return self.world_width, self.world_height

    # need to refer to viewport?
    def get_visible_foreground_sprites(self):
        foreground_layer = self.layer_names[0]
        foreground_sprites = self.get_last_query_sprites(foreground_layer)
        return foreground_sprites

    def get_last_query_sprites(self, layer_name: str) -> List[pygame.sprite.Sprite]:
        cached_data = self.cache[layer_name]
        if cached_data["sprites"] is not None:
            return cached_data["sprites"]
        else:
            query_rect = pygame.Rect(0, 0, self.world_width, self.world_height)
            return self.query_visible_sprites(layer_name, query_rect)

    # new methods:
    #   query world sprites - query sprites anywhere in the world tilemap
    #   query visible sprites - query sprites currently displayed in a viewport
    #   cache not good as other sprites use this for collision and will invalidate the cache - perhaps add name to cache

    def query_visible_sprites(
        self, layer_name: str, query_rect: pygame.Rect
    ) -> List[pygame.sprite.Sprite]:

        cached_data = self.cache[layer_name]

        # Debugging: print the cached and new query rectangles
        if self.debug:
            print(f"Cached rect: {cached_data['rect']}")
            print(f"New query rect: {query_rect}")

        if cached_data["rect"] == query_rect:
            if self.debug:
                print("Using cached sprites")
            return cached_data["sprites"]

        visible_sprites = self.quadtrees[layer_name].query(query_rect)
        self.cache[layer_name] = {"rect": query_rect.copy(), "sprites": visible_sprites}

        # Debugging: print updated cache information
        if self.debug:
            print(f"Updated cache with rect: {query_rect}")

        return visible_sprites

    def get_sprites_around_sprite(
        self, layer_name: str, sprite: pygame.sprite.Sprite, padding: int = 200
    ) -> List[pygame.sprite.Sprite]:
        """
        Returns sprites from a specific layer around a given sprite, using a padded rectangle for the query.
        """
        query_rect = sprite.rect.inflate(padding, padding)
        # print("layer", layer_name)
        return self.query_visible_sprites(layer_name, query_rect)
