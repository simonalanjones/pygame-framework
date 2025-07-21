from lib.container import ContainerSingle
from classes.models.Mothership import Mothership
from classes.config.Mothership_config import MothershipConfig
from lib.sprite_sheet import MothershipSpriteSheet


class MothershipContainer(ContainerSingle):
    def __init__(self):
        super().__init__()
        self.config = MothershipConfig()
        self.sprite_sheet = MothershipSpriteSheet()

        self.spawn_right_position = self.config.get("spawn_right_position")
        self.spawn_left_position = self.config.get("spawn_left_position")

        self.points_table = self.config.get("points_table")
        self.mothership_image = self.sprite_sheet.get_sprite("mothership_frame")
        self.explode_image = self.sprite_sheet.get_sprite("explode_frame")

        self.collision_manager.register_group(
            name="mothership",
            function=self.sprites,
            collision_group="targets",
        )

    def update(self):
        self.sprite.update()

    def get_shot_counter(self):
        if self.callback_manager.callback_exists("get_shot_counter"):
            return self.callback_manager.callback("get_shot_counter")

    def get_spawn_direction(self):
        shot_count = self.get_shot_counter()
        if shot_count:
            return -1 if shot_count % 2 == 1 else 1
        else:
            return 1  # default

    def get_spawn_position(self):
        shot_count = self.get_shot_counter()
        if shot_count:
            return (
                self.spawn_right_position
                if shot_count % 2 == 1
                else self.spawn_left_position
            )
        else:
            return self.spawn_left_position  # default

    def spawn(self):
        self.event_manager.notify("mothership_spawned")
        self.spawned = True
        self.sprite = Mothership(
            self.mothership_image,
            self.explode_image,
            self.get_spawn_position(),
            self.get_spawn_direction(),
            self.points_table,
        )
