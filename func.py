import numpy as np


# ZDT

def functions(func, opt='func', var_in=None):
    """
    opt args: default is func to calculate values
        init, to get the function args
        func, to calculate the values of function
        best, to get the best values
    """

    if func == 'ZDT_1':
        return ZDT_f1(opt, var_in)
    elif func == 'ZDT_2':
        return ZDT_f2(opt, var_in)
    elif func == 'ZDT_3':
        return ZDT_f3(opt, var_in)
    elif func == 'ZDT_4':
        return ZDT_f4(opt, var_in)
    elif func == 'ZDT_5':
        print('this function will not be tested')
        # return ZDT_f5(opt, var_in)
    elif func == 'ZDT_6':
        return ZDT_f6(opt, var_in)
    else:
        print('wrong function name has input')


def ZDT_f1(opt, x):

    x_range = [0, 1]
    m = 30
    dim = 2

    if opt == 'init':
        return x_range, m, dim
    elif opt == 'func':
        output = np.empty([len(x), 2])
        output[:, 0] = x[:, 0]
        g = 1 + 9 * np.sum(x[:, 1:], 1) / (m - 1)
        output[:, 1] = g * (1 - np.sqrt(output[:, 0] / g))
        return output
    elif opt == 'best':
        fx = np.arange(x_range[0], x_range[1], 0.005)
        g = 1
        best = g * (1 - np.sqrt(fx / g))

        return fx, best


def ZDT_f2(opt, x):

    x_range = [0, 1]
    m = 30
    dim = 2

    if opt == 'init':
        return x_range, m, dim
    elif opt == 'func':
        output = np.empty([len(x), 2])
        output[:, 0] = x[:, 0]
        g = 1 + 9 * np.sum(x[:, 1:], 1) / (m - 1)
        output[:, 1] = g * (1 - np.square(output[:, 0] / g))
        return output
    elif opt == 'best':
        fx = np.arange(x_range[0], x_range[1], 0.005)
        g = 1
        best = g * (1 - np.square(fx / g))

        return fx, best


def ZDT_f3(opt, x):

    x_range = [0, 1]
    m = 10
    dim = 2

    if opt == 'init':
        return x_range, m, dim
    elif opt == 'func':
        output = np.empty([len(x), 2])
        output[:, 0] = x[:, 0]
        g = 1 + 9 * np.sum(x[:, 1:], 1) / (m - 1)
        output[:, 1] = g * (1 - np.sqrt(output[:, 0] / g) -
                            np.sqrt(output[:, 0] / g) * np.sin(10 * np.pi * output[:, 0]))
        return output
    elif opt == 'best':
        fx = np.arange(x_range[0], x_range[1], 0.005)
        g = 1
        best = g * (1 - np.sqrt(fx / g) - np.sqrt(fx / g)
                    * np.sin(10 * np.pi * fx))

        return fx, best


def ZDT_f4(opt, x):

    x_range = [0, 1, -5, 5]
    m = 10
    dim = 2

    if opt == 'init':
        return x_range, m, dim
    elif opt == 'func':
        output = np.empty([len(x), 2])
        output[:, 0] = x[:, 0]
        g = 1 + 10 * \
            (m - 1) + np.sum(np.square(x[:, 1:]), 1) - \
            10 * np.sum(np.cos(4 * np.pi * x[:, 1:]), 1)
        output[:, 1] = g * (1 - np.sqrt(output[:, 0] / g))
        return output
    elif opt == 'best':
        fx = np.arange(x_range[0], x_range[1], 0.005)
        g = 1.25  # 1
        best = g * (1 - np.sqrt(fx / g))

        return fx, best


def ZDT_f6(opt, x):

    x_range = [0, 1]
    m = 10
    dim = 2

    if opt == 'init':
        return x_range, m, dim
    elif opt == 'func':
        output = np.empty([len(x), 2])
        output[:, 0] = 1 - np.exp(-4 * x[:, 0]) * \
            np.power(np.sin(6 * np.pi * x[:, 0]), 6)
        g = 1 + 9 * np.power(np.sum(x[:, 1:], 1)/(m-1), 0.25)
        output[:, 1] = g * (1 - np.sqrt(output[:, 0] / g))
        return output
    elif opt == 'best':
        xx = np.arange(x_range[0], x_range[1], 0.005)
        fx = 1 - np.exp(-4 * xx) * np.power(np.sin(6 * np.pi * xx), 6)
        g = 1
        best = g * (1 - np.sqrt(fx / g))

        return fx, best


# DTLZ
def DTLZ_f1(opt, x):
    pass
