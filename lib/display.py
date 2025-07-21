import pygame
from classes.config.game_config import GameConfig
from lib.debug import DebugOverlay
from lib.event_object import EventObject

class Display(EventObject):
    def __init__(self):
        super().__init__()
        config = GameConfig()
        self.top_left = config.get("top_left")
        self.original_screen_size = config.get("original_screen_size")
        self.larger_screen_size = config.get("larger_screen_size")
        _bg_image = pygame.image.load(config.get_file_path(config.get("bg_image_path")))
        self.scaled_image = pygame.transform.scale(_bg_image, self.larger_screen_size)
        self.window_surface = pygame.display.set_mode(self.larger_screen_size)
        self.is_debugging = False

    def set_debugging(self, is_debugging):
        self.is_debugging = is_debugging

    # def setDebug(self, debug_instance):
    #     self.debug_instance = debug_instance

    def update(self, surface_array, wiping=False, wipe_x=0):

        clean_game_surface = pygame.Surface(self.original_screen_size, pygame.SRCALPHA)
        for drawable_surface in surface_array:
            if isinstance(drawable_surface, pygame.sprite.Group):
                drawable_surface.draw(clean_game_surface)
            elif isinstance(drawable_surface, pygame.Surface):
                clean_game_surface.blit(drawable_surface, (0, 0))
            elif isinstance(drawable_surface, pygame.sprite.GroupSingle):
                drawable_surface.draw(clean_game_surface)

        # background image is drawn first
        self.window_surface.blit(self.scaled_image, self.top_left)

        # scale the playing surface up to target size on main window
        self.window_surface.blit(
            pygame.transform.scale(clean_game_surface, self.larger_screen_size),
            self.top_left,
        )

        # if self.is_debugging:
        #     self.window_surface.blit(self.debug_instance.render(),self.top_left)

        # if wiping == True:
        #     if wipe_x <= 224 * 4:
        #         self.window_surface.blit(
        #             self.scaled_image, (0, 160), (0, 160, wipe_x, 256 * 4)
        #         )
        #     elif wipe_x >= 224 * 4:
        #         self.window_surface.blit(
        #             self.scaled_image, (0, 160), (0, 160, 224 * 4, 256 * 4)
        #         )
