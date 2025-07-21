import pygame
from lib.event_object import EventObject
from lib.collision_manager import CollisionManager


# container for multiple sprites in a group such as invader and shields
class Container(pygame.sprite.Group, EventObject):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        EventObject.__init__(self)
        self.collision_manager = CollisionManager.get_instance()


# container for use with single sprite group such as player and player missile
class ContainerSingle(pygame.sprite.GroupSingle, EventObject):
    def __init__(self):
        pygame.sprite.GroupSingle.__init__(self)
        EventObject.__init__(self)
        self.collision_manager = CollisionManager.get_instance()
