import numpy as np
import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from blatt1.aufgabe2.ants.agents import AntAgent, ParticleAgent


def get_num_single_particles(model):
    num_single = 0
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            if any(isinstance(c, ParticleAgent) for c in model.grid[x][y]):
                if len(list(filter(lambda i: isinstance(i, ParticleAgent),
                                   model.grid.get_neighbors((x, y), moore=True, include_center=False)))) == 0:
                    num_single += 1
    return num_single / model.num_particles


class AntModel(Model):
    def __init__(self, num_ants, width, height, density, step_size, radius, alpha, init_dist):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.free_particles = []
        self.num_ants = num_ants
        self.step_size = step_size
        assert init_dist in ['random', 'center']
        self.init_dist = init_dist
        self.running = True
        self.num_particles = 0

        self.datacollector = DataCollector(
            model_reporters={
                "percentage of isolated particles": get_num_single_particles
            }
        )

        # Fill with particles
        particle_id = 0
        particle_types = ['stone', 'leave', 'nut']
        for i in range(height):
            for j in range(width):
                if np.random.rand() <= density:
                    particle = ParticleAgent(particle_id, self, random.choice(particle_types))
                    particle_id += 1
                    self.grid.place_agent(particle, (i, j))
                    self.num_particles += 1
                    self.free_particles.append(particle)

        # Create agents
        for i in range(self.num_ants):
            a = AntAgent(i, self, step_size, radius, alpha)
            self.schedule.add(a)
            if self.init_dist is 'random':
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            else:
                x = width // 2
                y = height // 2
            self.grid.place_agent(a, (x, y))
            a.pick_up(random.choice(self.free_particles))

        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
