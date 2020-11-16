from numpy import linalg


def neighborhood_func(i, j):
    """ i = sampled particle, j = all other particles in ant's proximity """

    alpha = 1.0
    sigma_sq = 9
    coeff = 1 / sigma_sq
    arg_sum = 0.0

    for m in j:
        constraint = (1 - (distance_func(i, m) / alpha))
        if constraint > 0:
            arg_sum += constraint
        else:
            return 0.0

    f_i = max(0.0, coeff * arg_sum)

    return f_i


def distance_func(i, m):
    """ i = particle 1, m = particle 2 """

    return linalg.norm(i.pos - m.pos)


def p_pick(i, j):
    """ i = particle 1, m = j = all other particles in ant's proximity """

    # k_plus = 0.1
    f_i = neighborhood_func(i, j)

    if f_i <= 1.0:
        return 1.0
    else:
        return 1 / (f_i ** 2)

    # (k_plus / (k_plus + neighborhood_func(i, j))) ** 2


def p_drop(i, j):
    """ i = particle 1, m = j = all other particles in ant's proximity """

    # k_minus = 0.3
    f_i = neighborhood_func(i, j)

    if (f_i >= 1.0):
        return 1.0
    else:
        return f_i ** 4

    # (f_i / (k_minus + f_i)) ** 2
