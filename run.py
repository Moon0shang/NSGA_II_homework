import numpy as np
import matplotlib.pyplot as plt

from test_func import choose_fun
from NSGA_II import NSGA_II


def run(pop, gen, x_range, dim, prob, yita, func):

    pop_num = pop.shape[0]
    NSGA = NSGA_II(gen, pop_num, prob, yita, x_range)
    # values = np.empty((pop_num, dim))
    values = choose_fun(func, var_in=pop)

    Usort, dis = NSGA.dis_sort(values, dim)
    for i in range(gen):
        # selected = NSGA.select()
        cross_pop = NSGA.cross(pop)
        new_pop = np.vstack((pop, cross_pop))
        mut_pop = NSGA.mutation(pop)
        new_pop = np.vstack((new_pop, mut_pop))

        # values = np.empty((pop_num, dim))
        values = choose_fun(func, var_in=new_pop)
        Usort, dis = NSGA.dis_sort(values, dim)
        pop = NSGA.elitism(new_pop, Usort, dis)

        # if i % 20 == 0:
        print('----------------------------------------')
        print('gen:%d' % i)

    visualize(func, pop, dim)


def init_population(pop_num, func):

    x_range, m = choose_fun(func, infos=True)
    population = np.empty([pop_num, m])

    for i in range(pop_num):
        x_init = np.empty([m])
        if len(x_range) != 2:
            # if func == 'DZT_5':
            #     x_init[0] = np.random.randint(x_range[0], x_range[1], 1)
            #     x_init[1:] = np.random.randint(
            #         x_range[3], x_range[4], m - 1)
            # else:
            x_init[0] = np.random.uniform(x_range[0], x_range[1], 1)
            x_init[1:] = np.random.uniform(x_range[0], x_range[1], m - 1)
        else:
            x_init = np.random.uniform(x_range[0], x_range[1], m)

        population[i, :] = x_init

    if func[:3] == 'ZDT':
        dim = 2
    else:
        dim = 3

    return population, x_range, dim


def visualize(func, pop, dim):

    values = choose_fun(func, var_in=pop)

    if dim == 2:
        plt.scatter(values[:, 0], values[:, 1])
        plt.show()


if __name__ == "__main__":

    generation = 300
    pop_num = 100

    prob_c = 0.9
    prob_m = 0.1
    prob = [prob_c, prob_m]

    yita_c = 20
    yita_m = 10
    yita = [yita_c, yita_m]

    func = ['ZDT_1', 'ZDT_2', 'ZDT_3', 'ZDT_4',
            'ZDT_5', 'ZDT_6', 'DTLZ_1', 'DTLZ_1', 'DTLZ_1']
    population, x_range, dim = init_population(pop_num, func[0])
    run(population, generation, x_range, dim, prob, yita, func[0])
