from mesa import Agent
from functions import p_drop, p_pick


PARTICLE_TYPE = ['Leaf', 'Nut', 'Stone']


class AntAgent(Agent):
    """Ant agent"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.is_laden = False
        self.storage = None
        self.debug = True

    def move(self, length):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=length)

        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move(self.model.step_size)  # make steps in random direction

        drop_item = p_drop(self.storage, self.get_all_surrounding_particles(), self.pos)
        # print(drop_item)

        if drop_item > 0:
            if self.debug:
                print("Agent #" + str(self.unique_id) +
                      " wants to drop item")

            if not self.is_occupied_by_particle():
                self.drop_particle_locally()
            else:
                self.drop_particle_nearby()

            pick = 0
            while pick > 0:
                print("test")
                p_rnd_tgt = self.get_random_particle()  # get random particle
                print("test2")
                self.model.grid.move_agent(self, p_rnd_tgt.pos)  # jump to particle
                print("RndP: " + str(p_rnd_tgt))
                pick = p_pick(p_rnd_tgt, self.get_all_surrounding_particles())
                print(pick)

            self.pickup_particle()

    def is_occupied_by_particle(self):
        cell_content = self.model.grid.get_cell_list_contents([self.pos])

        if any(isinstance(c, ParticleAgent) for c in cell_content):
            return True
        else:
            return False

    def get_local_particle(self):
        return next(self.get_all_local_particles)

    def get_all_surrounding_particles(self):
        cell_contents = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=True)

        return list(filter(lambda c: isinstance(c, ParticleAgent),
                    cell_contents))

    def drop_particle_nearby(self):  # if center-spot is first, then combine functions
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        possible_steps = \
            list(filter(lambda c: not isinstance(c, ParticleAgent),
                        possible_steps))

        new_position = self.random.choice(possible_steps)
        self.model.grid.place_agent(self.storage, new_position)
        self.model.free_particles.append(self.storage)
        self.storage = None
        self.is_laden = False

    def drop_particle_locally(self):
        self.model.grid.place_agent(self.storage, self.pos)
        self.model.free_particles.append(self.storage)
        self.storage = None
        self.is_laden = False

    def pickup_particle(self):
        self.storage = self.get_local_particle()  # pick up obj
        self.model.grid.remove_agent(self.storage)  # remove particle
        self.is_laden = True
        self.model.free_particles.remove(self.storage)

    def get_random_particle(self):
        return self.model.free_particles[self.random.randrange(len(self.model.free_particles))]


class ParticleAgent(Agent):
    """Particle agent"""

    def __init__(self, unique_id, model, particle_type):
        super().__init__(unique_id, model)
        self.particle_type = particle_type
