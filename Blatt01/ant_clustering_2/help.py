import numpy


def neighborhood_function(i):
    L = i.model.grid.get_neighbors(i.pos, moore=True, include_center=False, radius=1)
    sigma2 = 9
    alpha = .5
    sum = 0
    for j in L:
        s = 1 - dist(i, j) / alpha
        if s > 0:
            sum += s
        else:
            return 0.0
    return (1 / sigma2) * sum


def dist(i, j):
    return numpy.linalg.norm(i - j)


def p_pick(i):
    f = neighborhood_function(i)
    if f <= 1.0:
        return 1.0
    return 1 / (f ** 2)


def p_drop(i):
    f = neighborhood_function(i)
    if f >= 1.0:
        return 1.0
    return f ** 4
