from numpy import linalg, asarray


def neighborhood_func(i, j):
    """ i = sampled particle, j = all other particles in ant's proximity """

    alpha = 0.9
    sigma_sq = 9.0
    coeff = 1.0 / sigma_sq
    arg_sum = 0.0

    for m in j:

        constraint = (1.0 - (dissimilarity_func(i, m) / alpha))

        if constraint > 0:
            arg_sum += constraint
        else:
            return 0.0

    f_i = max(0.0, coeff * arg_sum)

    return f_i


def dissimilarity_func(i, m):
    """ i = particle 1, m = particle 2 """

    return 1 - int(i.particle_type == m.particle_type)


def p_pick(i, j):
    """ i = particle 1, j = all other particles in ant's proximity """

    f_i = neighborhood_func(i, j)

    if f_i <= 1.0:
        return 1.0
    else:
        return 1 / (f_i ** 2)


def p_drop(i, j, alt_pos):
    """ i = particle 1, j = all other particles in ant's proximity """

    f_i = neighborhood_func(i, j)

    if f_i >= 1.0:
        return 1.0
    else:
        return f_i ** 4
