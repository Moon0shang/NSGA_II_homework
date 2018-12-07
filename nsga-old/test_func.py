import numpy as np


# ZDT

def choose_fun(func, opt='func', var_in=None):

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

    if opt == 'init':
        return x_range, m
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

        # for i in range(len(x)):
        #     output[i, 0] = x[i, 0]
        #     g = 1
        #     for j in range(1, m):
        #         g += 9 * x[i, j] / (m - 1)
        #     output[i, 1] = g*(1-np.power(output[i, 0]/g, 0.5))
        # # fx = np.arange(x_range[0], x_range[1], 200)
        # # v_true = 1 - np.sqrt(fx / pof)
        # for i in range(len(x)):
        #     output[i, 0] = x[i, 0]
        #     g = 1 + 9 * np.sum(x[i, 1:]) / (m - 1)
        #     output[i, 1] = 1-np.sqrt(output[i, 0]/g)
        # output[:, 0] = f
        # output[:, 1] = h
        # output[:, 2] = v_true

        return fx, best


def ZDT_f2(opt, x):

    x_range = [0, 1]
    m = 30
    # pof = 1

    if opt == 'init':
        return x_range, m
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

    # if opt:
    #     return x_range, m
    # else:
    #     output = np.empty([len(x), 3])
    #     f = x[:, 0]
    #     g = 1 + 9 * np.sum(x[:, 1:], 1) / (m - 1)
    #     h = 1 - np.square(f / g)
    #     fx = np.arange(x_range[0], x_range[1], 200)
    #     v_true = 1 - np.square(fx / pof)
    #     output[:, 0] = f
    #     output[:, 1] = h
    #     output[:, 2] = v_true

        # return output


def ZDT_f3(opt, x):

    x_range = [0, 1]
    m = 10
    # pof = 1

    if opt == 'init':
        return x_range, m
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

    # if opt:
    #     return x_range, m
    # else:
    #     output = np.empty([len(x), 3])
    #     f = x[:, 0]
    #     g = 1 + 9 * np.sum(x[:, 1:], 1) / (m - 1)
    #     h = 1 - np.sqrt(f / g) - np.sqrt(f / g) * np.sin(10 * np.pi * f)
    #     fx = np.arange(x_range[0], x_range[1], 200)
    #     v_true = h = 1 - np.sqrt(fx / pof) - \
    #         np.sqrt(fx / pof) * np.sin(10 * np.pi * fx)
    #     output[:, 0] = f
    #     output[:, 1] = h
    #     output[:, 2] = v_true
    #     return output


def ZDT_f4(opt, x):

    x_range = [0, 1, -5, 5]
    m = 10
    # pof = 1.25  # global = 1

    if opt == 'init':
        return x_range, m
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

    # if opt:
    #     return x_range, m
    # else:
    #     output = np.empty([len(x), 3])
    #     f = x[:, 0]
    #     g = 1 + 10 * \
    #         (m - 1) + np.sum(np.square(x[:, 1:]), 1) - \
    #         10 * np.sum(np.cos(4 * np.pi * x[:, 1:]), 1)
    #     h = 1 - np.sqrt(f / g)
    #     fx = np.arange(x_range[0], x_range[1], 200)
    #     v_true = 1-np.sqrt(fx/pof)
    #     output[:, 0] = f
    #     output[:, 1] = h
    #     output[:, 2] = v_true
    #     return output


# def ZDT_f5(opt, x):

#     x_range = [0, 30, 0, 5]
#     m = 11
#     pof = 10  # 11

#     if opt:
#         return x_range, m
#     else:
#         # x = []
#         # x.append(np.random.choice([0, 1], 30))
#         f = 1 + x[:, 0]  # np.sum(x[:, 0])
#         # g = 0

#         # for i in range(m - 1):
#         #     # x.append(np.random.choice([0, 1], 5))
#         #     u_x = x[:, 1]  # np.sum(x[i + 1])
#         #     v_x[u_x == 5] = 1
#         #     v_x[ux < 5] = 2 + u_x[ux < 5]

#         # #     if u_x == 5:
#         # #         v_x = 1
#         # #     else:
#         # #         v_x = 2 + u_x
#         #     g += v_x
#         h = 1 / f
#         output[:, 0] = f
#         output[:, 1] = h
#         return output


def ZDT_f6(opt, x):

    x_range = [0, 1]
    m = 10
    # pof = 1

    if opt == 'init':
        return x_range, m
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

    # if opt:
    #     return x_range, m
    # else:
    #     output = np.empty([len(x), 3])
    #     f = 1 - np.exp(-4 * x[:, 0]) * np.power(np.sin(6 * np.pi * x[:, 0]), 6)
    #     g = 1 + 9 * np.power(np.sum(x[:, 1:], 1)/(m-1), 0.25)
    #     h = 1 - np.square(f / g)
    #     fx = np.arange(x_range[0], x_range[1], 200)
    #     v_true = 1-np.sqrt(fx/pof)
    #     output[:, 0] = f
    #     output[:, 1] = h
    #     output[:, 2] = v_true
    #     return output

# DTLZ


def DTLZ_f1(opt, x):
    pass
