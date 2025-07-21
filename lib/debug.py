import pygame

class DebugOverlay:

    _instance = None

    @classmethod
    def get_instance(cls, width=None, height=None):
        # First call must pass width & height
        if cls._instance is None:
            if width is None or height is None:
                raise ValueError(
                    "DebugOverlay not initialized yet; "
                    "you must call get_instance(width, height) first."
                )
            cls._instance = cls(width, height)
        return cls._instance


    def __init__(self, width, height):
        # Guard against __init__ being called multiple times
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("consolas", 12)
        self.watch = []
        self.enabled = True
        self.paused = False

    def add_watch(self, label, getter):
        self.watch.append((label, getter))

    def render(self):
        # Make a semi-transparent overlay surface
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Dark, mostly transparent

        # y = 8
        # for line in self.lines:
        #     text_img = self.font.render(line, True, (255, 255, 80))
        #     overlay.blit(text_img, (10, y))
        #     y += 16  # Line spacing

        for label, getter in self.watch:
            x, y = 10, 10
            value = getter()
            text = f"{label}: {value}"
            img = self.font.render(text, True, (255, 255, 0))
            overlay.blit(img, (x, y))
            y += 18  # Line spacing

        return overlay
