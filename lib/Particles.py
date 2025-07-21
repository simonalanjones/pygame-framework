import math
import random
import pygame
from lib.Physics_object import PhysicsObject


class Particle(PhysicsObject):
    def __init__(self, position, rotation):

        # print(rotation)
        self.position = position

        adjusted_rotation = (
            rotation - math.pi / 2
        )  # Adjusting rotation by 90 degrees counter-clockwise
        velocity = {
            "speed": 20,
            "direction": adjusted_rotation,
        }  # Fixed speed and direction based on rotation

        acceleration = 0
        max_speed = 20
        friction = 0.98  # No friction for the missile
        mass = 0.1

        super().__init__(
            position, velocity, acceleration, rotation, 0, max_speed, friction, mass
        )
        self.image = pygame.image.load("graphics/circle.png")

        self.rect = self.image.get_rect(center=(self.position["x"], self.position["y"]))
        self.original_image = self.image

        self.hit_rect = pygame.Rect(0, 0, 8, 24)
        self.hit_rect.center = self.rect.center

        self.vx = 0
        self.vy = 0

        self.acceleration = 0.7  # Acceleration due to thrust
        self.gravity = 0.7  # Gravity affecting the particle
        self.thrust_power = 0.6  # Power of thrust
        self.mass = 0.4
        self.timer = random.randint(1, 4)

    def update(self):
        self.update_physics()
        self.timer -= 0.5

        if self.timer <= 0:
            self.kill()


class ExhaustParticle(Particle):
    def __init__(self, position, rotation):
        super().__init__(position, rotation)
        self.velocity["direction"] = (self.velocity["direction"] + math.pi) % (
            2 * math.pi
        )


class ParticleEmitter:
    def __init__(self):
        self.particle_container = ParticleContainer()

    def update(self):
        self.particle_container.update()

    # def create_particle(self, position, rotation, **kwargs):
    #     """
    #     Create a particle. To be overridden by subclasses for custom functionality.

    #     :param position: Starting position of the particle.
    #     :param rotation: Initial rotation of the particle.
    #     :param kwargs: Additional parameters for customization.
    #     :return: A new Particle instance.
    #     """
    #     raise NotImplementedError("Subclasses should implement this method.")

    # def emit(self, position, rotation, **kwargs):
    #     """
    #     Emit a particle at a given position and rotation.

    #     :param position: Starting position of the particle.
    #     :param rotation: Initial rotation of the particle.
    #     :param kwargs: Additional parameters for customization.
    #     """
    #     particle = self.create_particle(position, rotation, **kwargs)
    #     self.particle_container.add(particle)

    def emit(self, position, rotation):
        particle = Particle(position, rotation)
        self.particle_container.add(particle)

    def get_particles(self):
        return self.particle_container.sprites()


class ExhaustEmitter(ParticleEmitter):
    def __init__(self):
        super().__init__()

    def emit(self, position, rotation):
        particle = ExhaustParticle(position, rotation)
        # particle.velocity["direction"] = (self.velocity["direction"] + math.pi) % (
        #     2 * math.pi
        # )
        self.particle_container.add(particle)


class ParticleContainer(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self):
        # super().update()

        return
        for particle in self.sprites():
            if particle.timer <= 0:
                particle.kill()


class ExhaustParticleEmitter:
    def __init__(self, position):
        self.position = position
        self.particle_container = ParticleContainer()

    def update(self):
        self.particle_container.update()

    def get_particles(self):
        return self.particle_container.sprites()

    def emit(self, rotation, **kwargs):
        """
        Emit particles from the emitter's position with given rotation.

        :param rotation: Initial rotation of the particles.
        :param kwargs: Additional parameters for customization.
        """
        particles = self.create_particle(self.position, rotation, **kwargs)
        if isinstance(particles, list):
            for p in particles:
                self.particle_container.add(p)
        else:
            self.particle_container.add(particles)

    def create_particle(self, position, rotation, **kwargs):
        """
        Create a particle at the emitter's position.

        :param position: Starting position of the particle (emitter's position).
        :param rotation: Initial rotation of the particle.
        :param kwargs: Additional parameters for customization.
        :return: A Particle instance or a list of Particle instances.
        """
        return Particle(position, rotation)
