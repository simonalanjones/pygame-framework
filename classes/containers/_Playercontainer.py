from lib.container import ContainerSingle
from classes.models.player import Player

player_speed = 1


class PlayerContainer(ContainerSingle):

    def __init__(self):
        super().__init__()
        #self.sprite = Player({"player_x_position": 10, "player_y_position": 219})

        self.has_collided = False

        self.collision_manager.register_group(
            name="player",
            function=self.sprites,
            collision_group="player",
            callback=self.on_player_collision,
            autorun=True,
        )

        # not currently used but will be for bombs that target player
        # suggest we store where it was called from as part of debug
        # that way we can trace where/if our callbacks are getting used and by who
        self.callback_manager.register_callback("get_player", self.get_player)

    def get_player(self):
        return self.sprite

    def move_left(self):
        self.sprite.rect.x -= player_speed

    def move_right(self):
        self.sprite.rect.x += player_speed

    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def update(self):
        if self.sprite:
            self.sprite.update()

    def update_movement(self, left_key_pressed, right_key_pressed):
        if not self.has_collided:
            if left_key_pressed:
                self.move_left()
            elif right_key_pressed:
                self.move_right()

    # def spawn_player(self):
    #     if not self.sprite:
    #         params = {
    #             "player_x_position": 10,
    #             "player_y_position": 219,
    #         }
    #         self.sprite = Player(params)
    #         self.has_collided = False

    def on_player_collision(self, collision):
        # only allow one player collision
        if not self.has_collided:
            bomb_sprite = collision.extract_sprite_by_class("Bomb")
            if bomb_sprite != None:
                bomb_sprite.explode()

            self.event_manager.notify("player_explodes")
            self.has_collided = True
