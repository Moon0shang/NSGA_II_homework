import time
import numpy as np

from func import functions


class NSGA_Core(object):

    def __init__(self, pop_num, prob, yita, func):

        self.pop_num = pop_num
        self.func = func
        # yita
        self.yita_c = yita[0]
        self.yita_m = yita[1]
        # probilities
        self.prob_c = prob[0]
        self.prob_m = prob[1]
        # initialize parameters
        x_range, m, dim = functions(func, opt='init')
        self.x_num = m
        self.x_range = x_range
        self.dim = dim

    def get_best(self):

        fx, best = functions(self.func, opt='best')

        return fx, best

    def initialize(self,):

        pop_num = self.pop_num
        x_range = self.x_range
        m = self.x_num

        population = np.empty([pop_num, m+self.dim])
        if len(x_range) == 2:
            population[:, :m] = np.random.uniform(
                x_range[0], x_range[1], [pop_num, m])
        elif len(x_range) == 4:
            population[:, 0] = np.random.uniform(
                x_range[0], x_range[1], [pop_num, 1])
            population[:, 1:m] = np.random.uniform(
                x_range[2], x_range[3], [pop_num, m - 1])
        else:
            print('wrong x range!')

        population[:, m:] = functions(self.func, var_in=population[:, :m])

        return population

    def sort_dis(self, pop):

        Usort, sort_pop = self.__fast_Usort(pop)
        dis_pop = self.__distance(Usort, sort_pop)

        return dis_pop

    def __fast_Usort(self, pop):

        num = pop.shape[0]
        values = pop[:, self.x_num:(self.x_num+self.dim)]
        n_p = np.zeros([num])   # dominate p
        s_p = [[] for i in range(num)]  # be dominated by p
        rank = np.zeros([num], dtype=np.int32)
        F1 = []
        Usort = []

        for p in range(num):
            for q in range(num):

                T = np.zeros([3])
                for d in range(self.dim):
                    if values[p, d] == values[q, d]:
                        T[0] += 1
                    elif values[p, d] < values[q, d]:
                        T[1] += 1   # 被个体p支配的个体，比p的值要大（求最小值）
                    else:
                        T[2] += 1   # 支配p的个体，比p值小（求最小值）

                if T[1] == 0 and T[0] != self.dim:
                    n_p[p] += 1
                elif T[2] == 0 and T[0] != self.dim:
                    s_p[p].append(q)
                # if T[0] != self.dim:
                #     if T[0] + T[1] == self.dim:
                #         s_p[p].append(q)  # 被个体p支配的个体，比p的值要大（求最小值）
                #     elif T[0] + T[2] == self.dim:
                #         n_p[p] += 1  # 支配p的个体，比p值小（求最小值）

            if n_p[p] == 0:
                rank[p] = 1
                F1.append(p)

        Usort.append(F1)

        # get the other levels
        i = 0
        while Usort[i] != []:
            Q = []
            for p in Usort[i]:
                if s_p[p] != []:
                    for q in s_p[p]:
                        # if q not in Q:
                        n_p[q] -= 1
                        if n_p[q] == 0:
                            # 该个体Pareto级别为当前最高级别加1。此时i初始值为0，所以要加2
                            rank[q] = i + 2
                            Q.append(q)

            Usort.append(Q)
            i += 1

        sort_idx = np.argsort(rank)
        rank_pop = np.hstack((pop, rank.reshape(-1, 1)))
        sort_pop = rank_pop[sort_idx, :]

        return Usort[:-1], sort_pop

    def __distance(self, Usort, pop):

        # cur_idx = 0
        # for i, level in enumerate(Usort):
        #     distance = 0
        #     y = np.empty([len(level), pop.shape[1]+1])
        #     pre_idx = cur_idx+1
        #     for j, idx in enumerate(level):
        #         y[:, j] = pop[cur_idx + j]
        #     for j in range(self.dim):
        #         sort_idx = np.argsort(y[:, self.x_num + j])
        #         sort_y = np.empty(y.shape)
        #         for k, sidx in enumerate(sort_idx):
        #             sort_y[j, :] = y[sidx, :]
        #         fmax = sort_y[-1, self.x_num + j]
        #         fmin = sort_y[0, self.x_num + j]
        #         y[-1, self.x_num + self.dim + 1 + i] = np.inf

        for i, level in Usort:
            
        dis_pop = None

        return dis_pop

    def tournament(self,):
        pass

    def cross_mutate(self,):
        pass

    def __cross(self,):
        pass

    def __mutate(self,):
        pass

    def elitism(self,):
        pass
