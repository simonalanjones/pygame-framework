from lib.container import Container


class ShieldContainer(Container):
    def __init__(self):
        super().__init__()

        self.collision_manager.register_group(
            name="shield_collisions",
            function=self.sprites,
            collision_group="shield_collisions",
            callback=self.on_collision,
        )

    def update(self):
        self.collision_manager.check_collisions("shield_collisions")

    def on_collision(self, collision):
        bomb_sprite = collision.extract_sprite_by_class("Bomb")
        shield_sprite = collision.extract_sprite_by_class("Shield")
        missile_sprite = collision.extract_sprite_by_class("PlayerMissile")
        invader_sprite = collision.extract_sprite_by_class("Invader")

        if not shield_sprite:
            return

        # handle collision between invader and shield
        if invader_sprite:
            shield_sprite.invader_damage(invader_sprite)

        # handle collision between player missile and shield
        if missile_sprite and missile_sprite.active:
            self.callback_manager.callback("explode_player_missile")
            shield_sprite.missile_damage(missile_sprite)
            self.callback_manager.callback("remove_player_missile")

        # handle collision between invader bomb and shield
        if bomb_sprite and bomb_sprite.active:
            bomb_sprite.explode()
            shield_sprite.bomb_collision(bomb_sprite)
