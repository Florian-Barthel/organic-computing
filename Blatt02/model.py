from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import AntAgent, ParticleAgent, PARTICLE_TYPE
import entropies
import emergence


def get_num_particles_with_neighbors(model):
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


def get_num_particles_with_neighbors_percent(model):
    num_particles_with_neighbors = get_num_particles_with_neighbors(model)

    return (num_particles_with_neighbors / len(model.free_particles)) * 100


class AntModel(Model):
    """A model with some number of agents."""

    def __init__(self, num_ants, particle_density, step_size, all_in_center,
                 grid_width, grid_height):
        super().__init__()
        self.num_agents = num_ants
        self.grid = MultiGrid(grid_width, grid_height, True)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.schedule = RandomActivation(self)
        self.step_size = step_size
        self.free_particles = []

        num_particles = int(self.grid.width * self.grid.height *
                            particle_density)
        self.num_particles = num_particles

        particles_for_ants = []

        # create particle agents
        for i in range(num_particles):
            p_type = self.random.randrange(3)

            p = ParticleAgent(i, self, PARTICLE_TYPE[p_type])
            self.schedule.add(p)

            if len(particles_for_ants) >= self.num_agents:
                self.grid.place_agent(p, self.grid.find_empty())
                self.free_particles.append(p)
            else:
                particles_for_ants.append(p)

        # Create ant agents
        for i in range(num_particles, num_particles + self.num_agents):
            a = AntAgent(i, self)
            self.schedule.add(a)

            if all_in_center == 'Yes':
                self.grid.place_agent(a, (25, 25))
            else:
                self.grid.place_agent(a, self.grid.find_empty())

            a.storage = particles_for_ants[i - num_particles]  # pick up obj
            a.is_laden = True

        self.datacollector = DataCollector(
            model_reporters={
                "Particles with neighbors percentage":
                    get_num_particles_with_neighbors_percent,
                "Entropy particles x": entropies.entropy_particle_x,
                "Entropy particles y": entropies.entropy_particle_y,
                "Entropy ants x": entropies.entropy_ant_x,
                "Entropy ants y": entropies.entropy_ant_y,
                "Entropy particles type": entropies.entropy_particle_type,
                "Entropy ants laden": entropies.entropy_ant_laden,
                "Emergence particles x": emergence.emergence_particle_x,
                "Emergence particles y": emergence.emergence_particle_y,
                "Emergence ants x": emergence.emergence_ant_x,
                "Emergence ants y": emergence.emergence_ant_y,
                "Emergence particles type": emergence.emergence_particle_type,
                "Emergence ants laden": emergence.emergence_ant_laden
            })

        self.start_entropy_particles_x = entropies.entropy_particle_x(self)
        self.start_entropy_particles_y = entropies.entropy_particle_y(self)
        self.start_entropy_ants_x = entropies.entropy_ant_x(self)
        self.start_entropy_ants_y = entropies.entropy_ant_y(self)
        self.start_entropy_particle_type = entropies.entropy_particle_type(
            self)
        self.start_entropy_ant_laden = entropies.entropy_ant_laden(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
