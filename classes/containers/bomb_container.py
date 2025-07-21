from lib.container import Container


class BombContainer(Container):
    def __init__(self):
        super().__init__()

        self.callback_manager.register_callback("get_bombs", self.get_bombs)

        # we let the shield container handle the collisions
        # with bombs as it needs to sync the shield eroding
        self.collision_manager.register_group(
            name="shield_collisions",
            function=self.get_bombs,
            collision_group="shield_collisions",
        )

        # we let the player container handle the collision
        self.collision_manager.register_group(
            name="bomb_player",
            function=self.get_bombs,
            collision_group="player",
        )

        self.collision_manager.register_group(
            name="bomb_baseline",
            function=self.get_bombs,
            collision_group="baseline",
        )

    def update(self):
        # Update all bomb sprites in this container
        for sprite in self.sprites():
            sprite.update()

    def get_bombs(self):
        return [bomb for bomb in self.sprites() if bomb.active]

    def has_rolling_shot(self):
        return any(bomb.bomb_type == "rolling" for bomb in self.sprites())
