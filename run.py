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

        find_err(cross_pop, 'cross')

        mut_pop = NSGA.mutation(pop)

        find_err(mut_pop, 'mutate')

        new_pop = NSGA.cross_mutate(pop)

        find_err(new_pop, 'stack')

        # values = np.empty((pop_num, dim))
        values = choose_fun(func, var_in=new_pop)
        Usort, dis = NSGA.dis_sort(values, dim)
        pop = NSGA.elitism(new_pop, Usort, dis)
        find_err(pop, 'elitism')
        # if i % 10 == 0:
        #     print('debug')
        print('--------------------------------gen:%d-----------------------------' % i)

    visualize(func, pop, dim)


def find_err(pop, explain):

    jug = np.zeros(pop.shape)
    jug[pop > 1] = 1
    jug[pop < 0] = 1
    a1 = np.sum(jug, 1)
    a2 = np.sum(jug)
    if a2 > 0:
        print('*****************%s errors*************************' % explain)


def init_population(pop_num, func):

    x_range, m = choose_fun(func, infos=True)

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

    if dim == 2:
        plt.scatter(values[:, 0], values[:, 1], color='b', marker='*')
        fx = np.arange(0, 1, 0.005)
        v_true = np.multiply(1, 1 - np.sqrt(fx / 1))
        plt.scatter(fx, v_true, color='r', marker='.')
        plt.show()


if __name__ == "__main__":

    generation = 300
    pop_num = 100

    prob_c = 0.9
    prob_m = 0.1
    prob = [prob_c, prob_m]

    yita_c = 20
    yita_m = 20
    yita = [yita_c, yita_m]

    func = ['ZDT_1', 'ZDT_2', 'ZDT_3', 'ZDT_4',
            'ZDT_5', 'ZDT_6', 'DTLZ_1', 'DTLZ_1', 'DTLZ_1']
    population, x_range, dim = init_population(pop_num, func[0])
    run(population, generation, x_range, dim, prob, yita, func[0])
