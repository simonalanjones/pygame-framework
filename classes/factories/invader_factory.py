from classes.models.invader import Invader
from classes.config.invader_config import InvaderConfig
from lib.sprite_sheet import InvaderSpriteSheet


class InvaderFactory:
    def __init__(self):
        config = InvaderConfig()

        self.points_array = config.get("points")
        self.spawn_rows = config.get("spawn_rows")

        self.invader_cols = config.get("cols")

        # number of invaders to draw vertically
        self.invader_rows = config.get("rows")

        # starting x position of invaders
        self.x_position_start = config.get("x_position_start")

        # horizontal offset between each invader
        self.x_repeat_offset = config.get("x_repeat_offset")

        # vertical offset between each invader
        self.y_repeat_offset = config.get("y_repeat_offset")

        sprite_sheet = InvaderSpriteSheet()

        self.explode_image = sprite_sheet.get_sprite("invader_explode_frame")
        # invaders build/drawn upwards on screen

        self.invader_build_array = [
            [
                sprite_sheet.get_sprite("invader_small_frame1"),
                sprite_sheet.get_sprite("invader_small_frame2"),
            ],
            [
                sprite_sheet.get_sprite("invader_small_frame1"),
                sprite_sheet.get_sprite("invader_small_frame2"),
            ],
            [
                sprite_sheet.get_sprite("invader_mid_frame1"),
                sprite_sheet.get_sprite("invader_mid_frame2"),
            ],
            [
                sprite_sheet.get_sprite("invader_large_frame1"),
                sprite_sheet.get_sprite("invader_large_frame2"),
            ],
            [
                sprite_sheet.get_sprite("invader_large_frame1"),
                sprite_sheet.get_sprite("invader_large_frame2"),
            ],
        ]

    def create_invader_swarm(self):
        spawn_rows_pointer = 0

        # starting y position of invaders (change with each wave cleared)
        y_position_start = self.spawn_rows[spawn_rows_pointer]
        index = 0

        for y_position in range(self.invader_rows):
            for x_position in range(self.invader_cols):
                yield self.create_invader(
                    self.x_position_start + (x_position * self.x_repeat_offset),
                    y_position_start - (y_position * self.y_repeat_offset),
                    True,
                    x_position,
                    4 - y_position,
                    index,
                    self.points_array[4 - y_position],
                )

                index += 1

    def create_invader(self, x, y, active, column, row, index, points):
        invader_sprite = Invader(
            x,
            y,
            active,
            column,
            row,
            self.invader_build_array[row],
            self.explode_image,
            index,
            points,
        )
        return invader_sprite
