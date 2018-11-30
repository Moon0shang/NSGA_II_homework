import numpy as np

# ZDT


def ZDT_f1(x):

    x_range = [0, 1]
    f = x[0]
    m = 30
    pof = 1
    g = 1 + np.sum(x[1:]) / (m - 1)
    h = 1 - np.sqrt(f / g)

    return x_range, f, h


def ZDT_f2(x):

    x_range = [0, 1]
    f = x[0]
    m = 30
    pof = 1
    g = 1 + np.sum(x[1:]) / (m - 1)
    h = 1 - np.square(f / g)

    return x_range, f, h


def ZDT_f3(x):

    x_range = [0, 1]
    f = x[0]
    m = 10
    pof = 1
    g = 1 + np.sum(x[1:]) / (m - 1)
    h = 1 - np.sqrt(f / g) - np.sqrt(f / g) * np.sin(10 * np.pi * f)

    return x_range, f, h


def ZDT_f4(x):

    x_range = [0, 1]
    f = x[0]
    m = 10
    pof = 1.25
    g = 1 + 10 * \
        (m - 1) + np.sum(np.square(x[1:])) - \
        10 * np.sum(np.cos(4 * np.pi * x[1:]))
    h = 1 - np.sqrt(f / g)

    return x_range, f, h


def ZDT_f5(x):
    x_range = [0, 1, 30, 5]
    m = 11
    pof = 10
    f = 1 +
    # DTLZ


def ZDT_f6(x):

    x_range = [0, 1]
    m = 10
    pof = 1
    f = 1 - np.exp(-4 * x[0]) * np.power(np.sin(6 * np.pi * x[0]), 6)
    g = 1 + 9 * np.power(np.sum(x[1:])/(m-1), 0.25)
    h = 1-np.square(f/g)

    return x_range, f, h


# DTLZ
def DTLZ_f1(x):
