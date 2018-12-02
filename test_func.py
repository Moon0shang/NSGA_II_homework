import numpy as np


# ZDT

def choose_fun(func, init=False, var_in=None):

    if func == 'ZDT_1':
        return ZDT_f1(init, x)
    elif func == 'ZDT_2':
        return ZDT_f2(init, x)
    elif func == 'ZDT_3':
        return ZDT_f3(init, x)
    elif func == 'ZDT_4':
        return ZDT_f4(init, x)
    elif func == 'ZDT_5':
        return ZDT_f5(init, x)
    elif func == 'ZDT_6':
        return ZDT_f6(init, x)


def ZDT_f1(init, x):

    x_range = [0, 1]
    m = 30
    pof = 1

    if init:
        return x_range, m
    else:
        f = x[0]
        g = 1 + np.sum(x[1:]) / (m - 1)
        h = 1 - np.sqrt(f / g)

        return f, h


def ZDT_f2(init, x):

    x_range = [0, 1]
    m = 30
    pof = 1

    if init:
        return x_range, m
    else:
        f = x[0]
        g = 1 + np.sum(x[1:]) / (m - 1)
        h = 1 - np.square(f / g)
        return f, h


def ZDT_f3(init, x):

    x_range = [0, 1]
    m = 10
    pof = 1

    if init:
        return x_range, m
    else:
        f = x[0]
        g = 1 + np.sum(x[1:]) / (m - 1)
        h = 1 - np.sqrt(f / g) - np.sqrt(f / g) * np.sin(10 * np.pi * f)
        return f, h


def ZDT_f4(init, x):

    x_range = [0, 1, -5, 5]
    m = 10
    pof = 1.25  # global = 1

    if init:
        return x_range, m
    else:
        f = x[0]
        g = 1 + 10 * \
            (m - 1) + np.sum(np.square(x[1:])) - \
            10 * np.sum(np.cos(4 * np.pi * x[1:]))
        h = 1 - np.sqrt(f / g)
        return f, h


def ZDT_f5(init, x):

    x_range = [0, 30, 0, 5]
    m = 11
    pof = 10  # 11

    if init:
        return x_range, m
    else:
        # x = []
        # x.append(np.random.choice([0, 1], 30))
        f = 1 + x[0]  # np.sum(x[0])
        g = 0
        for i in range(m - 1):
            # x.append(np.random.choice([0, 1], 5))
            u_x = x  # np.sum(x[i + 1])
            if u_x == 5:
                v_x = 1
            else:
                v_x = 2 + u_x
            g += v_x
        h = 1 / f
        return f, h


def ZDT_f6(init, x):

    x_range = [0, 1]
    m = 10
    pof = 1

    if init:
        return x_range, m
    else:
        f = 1 - np.exp(-4 * x[0]) * np.power(np.sin(6 * np.pi * x[0]), 6)
        g = 1 + 9 * np.power(np.sum(x[1:])/(m-1), 0.25)
        h = 1-np.square(f/g)
        return f, h

# DTLZ


def DTLZ_f1(init, x):
    pass
