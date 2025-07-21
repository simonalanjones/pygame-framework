from pygame.locals import *
from classes.config.Input_config import InputConfig
from lib.controller import Controller
from classes.states.game_state import GameState
from classes.events.input_events import (
    LeftInputKeyReleasedEvent,RightInputKeyReleasedEvent,RightInputKeyPressedEvent,LeftInputKeyPressedEvent,FireKeyPressedEvent
)

class InputController(Controller):

    states = (GameState.PLAYING, GameState.PLAYER_DIES)

    def __init__(self):
        super().__init__()
        input_config = InputConfig()
        self.left_key = input_config.get("key_left")
        self.right_key = input_config.get("key_right")
        self.fire_key = input_config.get("key_fire")


        #self.move1_sound = audio_config.get("move1_sound")

    def update(self, events, dt=0):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.notify("escape_button_pressed")

                if event.key == self.left_key:
                    self.notify(LeftInputKeyPressedEvent())

                elif event.key == self.right_key:
                    self.notify(RightInputKeyPressedEvent())

                elif event.key == self.fire_key:
                    self.notify(FireKeyPressedEvent())

                elif event.key == K_F11:
                    pass
                    #self.notify("debug_pressed")

            elif event.type == KEYUP:

                if event.key == K_F12:
                    pass
                    #self.notify("pause_pressed")

                if event.key == self.left_key:  # 'K' key released
                    self.notify(LeftInputKeyReleasedEvent())

                elif event.key == self.right_key:  # 'L' key released
                    self.notify(RightInputKeyReleasedEvent())

            elif event.type == MOUSEBUTTONDOWN:
                pass
                # if event.button == 1:  # 1 is left mouse button
                #     self.notify("mouse_left_clicked", data=event.pos)
                # elif event.button == 3:  # 3 is right mouse button
                #     self.notify("mouse_right_clicked", data=event.pos)
