from numpy import linalg, asarray


def neighborhood_func(i, j, alt_pos = None):
    """ i = sampled particle, j = all other particles in ant's proximity """

    alpha = 0.1
    sigma_sq = 9.0
    coeff = 1.0 / sigma_sq
    arg_sum = 0.0

    for m in j:

        constraint = (1.0 - (distance_func(i, m, alt_pos) / alpha))

        if constraint > 0:
            arg_sum += constraint
        else:
            return 0.0

    f_i = max(0.0, coeff * arg_sum)

    return f_i


def distance_func(i, m, alt_pos):
    """ i = particle 1, m = particle 2 """

    i_pos = None
    if i.pos is None:
        i_pos = alt_pos
    else:
        i_pos = i.pos

    return linalg.norm(asarray(i_pos) - asarray(m.pos))


def p_pick(i, j):
    """ i = particle 1, j = all other particles in ant's proximity """
    print("test1")
    # k_plus = 0.1
    f_i = neighborhood_func(i, j)

    if f_i <= 1.0:
        return 1.0
    else:
        return 1 / (f_i ** 2)

    # (k_plus / (k_plus + neighborhood_func(i, j))) ** 2


def p_drop(i, j, alt_pos):
    """ i = particle 1, j = all other particles in ant's proximity,
    alt_pos = own position in case i is the currently carried particle with no position """

    # k_minus = 0.3
    f_i = neighborhood_func(i, j, alt_pos)

    if (f_i >= 1.0):
        return 1.0
    else:
        return f_i ** 4

    # (f_i / (k_minus + f_i)) ** 2
