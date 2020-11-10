from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from .agent import Ant, Particle


class AntClustering(Model):

    def __init__(self, height, width, ants, density, s, j, distribution):
        """
        parameters:
            height, width: The grid size
            ants: number ants
            density: initial density of particles; probability of grid cells having a particle on them
            s: ant step size during random movement
            j: ant jump distance
            distribution: initial distribution of ants (random or center)
        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.ants = ants
        self.density = density
        self.s = s
        self.j = j
        self.distribution = distribution

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=True)  # cells in MultiGrid can contain more than one object

        # create ants for the model according to number of ants set by user
        for i in range(self.ants):
            if self.distribution == 'random':
                # set x, y coordinates randomly within the grid
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            else:  # distribution == "center"
                x = width // 2
                y = height // 2
            ant = Ant(i, (x, y), s, j, self)
            # place the Ant on the grid at coordinates (x, y)
            self.grid.place_agent(ant, (x, y))
            # add the Ant to the model schedule
            self.schedule.add(ant)

        # Place a particle in each cell with Prob = density
        p_id = 0
        for x in range(width):
            for y in range(height):
                if self.random.random() < self.density:
                    particle = Particle(p_id, self)
                    self.grid.place_agent(particle, (x, y))
                    p_id += 1

        self.running = True

    def step(self):
        self.schedule.step()
