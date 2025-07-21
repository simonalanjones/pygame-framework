from lib.game_sprite import GameSprite


class Bomb(GameSprite):

    def __init__(self, x, y, image_frames, explode_frame, bomb_type):
        super().__init__()
        self.image_frames = image_frames
        self.explode_frame = explode_frame
        self.direction = 2
        self.frame_counter = 0
        self.frame_pointer = 0
        self.bomb_type = bomb_type
        self.active = True
        self.countdown = 15

        # Create copies of the image frames to modify without affecting originals
        self.modified_frames = [frame.copy() for frame in self.image_frames]
        self.image = self.modified_frames[0]  # Start with the modified copy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.active == True:
            self.frame_counter += 1
            if self.frame_counter >= 3:
                self.frame_counter = 0
                self.frame_pointer = (self.frame_pointer + 1) % len(self.image_frames)
                self.image = self.get_sprite_image()

            if self.rect.y <= 243:
                self.rect.y += 2 * 1.5  # 3 * 1.4
            else:
                self.explode()
        else:
            self.countdown -= 1
            if self.countdown == 0:
                self.kill()

    def explode(self):
        if self.active == True:
            # self.image = self.modify_pixel_colors(self.explode_frame)
            self.image = self.explode_frame

            if not self.bomb_type == "plunger":
                self.rect.y += 1
                self.rect.x -= 1
            else:
                self.rect.y += 2
                self.rect.x -= 2

            self.active = False
            self.countdown = 5

    def get_sprite_image(self):
        return self.modified_frames[self.frame_pointer]
        # return self.modify_pixel_colors(self.modified_frames[self.frame_pointer])
