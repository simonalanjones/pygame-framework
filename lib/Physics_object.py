import math
import pygame
from lib.event_object import Event_object

GRAVITY = 0.02


class PhysicsObject(pygame.sprite.Sprite, Event_object):
    def __init__(
        self,
        position,
        velocity,
        acceleration,
        rotation,
        rotationSpeed,
        max_speed,
        friction,
        mass,
    ):
        Event_object.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.rotation = rotation
        self.rotationSpeed = rotationSpeed
        self.max_speed = max_speed
        self.friction = friction
        self.mass = mass
        self.image = None
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = None
        self.hit_rect = None

    def update_physics(self):
        self.apply_gravity()
        self.velocity["speed"] *= self.friction
        if self.velocity["speed"] < 0.01:
            self.velocity["speed"] = 0
        self.move_point_by_velocity()
        self.rotate_image()

    def apply_gravity(self):
        vertical_velocity = self.velocity["speed"] * math.sin(
            self.velocity["direction"]
        )
        vertical_velocity += GRAVITY / self.mass
        self.velocity = self.comp_to_vector(
            self.velocity["speed"] * math.cos(self.velocity["direction"]),
            vertical_velocity,
        )

    def move_point_by_velocity(self):
        components = self.get_vector_components(self.velocity)
        self.position["x"] += components["xComp"]
        self.position["y"] += components["yComp"]

    def rotate_image(self):
        if self.image:
            self.image = pygame.transform.rotate(
                self.original_image, -math.degrees(self.rotation)
            )
            self.rect = self.image.get_rect(
                center=(self.position["x"], self.position["y"])
            )
            self.hit_rect.center = self.rect.center
            self.mask = pygame.mask.from_surface(self.image)

    def keep_angle_in_range(self, angle):
        while angle < 0:
            angle += 2 * math.pi
        while angle > 2 * math.pi:
            angle -= 2 * math.pi
        return angle

    def add_vectors(self, vector1, vector2):
        v1Comp = self.get_vector_components(vector1)
        v2Comp = self.get_vector_components(vector2)
        resultant_x = v1Comp["xComp"] + v2Comp["xComp"]
        resultant_y = v1Comp["yComp"] + v2Comp["yComp"]
        return self.comp_to_vector(resultant_x, resultant_y)

    def get_vector_components(self, vector):
        xComp = vector["speed"] * math.cos(vector["direction"])
        yComp = vector["speed"] * math.sin(vector["direction"])
        return {"xComp": xComp, "yComp": yComp}

    def comp_to_vector(self, x, y):
        magnitude = math.sqrt((x * x) + (y * y))
        direction = math.atan2(y, x)
        direction = self.keep_angle_in_range(direction)
        return {"speed": magnitude, "direction": direction}
