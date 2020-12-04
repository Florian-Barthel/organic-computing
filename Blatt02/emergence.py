import entropies


def emergence_particle_x(model):
    return model.start_entropy_particles_x - entropies.entropy_particle_x(
        model)


def emergence_particle_y(model):
    return model.start_entropy_particles_y - entropies.entropy_particle_y(
        model)


def emergence_ant_x(model):
    return model.start_entropy_ants_x - entropies.entropy_ant_x(model)


def emergence_ant_y(model):
    return model.start_entropy_ants_y - entropies.entropy_ant_y(model)


def emergence_particle_type(model):
    return model.start_entropy_particle_type - entropies.entropy_particle_type(
        model)


def emergence_ant_laden(model):
    return model.start_entropy_ant_laden - entropies.entropy_ant_laden(model)
