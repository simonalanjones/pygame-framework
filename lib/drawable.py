class Drawable:
    def __init__(self, surface, position=(0, 0), z_index=0, scale=True):
        self.surface = surface
        self.position = position
        self.z_index = z_index
        self.scale = scale  # True means scale with game surface
