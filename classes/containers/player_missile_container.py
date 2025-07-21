import pygame
from lib.container import Container

from classes.models.player_missile_explosion import PlayerMissileExplosion
from classes.models.player_missile import PlayerMissile


class PlayerMissileContainer(Container):
    def __init__(self):
        super().__init__()
        self.countdown = 0

        self.register_callbacks()
        self.register_collision_groups()


    def add_missile_sprite(self, params):
        player_missile = PlayerMissile(params)
        self.add(player_missile)

    def add_missile_explosion_sprite(self, player_missile):
        x = player_missile.rect.x - 4
        y = player_missile.rect.y
        explosion_sprite = PlayerMissileExplosion(x, y)
        self.add(explosion_sprite)

    def find_sprite_by_class(self, class_name):
        for sprite in self.sprites():
            if sprite.__class__.__name__ == class_name:
                return sprite
        return None

    def find_missile_sprite(self):
        return self.find_sprite_by_class("PlayerMissile")

    def find_missile_explosion(self):
        return self.find_sprite_by_class("PlayerMissileExplosion")

    def update(self):
        self.collision_manager.check_collisions("targets")

        missile_explosion = self.find_missile_explosion()
        if missile_explosion:
            missile_explosion.update()

        # move this into an update method when code is good
        missile_sprite = self.find_missile_sprite()
        if missile_sprite:
            missile_sprite.move_up()  # Move the missile vertically upwards
            if missile_sprite.get_y_position() <= 42:
                missile_sprite.explode()
                self.add_missile_explosion_sprite(missile_sprite)

            return missile_sprite.update()





    # this is a callback which handles the switching of sprites
    def explode_player_missile(self):
        player_missile = self.find_missile_sprite()
        if player_missile:
            self.add_missile_explosion_sprite(player_missile)

    # removing of main missile
    def remove_player_missile(self):
        player_missile = self.find_missile_sprite()
        if player_missile:
            player_missile.explode()

    def missile_sprite_group(self):
        missile_group = pygame.sprite.GroupSingle()
        missile_group.add(self.find_missile_sprite())
        return missile_group

    def on_collision(self, collision):
        bomb_sprite = collision.extract_sprite_by_class("Bomb")
        invader_sprite = collision.extract_sprite_by_class("Invader")
        mothership_sprite = collision.extract_sprite_by_class("Mothership")

        if mothership_sprite and self.find_missile_sprite().active:
            mothership_sprite.explode()
            self.empty()

        if bomb_sprite and self.find_missile_sprite().active:
            bomb_sprite.explode()
            self.find_missile_sprite().kill()

        if invader_sprite:
            self.event_manager.notify("invader_hit", invader_sprite)
            self.empty()  # dont need missile or explosion sprite for this use case

        # bomb_sprite = collision.extract_sprite_by_class("Bomb")
        # shield_sprite = collision.extract_sprite_by_class("Shield")

        # if bomb_sprite != None:
        #     bomb_sprite.explode()

        # if shield_sprite != None and bomb_sprite != None:
        #     shield_sprite.bomb_collision(bomb_sprite)




    def register_callbacks(self):
        self.callback_manager.register_callback(
            "get_player_missile", self.find_missile_sprite
        )
        self.callback_manager.register_callback(
            "get_player_missile_explosion", self.find_missile_explosion
        )
        self.callback_manager.register_callback(
            "explode_player_missile", self.explode_player_missile
        )
        self.callback_manager.register_callback(
            "remove_player_missile", self.remove_player_missile
        )

    def register_collision_groups(self):

        # register missile sprite subgroup with "shield_collisions"
        self.collision_manager.register_group(
            name="shield_collisions",
            function=self.missile_sprite_group,
            collision_group="shield_collisions",
        )

        # register missile sprite subgroup with "targets"
        self.collision_manager.register_group(
            name="targets",
            function=self.missile_sprite_group,
            collision_group="targets",  # invaders/mothership/bombs
            callback=self.on_collision,
        )
