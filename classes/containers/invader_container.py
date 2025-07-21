from lib.container import Container
from classes.config.invader_config import InvaderConfig
from classes.config.game_config import GameConfig
from classes.helpers.invader_movement import InvaderMovementHelper

class InvaderContainer(Container):
    def __init__(self):
        super().__init__()

        # game_config = GameConfig()
        # original_screen_size = game_config.get("original_screen_size")
        # larger_screen_size = game_config.get("larger_screen_size")
        # self.screen_scale_ratio = (
        #     larger_screen_size[0] / original_screen_size[0],
        #     larger_screen_size[1] / original_screen_size[1]
        # )


        config = InvaderConfig()
        self.invader_direction = config.get("horizontal_move")
        self.invader_down_direction = config.get("vertical_move")
        self.screen_left_limit = config.get("screen_left_limit")
        self.screen_right_limit = config.get("screen_right_limit")
        self.screen_bottom_limit = config.get("screen_bottom_limit")
        self.invaders_moving_down = False
        self.current_invader_index = 0
        self.invaders_have_landed = False

        self.movement = InvaderMovementHelper()

        self.collision_manager.register_group(
            name="invaders",
            function=self.sprites,
            collision_group="targets",
        )
        self.collision_manager.register_group(
            name="invaders_shields",
            function=self.sprites,
            collision_group="shield_collisions",
        )

        # self.event_manager.add_listener("mouse_left_clicked", self.on_mouse_left)

    # def on_mouse_left(self, data):
    #     scale_x, scale_y = self.screen_scale_ratio
    #     # Calculate inverse ratio:
    #     game_x = int(data[0] / scale_x)
    #     game_y = int(data[1] / scale_y)
    #
    #     for sprite in self.sprites():
    #         if sprite.rect.collidepoint((game_x, game_y)):
    #             print('got one')

    def update(self):
        self.movement.handle_invader_movement(self)
        self.movement.update_current_invader_index(self)

    def add_invader(self, invader):
        self.add(invader)

    def remove_inactive(self):
        for invader in list(self.sprites()):
            if not invader.active:
                self.remove_invader(invader)

    def remove_invader(self, invader):
        invader.active = False
        invader_index = invader.index

        self.remove(invader)
        for inv in self.sprites():
            if inv.index > invader_index:
                inv.index -= 1

        if invader_index < self.current_invader_index:
            self.current_invader_index -= 1
        elif invader_index == self.current_invader_index:
            if self.current_invader_index >= self.get_invader_count():
                self.current_invader_index = 0
        else:
            if self.current_invader_index >= self.get_invader_count():
                self.current_invader_index = 0


    def get_invader_count(self) -> int:
        return len(self.sprites())


    def get_lowest_invader_y(self):
        all_sprites = self.sprites()
        if all_sprites:
            return all_sprites[0].rect.y
        return None

    def get_invaders_with_clear_path(self):
        invaders_with_clear_path = []
        invader_group = self.sprites()
        if not invader_group:
            return invaders_with_clear_path
        max_row = max(invader_group, key=lambda inv: inv.row).row
        for invader in invader_group:
            clear_path = True
            if invader.row == max_row:
                invaders_with_clear_path.append(invader)
                continue
            for _invader in invader_group:
                if _invader.column == invader.column and _invader.row > invader.row:
                    clear_path = False
                    break
            if clear_path:
                invaders_with_clear_path.append(invader)
        return invaders_with_clear_path
