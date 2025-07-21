from lib.game_sprite import GameSprite


class Invader(GameSprite):
    def __init__(
        self, x, y, active, column, row, image_frames, explode_image, index, points
    ):
        super().__init__()

        self.index = index
        self.row = row
        self.column = column
        self.frame_pointer = 0
        self.image_frames = image_frames
        self.explode_frame = explode_image
        self.active = active
        self.points = points

        # Create copies of the image frames to modify without affecting originals
        self.modified_frames = [frame.copy() for frame in self.image_frames]

        self.image = self.modified_frames[0]  # Start with the modified copy
        self.rect = self.image.get_rect(topleft=(x, y))

    def bomb_launch_position(self):
        return (self.rect.x + 7, self.rect.y + 8)

    def explode(self):
        self.image = self.explode_frame
        self.active = False

    def release(self):
        self.kill()

    def move_across(self, direction):
        self.image = self.get_sprite_image()
        self.rect.x += direction

    def move_down(self, direction):
        self.rect.y += direction
        self.image = self.get_sprite_image()

    def get_sprite_image(self):
        self.frame_pointer = 1 - self.frame_pointer
        return self.modified_frames[self.frame_pointer]
        # return self.modify_pixel_colors(
        #     self.modified_frames[self.frame_pointer]
        # )  # Use the modified copy
