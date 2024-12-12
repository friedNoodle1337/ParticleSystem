import random

import glm

from particles.emitter import Emitter
from particles.particle import Particle


class PointEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime):
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range  # (min_speed, max_speed)
        self.size_range = size_range  # (min_size, max_size)
        # Нормализуем цвет, если он задан в диапазоне [0, 255]
        self.color = glm.vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0)
        self.lifetime = lifetime

    def emit_particle(self):
        # Начальная скорость с уменьшением по мере удаления
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        direction = glm.vec3(
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0)
        )
        direction = glm.normalize(direction)
        velocity = direction * speed
        size = random.uniform(self.size_range[0], self.size_range[1])
        return Particle(
            position=self.position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=True
        )
