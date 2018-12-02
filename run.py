import numpy as np

from test_func import choose_fun
from NSGA_II import NSGA_II


def run(pop, gen, pop_num, prob, yita):

    NSGA = NSGA_II(gen, pop_num, prob, yita, func)
    NSGA.fast_Usort()
    NSGA.cal_Cdis()

    for i in range(gen):
        NSGA.select()
        cross_pop = NSGA.cross()
        mut_pop = NSGA.mutation()
        new_pop = NSGA.merge_all(population, cross_pop, mut_pop)
        NSGA.fast_Usort()
        NSGA.cal_Cdis()
        NSGA.elitism()


def init_population(pop_num, func):

    x_range, m = choose_fun(func=func, init=True)
    population = np.empty(pop_num, m)

    for i in range(pop_num)
      x_init = np.empty(m)
       if len(x_range) != 2:
           if func == 'DZT_5':
                x_init[0] = np.random.randint(x_range[0], x_range[1], 1)
                x_init[1:] = np.random.randint(x_range[3], x_range[4], m - 1)
            else:
                x_init[0] = np.random.uniform(x_range[0], x_range[1], 1)
                x_init[1:] = np.random.uniform(x_range[0], x_range[1], m - 1)
        else:
            x_init = np.random.uniform(x_range[0], x_range[1], m)

        population[i, :] = x_init

    return population


def visualize():
    pass


if __name__ == "__main__":

    generation = 300
    pop_num = 100

    prob_c = 0.9
    prob_m = 0.1
    prob = [prob_c, prob_m]

    yita_c = 0.1
    yita_m = 0.1
    yita = [yita_c, yita_m]

    population = init_population(pop_num, 'DZT_1')
    run(population,generation, pop_num, prob, yita)
