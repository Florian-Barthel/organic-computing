from mesa import Agent
import numpy as np
import random


class AntAgent(Agent):
    def __init__(self, unique_id, model, step_size, radius, alpha):
        super().__init__(unique_id, model)
        self.loaded_particle = None
        self.step_size = step_size
        self.radius = radius
        self.alpha = alpha

    def step(self):
        self.move()
        item = self.loaded_particle
        drop = self.p_drop_item(item)
        print(drop)

        if np.random.uniform() <= drop * 100:
            self.drop()
            pick = 0.0
            while np.random.uniform() <= pick * 100:
                if self.close_particles():
                    item = self.random.choice(self.close_particles())
                    pick = self.p_pick_item(self.f(item))
                else:
                    break
            self.pick_up(item)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.step_size
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def p_pick_item(self, item):
        if self.f(item) <= 1.0:
            return 1.0
        else:
            return 1 / (self.f(item) ** 2)

    def p_drop_item(self, item):
        if self.f(item) >= 1.0:
            return 1.0
        else:
            return self.f(item) ** 4

    def f(self, item):
        surrounding_particles = self.close_particles()
        value = 0.0
        for p in surrounding_particles:
            current_value = 1 - item.dissimilarity(p) / self.alpha
            value += current_value
            if current_value <= 0:
                return 0.0
        factor = 1 / ((self.radius * 2 + 1) ** 2)
        return factor * value

    def close_particles(self):
        particles = []
        neighborhood = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.radius
        )
        for neighbor in neighborhood:
            if isinstance(neighbor, ParticleAgent):
                particles.append(neighbor)
        return particles

    def pick_up(self, particle):
        self.loaded_particle = particle
        self.model.grid.remove_agent(particle)

    def drop(self):
        self.model.grid.place_agent(self.loaded_particle, self.pos)
        self.loaded_particle = None


class ParticleAgent(Agent):
    def __init__(self, unique_id, model, particle_type):
        super().__init__(unique_id, model)
        self.particle_type = particle_type

    def dissimilarity(self, particle):
        return 1 - int(particle.particle_type == self.particle_type)