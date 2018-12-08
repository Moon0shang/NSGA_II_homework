import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from NSGA_II import NSGA_Core


def run(pop_num, gen, prob, yita, func):
    NC = NSGA_Core(pop_num, prob, yita, func)
    pop = NC.initialize()
    print('test')
    # pop = NC.sort_dis()
    # for i in range(gen):
    #     parents = NC.tournament()
    #     new_pop = NC.cross_mutate()
    #     pop = NC.elitism()
    values = pop[:, NC.x_num:(NC.x_num+NC.dim)]
    visualize(values, NC.dim)


def visualize(values, dim):

    if dim == 2:

        # fx, best = choose_fun(func, opt='best')
        plt.scatter(values[:, 0], values[:, 1], color='g', marker='o')
        plt.show()
    else:
        fig = plt.figure()
        ax = fig.subplot('111', 'project3d')
        ax.scatter(values[:, 0], values[:, 1],
                   values[:, 2], color='g', marker='o')
        plt.show()


if __name__ == "__main__":

    generation = 100
    pop_num = 100

    prob_c = 0.9
    prob_m = 0.4
    prob = [prob_c, prob_m]

    # the ditribution is narrow when yita_c is largeer
    yita_c = 20
    # the parent and offspring are more different when yita_m is smaller
    yita_m = 20
    yita = [yita_c, yita_m]

    func = [['ZDT_1', 'ZDT_2', 'ZDT_3', 'ZDT_4', 'ZDT_5', 'ZDT_6'],
            ['DTLZ_1', 'DTLZ_1', 'DTLZ_1']]

    run(pop_num, generation, prob, yita, func[0][0])
