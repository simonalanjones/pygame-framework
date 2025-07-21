import pygame
import itertools
from lib.event_manager import EventManager
from classes.events.collision_events import SpriteCollisionEvent

class Collision:
    def __init__(self, sprite1, sprite2, collision_area):
        self.sprites = (sprite1, sprite2)
        self.collision_area = collision_area

    def extract_sprite_by_class(self, target_class):
        for sprite in self.sprites:
            if sprite.__class__.__name__ == target_class:
                return sprite
        return None

    def collision_area(self):
        return self.collision_area

    def overlap_area(self):
        return self.collision_area.overlap_area


class CollisionManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = CollisionManager()
        return cls._instance

    def __init__(self):
        self.grouped_containers = {}
        self.event_manager = EventManager.get_instance()

    def register_group(
        self, name, function, collision_group=None, callback=None, autorun=False
    ):
        if collision_group not in self.grouped_containers:
            self.grouped_containers[collision_group] = []
        self.grouped_containers[collision_group].append(
            (name, function, callback, autorun)
        )

    def run_autorun_groups(self):
        for collision_group, containers in self.grouped_containers.items():

            for name, function, callback, autorun in containers:
                if autorun:
                    # print(collision_group)
                    self.check_collisions(collision_group)

    def check_collisions(self, collision_group):
        containers_to_check = self.get_containers_to_check(collision_group)
        unique_pairs = self.get_unique_pairs(containers_to_check)

        for pair in unique_pairs:
            container1_name, container1_function, callback1, autorun1 = pair[0]
            container2_name, container2_function, callback2, autorun2 = pair[1]

            self.check_collision_between_groups(
                container1_function, container2_function, callback1, callback2
            )

    def get_containers_to_check(self, collision_group):
        if collision_group is not None and collision_group in self.grouped_containers:
            return self.grouped_containers[collision_group]
        else:
            return [
                (name, function, callback)
                for group in self.grouped_containers.values()
                for name, function, callback in group
            ]

    def get_unique_pairs(self, containers_to_check):
        return itertools.combinations(containers_to_check, 2)

    def check_collision_between_groups(
        self, container1_function, container2_function, callback1, callback2
    ):
        container1_group = container1_function()
        container2_group = container2_function()

        if (
            container1_group
            and container2_group
            and hasattr(container1_group, "__iter__")
            and hasattr(container2_group, "__iter__")
        ):
            self.check_collision_between_sprites(
                container1_group, container2_group, callback1, callback2
            )

    def check_collision_between_sprites(
        self, container1_group, container2_group, callback1, callback2
    ):
        for sprite1 in container1_group:
            for sprite2 in container2_group:
                collision_area = pygame.sprite.collide_mask(sprite1, sprite2)
                if collision_area is not None:
                    self.handle_collision_event(
                        sprite1, sprite2, collision_area, callback1, callback2
                    )

    def handle_collision_event(
            self, sprite1, sprite2, collision_area, callback1, callback2
    ):
        # 1) Fire a strongly-typed SpriteCollisionEvent
        evt = SpriteCollisionEvent(sprite1=sprite1,
                                   sprite2=sprite2,
                                   collision_area=collision_area)
        self.event_manager.notify(evt)

        # 2) Also invoke any per-pair callbacks you’d registered
        if callback1 is not None:
            callback1(Collision(sprite1, sprite2, collision_area))
        if callback2 is not None:
            callback2(Collision(sprite1, sprite2, collision_area))



    def _handle_collision_event(
        self, sprite1, sprite2, collision_area, callback1, callback2
    ):
        self.event_manager.notify(
            f"{sprite1.__class__.__name__}_{sprite2.__class__.__name__}_collision",
            [sprite1, sprite2, collision_area],
        )
        if callback1 is not None:
            callback1(Collision(sprite1, sprite2, collision_area))
        if callback2 is not None:
            callback2(Collision(sprite1, sprite2, collision_area))

    def debug(self):
        print("===== CollisionManager Debug =====")
        for collision_group, containers in self.grouped_containers.items():
            print(f"Collision Group: {collision_group}")
            for name, function, _, _ in containers:
                print(f"  - Container: {name}")
                if callable(function):
                    container_result = function()
                    if container_result is not None:
                        num_sprites = len(container_result)
                        print(f"  - Number of Sprites: {num_sprites}")
                    else:
                        print("  - Number of Sprites: Container result is None")
                else:
                    print(
                        "  - Number of Sprites: Unable to determine (function not callable)"
                    )
        print("=================================")
