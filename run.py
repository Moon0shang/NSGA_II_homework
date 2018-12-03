import numpy as np

from test_func import choose_fun
from NSGA_II import NSGA_II


def run(pop, gen, x_range, dim, pop_num, prob, yita, func):

    NSGA = NSGA_II(gen, pop_num, prob, yita, x_range)
    values = np.empty((pop_num, dim))
    values = choose_fun(func, var_in=pop)
    Usort = NSGA.fast_Usort(values, dim)
    rank_num = len(Usort)
    distance = []
    Usort_idx = []
    for rn in range(rank_num):
        dis, idx = NSGA.cal_Cdis(Usort[rn], values[:, Usort[rn]], dim)
        distance.append(dis)
        Usort_idx.append(idx)

    for i in range(gen):
        selected = NSGA.select()
        cross_pop = NSGA.cross()
        mut_pop = NSGA.mutation()
        # merge all
        new_pop = np.vstack(pop, cross_pop)
        new_pop = np.vstack(new_pop, mut_pop)

        Usort = NSGA.fast_Usort()
        dis = NSGA.cal_Cdis()
        pop = NSGA.elitism()


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
    
    if func[:3] == 'DZT':
        dim = 2
    else:
        dim = 3

    return population,x_range,dim


def visualize():
    pass


if __name__ == "__main__":

    generation = 300
    pop_num = 20

    prob_c = 0.9
    prob_m = 0.1
    prob = [prob_c, prob_m]

    yita_c = 0.1
    yita_m = 0.1
    yita = [yita_c, yita_m]

    func= 'DZT_1'
    population ,x_range,m= init_population(pop_num, func)
    run(population,generation,x_range,dim, pop_num, prob, yita,func)
