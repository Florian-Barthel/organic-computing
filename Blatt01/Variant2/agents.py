from mesa import Agent


PARTICLE_TYPE = ['Leaf', 'Nut', 'Stone']


class AntAgent(Agent):
    """Ant agent"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_laden = False
        self.storage = None
        self.debug = False

    def move(self, length):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=length)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        if not self.is_laden and self.is_occupied_by_particle():
            if self.debug:
                print("Agent #" + str(self.unique_id) +
                      " is not laden, picks up object and jumps")
            self.pickup_particle()
            self.move(self.model.jump_size)  # jump j steps in random direction
        elif self.is_laden and self.is_occupied_by_particle():
            if self.debug:
                print("Agent #" + str(self.unique_id) +
                      " is laden, drops object and jumps")
            self.drop_particle_nearby()  # look for empty place and drop obj
            self.move(self.model.jump_size)  # jump j steps in random direction
        else:
            self.move(self.model.step_size)  # make steps in random direction

    def is_occupied_by_particle(self):
        cell_content = self.model.grid.get_cell_list_contents([self.pos])

        if any(isinstance(c, ParticleAgent) for c in cell_content):
            return True
        else:
            return False

    def get_local_particle(self):
        cell_content = self.model.grid.get_cell_list_contents([self.pos])

        return next(filter(lambda c: isinstance(c, ParticleAgent),
                    cell_content))

    def drop_particle_nearby(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        possible_steps = \
            list(filter(lambda c: not isinstance(c, ParticleAgent),
                        possible_steps))

        new_position = self.random.choice(possible_steps)
        self.model.grid.place_agent(self.storage, new_position)
        self.storage = None
        self.is_laden = False

    def pickup_particle(self):
        self.storage = self.get_local_particle()  # pick up obj
        self.model.grid.remove_agent(self.storage)  # remove particle
        self.is_laden = True


class ParticleAgent(Agent):
    """Particle agent"""

    def __init__(self, unique_id, model, particle_type):
        super().__init__(unique_id, model)
        self.particle_type = particle_type
