import agents
import math


def get_pos_entropy(model, max_size, agent_type, pos_index):
    filtered_agents = list(filter(lambda a: type(a) is agent_type and a.pos is not None, model.schedule.agents))
    entropy_sum = 0
    x_distribution = [0] * (max_size - 1)

    for p in filtered_agents:
        x_distribution[p.pos[pos_index] - 1] += 1

    for x in x_distribution:
        entropy_sum += calc_shannon_entropy_element(x, max_size)

    return -entropy_sum


def get_similar_surrounding_particles(model, agent):
    cell_contents = model.grid.get_neighbors(
        agent.pos,
        moore=True,
        include_center=False,
        radius=1)

    return list(filter(lambda c: isinstance(c, agents.ParticleAgent) and c.particle_type is agent.particle_type,
                       cell_contents))


def entropy_particle_x(model):
    return get_pos_entropy(model, model.grid_width, agents.ParticleAgent, 0)


def entropy_particle_y(model):
    return get_pos_entropy(model, model.grid_height, agents.ParticleAgent, 1)


def entropy_particle_type(model):
    particles = list(filter(lambda a: type(a) is agents.ParticleAgent and a.pos is not None, model.schedule.agents))
    entropy_sum = 0
    ptype_distribution = [0] * 9  # Moore -> max. 8 neighbors -> including 0 neighbors equals 9 options

    for p in particles:
        similar_particles = get_similar_surrounding_particles(model, p)
        seen_pos = []
        for sp in similar_particles:
            if sp.pos in seen_pos:
                similar_particles.remove(sp)
            else:
                seen_pos.append(sp.pos)

        num_similar_particles = len(similar_particles)
        ptype_distribution[num_similar_particles] += 1

    for ptype in ptype_distribution:
        entropy_sum += calc_shannon_entropy_element(ptype, len(particles))

    return -entropy_sum


def entropy_ant_x(model):
    return get_pos_entropy(model, model.grid_width, agents.AntAgent, 0)


def entropy_ant_y(model):
    return get_pos_entropy(model, model.grid_height, agents.AntAgent, 1)


def entropy_ant_laden(model):
    ants = list(filter(lambda a: type(a) is agents.AntAgent, model.schedule.agents))
    entropy_sum = 0
    laden_distribution = [0] * 2  # Laden or not laden

    for a in ants:
        laden_distribution[int(a.is_laden)] += 1

    for laden in laden_distribution:
        entropy_sum += calc_shannon_entropy_element(laden, len(ants))

    return -entropy_sum


def calc_shannon_entropy_element(count, total):
    if count == 0 or total == 0:
        return 0
    fraction = count / total
    return fraction * math.log2(fraction)
