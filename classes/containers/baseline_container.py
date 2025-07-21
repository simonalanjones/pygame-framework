from lib.container import ContainerSingle


class BaselineContainer(ContainerSingle):

    def __init__(self):
        super().__init__()

        self.collision_manager.register_group(
            name="baseline_bomb",
            function=self.sprites,
            collision_group="baseline",
            callback=self.baseline_collision,
            autorun=True,
        )

    def baseline_collision(self, collision):
        bomb_sprite = collision.extract_sprite_by_class("Bomb")
        if bomb_sprite:
            self.sprite.apply_bomb_damage(bomb_sprite)
