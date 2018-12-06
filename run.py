import numpy as np
import matplotlib.pyplot as plt
import time

from test_func import choose_fun
from NSGA_II import NSGA_II


def run(pop, gen, x_range, dim, prob, yita, func):

    pop_num = pop.shape[0]
    NSGA = NSGA_II(pop_num, prob, yita, x_range)
    # values = np.empty((pop_num, dim))

    plt.ion()
    for i in range(gen):

        values = choose_fun(func, var_in=pop)
        Usort, dis, rank = NSGA.dis_sort(values, dim)
        parent = NSGA.select(pop, dis, rank)
        cross_pop = NSGA.cross(parent)

        find_err(cross_pop, 'cross')

        mut_pop = NSGA.mutation(parent)

        find_err(mut_pop, 'mutate')

        new1 = np.vstack((cross_pop, pop))
        new_pop = np.vstack((mut_pop, new1))

        # new_pop = NSGA.cross_mutate(parent)

        find_err(new_pop, 'stack')

        # values = np.empty((pop_num, dim))
        values = choose_fun(func, var_in=new_pop)
        Usort, dis, rank = NSGA.dis_sort(values, dim)
        pop = NSGA.elitism(new_pop, Usort, dis)
        find_err(pop, 'elitism')
        # if i % 10 == 0:
        #     print('debug')
        print('--------------------------------gen:%d-----------------------------' % i)

        visualize(func, pop, dim)
    plt.ioff()
    plt.show()


def find_err(pop, explain):

    jug = np.zeros(pop.shape)
    jug[pop > 1] = 1
    jug[pop < 0] = 1
    a1 = np.sum(jug, 1)
    a2 = np.sum(jug)
    if a2 > 0:
        time.sleep(0.1)
        print('*****************%s errors*************************' % explain)


def init_population(pop_num, func):

    x_range, m = choose_fun(func, opt='init')

    population = np.empty([pop_num, m])
    if len(x_range) == 2:
        population = np.random.uniform(x_range[0], x_range[1], [pop_num, m])
    elif len(x_range) == 4:
        population[:, 0] = np.random.uniform(
            x_range[0], x_range[1], [pop_num, 1])
        population[:, 1:] = np.random.uniform(
            x_range[2], x_range[3], [pop_num, m - 1])
    else:
        print('wrong x range!')

    if func[:3] == 'ZDT':
        dim = 2
    else:
        dim = 3

    return population, x_range, dim


def visualize(func, pop, dim):

    values = choose_fun(func, var_in=pop)
    fx, best = choose_fun(func, opt='best')
    # print(len(pop))

    if dim == 2:
        # plt.close()
        plt.cla()
        plt.scatter(values[:, 0], values[:, 1], color='g', marker='o')
        plt.pause(0.5)

        # plt.scatter(fx, best, color='r', marker='.')
        # plt.show()


if __name__ == "__main__":

    generation = 100
    pop_num = 100

    prob_c = 0.9
    prob_m = 0.4
    prob = [prob_c, prob_m]

    yita_c = 20
    yita_m = 20
    yita = [yita_c, yita_m]

    func = ['ZDT_1', 'ZDT_2', 'ZDT_3', 'ZDT_4',
            'ZDT_5', 'ZDT_6', 'DTLZ_1', 'DTLZ_1', 'DTLZ_1']
    population, x_range, dim = init_population(pop_num, func[0])
    run(population, generation, x_range, dim, prob, yita, func[0])
