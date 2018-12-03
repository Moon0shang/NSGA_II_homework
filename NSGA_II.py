import numpy as np


class NSGA_II(object):

    def __init__(self, gen, pop_num, prob, yita, x_range):

        self.yita_c = yita_c   # the ditribution is narrow when yita_c is largeer
        self.yita_m = yita_m   # the parent and offspring are more different when yita_m is smaller
        self.x_low = x_range[0]
        self.x_up = x_range[1]

    def cross(self, parent1, parent2):

        alpha1 = 2-np.power(1+((2*(parent1-self.x_low)) /
                               (parent2-parent1), -(self.yita_c+1)))
        alpha2 = 2-np.power(1+((2*(self.x_up-parent2)) /
                               (parent2-parent1), -(self.yita_c+1)))

        p = np.random.rand()

        beta1 = __get_beta(alpha1, p)
        beta2 = __get_beta(alpha2, p)

        offspring1 = 0.5 * (parent1 + parent2 - beta1 * (parent2 - parent1))
        offspring2 = 0.5 * (parent1 + parent2 + beta1 * (parent2 - parent1))

    def __get_beta(self, alpha, p):

        if p < 1 / alpha:
            beta = np.power(p * alpha, 1 / (self.yita_c + 1))
        else:
            beta = np.power(1 / (2 - p * alpha), 1 / (self.yita_c + 1))

    def mutation(self, parent):

        p = np.random.rand()

        if p <= 0.5:
            epsq = np.power(2 * p + (1 - 2 * p) * (1 - (parent -
                                                        self.x_low) / (self.x_up - self.x_low)), 1 / (self.yita_m + 1))
        else:
            epsq = 1 - np.power(2 * (1 - p) + 2 * (p - 0.5) *
                                (1 - (self.x_up - parent) / (self.x_up - self.x_low)), 1 / (self.yita_m + 1))
        offspring = parent + epsq * (self.x_up - self.x_low)

    def fast_Usort(self, values, dim):

        num = values.shape[0]
        np = np.zeros([num])
        sp = [[] for i in range(num)]
        rank = np.zeros([num])
        Usort = []
        idx_sort = np.empty([dim, num])
        F1 = []
        for p in range(num):
            for q in range(num):

                T = np.zeros([3])
                for d in range(dim):
                    if values[d][p] == values[d][q]:
                        T[0] += 1
                    elif values[d][p] < values[d][q]:
                        T[1] += 1   # 被个体p支配的个体，比p的值要大（求最小值）
                    else:
                        T[2] += 1   # 支配p的个体，比p值小（求最小值）

                if T[0] != dim:
                    if T[0] + T[1] == dim:
                        sp[p].append(q)  # 被个体p支配的个体，比p的值要大（求最小值）
                    elif T[0] + T[2] == dim:
                        np[p] += 1  # 支配p的个体，比p值小（求最小值）

            if np[p] == 0:
                rank[p] = 1

            F1.append(p)

        Usort.append(F1)

        i = 0
        while Usort[i] != []:
            Q = []
            for p in Usort[i]:
                for q in sp[p]:
                    if q not in Q:
                        np[q] -= 1
                        if np[q] == 0:
                            # 该个体Pareto级别为当前最高级别加1。此时i初始值为0，所以要加2
                            rank[q] = i + 2
                            Q.append(q)
            Usort.append(Q)
            i += 1

        return Usort

    def cal_Cdis(self, Usort, values, dim):
        'wrong'
        num = len(Usort)
        dis = np.zeros([num])
        dis[0], dis[-1] = np.inf, np.inf
        'need test'
        # idx = np.zeros([dim, num], dtype=np.int32)
        # fmax = np.zeros([dim], dtype=np.int32)
        # fmin = np.zeros([dim], dtype=np.int32)
        # for d in range(dim):
        #     fmax[d] = np.max(values[:, d])
        #     fmin[d] = np.min(values[:, d])

        idx = np.argsort(values[:, 0])
        values_sort = values[idx, :]
        Usort_idx = Usort[idx]
        for i in range(1, num-1):  # min ,max
            diff = 0
            for d in range(dim):
                diff += (values_sort[i+1, d] - values_sort[i-1, d]) / \
                    (np.max(values[:, d])-np.min(values[:, d]))
            dis[i] = diff

        return dis, Usort_idx

    def cal_Cdis_3(self, Usort, values, dim):

        num = len(Usort)
        dis = np.zeros([num])
        # dis[0], dis[-1] = np.inf, np.inf
        'need test'
        idx = np.zeros([dim, num], dtype=np.int32)
        fmax = np.zeros([dim], dtype=np.int32)
        fmin = np.zeros([dim], dtype=np.int32)
        for i in range(dim):
            idx[i] = np.argsort(values[:, i])
            fmax[i] = idx[i, -1]
            fmin[i] = idx[i, 0]
        for i in range(num):  # min ,max
            diff = 0
            for d in range(dim):
                diff += None
            dis[None] = diff

        'edge tobe inf'

    def select(self,):
        pass

    def elitism(self,):
        pass
