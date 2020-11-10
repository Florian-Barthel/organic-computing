from mesa import Agent


class Ant(Agent):

    def __init__(self, unique_id, pos, s, j, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.s = s
        self.j = j
        self.carrying_particle = None

    def step(self):
        """
        Pick up particle, move and drop particle. Repeat.
        """
        close_particles = self.particles_on_neighbouring_cells()
        if self.carrying_particle is None and close_particles:
            self.pick_up_particle(self.random.choice(close_particles))
            self.random_move(self.j)
        elif self.carrying_particle and close_particles:
            empty_place_nearby = self.get_empty_place_nearby(self.random.choice(close_particles))
            self.drop_particle(empty_place_nearby)
            self.random_move(self.j)
        else:
            self.random_move(self.s)

    def random_move(self, distance):
        """
        Move the given distance in any allowable direction.
        """
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=distance)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def particles_on_neighbouring_cells(self):
        """
        Returns a list of particles on neighbouring cells (Moore neighbourhood with radius 1).
        """
        particles = []
        neighbours = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        for n in neighbours:
            if isinstance(n, Particle):
                particles.append(n)
        return particles

    def get_empty_place_nearby(self, particle):
        empty_neighbours = []
        neighbourhood = self.model.grid.get_neighborhood(particle.pos, moore=True, include_center=False, radius=1)
        for cell in neighbourhood:
            if self.model.grid.is_cell_empty(cell):
                empty_neighbours.append(cell)
        empty_place_nearby = self.random.choice(empty_neighbours)  # What if list is empty??
        return empty_place_nearby

    def pick_up_particle(self, particle):
        self.carrying_particle = particle
        self.model.grid.remove_agent(particle)

    def drop_particle(self, cell):
        self.model.grid.place_agent(self.carrying_particle, cell)
        self.carrying_particle = None


class Particle(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
