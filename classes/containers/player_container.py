# classes/containers/player_container.py

from lib.container import ContainerSingle
from classes.models.player import Player
from classes.events.player_events import PlayerDiedEvent
from classes.events.game_events import GameplayStartEvent


class PlayerContainer(ContainerSingle[Player]):
    def __init__(self):
        super().__init__()

        self.sprite = Player({
            "player_x_position": 10,
            "player_y_position": 219,
        })
        self.active = False
        self.has_collided = False

        self.collision_manager.register_group(
            name="player",
            function=self.sprites,
            collision_group="player",
            callback=self.on_player_collision,
            autorun=True,
        )

        self.callback_manager.register_callback("get_player", self.get_player)
        self.event_manager.add_listener(GameplayStartEvent, self.on_gameplay_start)


    def on_gameplay_start(self, _):
        self.active = True


    def activate(self, x=10, y=219):
        self.sprite.rect.topleft = (x, y)
        #self.active = True
        self.has_collided = False

    def get_player(self):
        return self.sprite if self.active else None

    def update(self, left_key_pressed, right_key_pressed, dt):
        if self.active and not self.has_collided:
            if left_key_pressed:
                self.sprite.move_left(dt)
            elif right_key_pressed:
                self.sprite.move_right(dt)
        if self.get_player():
            self.sprite.update()


    def on_player_collision(self, collision):
        if self.active and not self.has_collided:
            print('player dies')
            self.get_player().explode()
            bomb_sprite = collision.extract_sprite_by_class("Bomb")
            if bomb_sprite:
                bomb_sprite.explode()

            self.event_manager.notify(PlayerDiedEvent())
            self.has_collided = True
