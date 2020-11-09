from mesa import Agent


class AntAgent(Agent):
    def __init__(self, unique_id, model, step_size, jump_size):
        super().__init__(unique_id, model)
        self.loaded_particle = None
        self.jump_size = jump_size
        self.step_size = step_size

    def step(self):
        if not self.loaded_particle and self.close_particles():
            self.pick_up_particle(self.random.choice(self.close_particles()))
            self.jump()
        elif self.loaded_particle and self.close_particles() and self.empty_neighbors():
            empyt_cell = self.random.choice(self.empty_neighbors())
            self.drop_particle(empyt_cell)
            self.jump()
        else:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=self.step_size
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def close_particles(self):
        particles = []
        neighborhood = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=False,
            radius=self.jump_size
        )
        for neighbor in neighborhood:
            if isinstance(neighbor, ParticleAgent):
                particles.append(neighbor)
        return particles

    def jump(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=self.jump_size
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def pick_up_particle(self, particle):
        self.loaded_particle = particle
        self.model.grid.remove_agent(particle)

    def drop_particle(self, empty_cell):
        self.model.grid.place_agent(self.loaded_particle, empty_cell)
        self.loaded_particle = None

    def empty_neighbors(self):
        empty_cells = []
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=self.step_size
        )
        for cell in neighborhood:
            if self.model.grid.is_cell_empty(cell):
                empty_cells.append(cell)
        return empty_cells


class ParticleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
