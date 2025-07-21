import pygame, os
from pygame.locals import QUIT
from lib.system import System


def main():
    pygame.init()
    system = System.get_instance()

    # Reserve a channel (won’t be used automatically)
    #pygame.mixer.set_reserved(1)

    # Play a sound on a named channel
    #channel = pygame.mixer.Channel(5)
    #channel.play(shot_sound)

    BASE_DIR = os.path.dirname(__file__)
    sound_path = os.path.join(BASE_DIR, 'sounds', 'move1.wav')
    shot_sound = pygame.mixer.Sound(sound_path)
    # Play it once
    shot_sound.play()

    max_fps = 60
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(max_fps) / 1000.0  # Delta time in seconds


        pygame.display.set_caption(f"Pyframe FPS: {int(clock.get_fps())}")

        events = [event for event in pygame.event.get()]
        for event in events:
            if event.type == QUIT:
                running = False

        system.update(events, dt)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
