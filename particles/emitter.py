from abc import ABC, abstractmethod
from typing import List

import glm

from materials.shader import Shader
from particles.particle import Particle


class Emitter(ABC):
    def __init__(self, position, emission_rate, max_particles, acceleration=None):
        self.position = glm.vec3(*position)
        self.emission_rate = emission_rate  # Частота эмиссии (частиц в секунду)
        self.max_particles = max_particles
        self.particles: List[Particle] = []
        self.accumulator = 0.0  # Накопитель времени

        self.acceleration = [0.0, -9.81, 0.0] if acceleration is None else acceleration

    @abstractmethod
    def emit_particle(self):
        pass

    def update(self, delta_time):
        # Эмиссия новых частиц
        self.accumulator += self.emission_rate * delta_time
        particles_to_emit = int(self.accumulator)

        for _ in range(particles_to_emit):
            if len(self.particles) < self.max_particles:
                self.particles.append(self.emit_particle())

        self.accumulator -= particles_to_emit

        # Обновление существующих частиц
        alive_particles = []
        for particle in self.particles:
            particle.update(delta_time, self.acceleration)
            if particle.is_alive():
                alive_particles.append(particle)
        self.particles = alive_particles

    def render(self, shader: Shader):
        for particle in self.particles:
            particle.render(shader)
