from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import AntAgent, ParticleAgent


def get_num_particles_with_neigbors(model):
    all_particles = list(filter(lambda a: type(a) is ParticleAgent,
                                model.schedule.agents))

    num_particles_with_neighbors = 0

    for p in all_particles:
        if p.pos is None:
            continue

        num_local_neighbors = 0

        for n in model.grid.get_neighbors(p.pos, radius=1, moore=True,
                                          include_center=False):
            if n is not None and type(n) is ParticleAgent:
                num_local_neighbors += 1

        if num_local_neighbors >= 2:
            num_particles_with_neighbors += 1

    return num_particles_with_neighbors


def get_num_particles_with_neigbors_percent(model):
    num_particles_with_neighbors = get_num_particles_with_neigbors(model)
    num_total_particles = len(list(filter(lambda a: type(a) is ParticleAgent,
                                          model.schedule.agents)))

    return (num_particles_with_neighbors / num_total_particles) * 100


class AntModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, particle_density, step_size, jump_size,
                 all_in_center):
        super().__init__()
        self.num_agents = N
        self.grid = MultiGrid(50, 50, True)
        self.schedule = RandomActivation(self)
        self.step_size = step_size
        self.jump_size = jump_size
        self.iteration_counter = 0

        # Create agents
        for i in range(self.num_agents):
            a = AntAgent(i, self)
            self.schedule.add(a)

            if (all_in_center):
                x = 25
                y = 25
            else:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        num_particles = self.grid.width * self.grid.height * particle_density
        self.num_particles = num_particles

        for i in range(self.num_agents, self.num_agents + int(num_particles)):
            p = ParticleAgent(i, self)
            self.schedule.add(p)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(p, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Particles with neighbors": get_num_particles_with_neigbors,
                             "Particles with neighbors percentage": get_num_particles_with_neigbors_percent})

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.iteration_counter += 1
        if self.iteration_counter == 5000:
            exit(0)
