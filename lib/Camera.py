import math
import pygame


class Camera:
    def __init__(
        self,
        width,
        height,
        initial_pos,
        world_width,
        world_height,
        smoothing_enabled=True,
        smoothing_speed=0.1,
    ):
        self.camera = pygame.Rect(initial_pos[0], initial_pos[1], width, height)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.smoothing_enabled = smoothing_enabled
        self.smoothing_speed = smoothing_speed

        self.camera_margin_x = 125
        self.camera_margin_y = 125
        self.camera_speed = 5
        self.target = None
        self.debug = False

    def apply(self, entity, speed_factor=1):
        x = math.floor(self.camera.x * speed_factor)
        y = math.floor(self.camera.y * speed_factor)

        # print(f"Entity position after camera apply: ({x}, {y})")
        return entity.rect.move(-x, -y)

    def set_target(self, target: pygame.sprite.Sprite):
        self.target = target

    def update(self):
        if not self.target is None:
            target_x = self.target.rect.centerx
            target_y = self.target.rect.centery

            camera_left_margin = self.camera.x + self.camera_margin_x
            camera_right_margin = self.camera.x + self.width - self.camera_margin_x
            camera_top_margin = self.camera.y + self.camera_margin_y
            camera_bottom_margin = self.camera.y + self.height - self.camera_margin_y

            desired_x = self.camera.x
            desired_y = self.camera.y

            if target_x < camera_left_margin:
                desired_x = target_x - self.camera_margin_x
            elif target_x > camera_right_margin:
                desired_x = target_x - self.width + self.camera_margin_x

            if target_y < camera_top_margin:
                desired_y = target_y - self.camera_margin_y
            elif target_y > camera_bottom_margin:
                desired_y = target_y - self.height + self.camera_margin_y

            desired_x = max(0, min(desired_x, self.world_width - self.width))
            desired_y = max(0, min(desired_y, self.world_height - self.height))

            # Use math.floor to ensure positions are rounded down to nearest integer
            if self.smoothing_enabled:
                self.camera.x += math.floor(
                    (desired_x - self.camera.x) * self.smoothing_speed
                )
                self.camera.y += math.floor(
                    (desired_y - self.camera.y) * self.smoothing_speed
                )
            else:
                self.camera.x = desired_x
                self.camera.y = desired_y

            self.camera.x = self.camera.x
            self.camera.y = self.camera.y
        else:
            if self.debug:
                print("No target set for camera")
