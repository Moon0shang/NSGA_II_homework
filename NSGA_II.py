import numpy as np


class NSGA_II(object):

    def __init__(self, gen, pop_num, prob, yita, x_range):

        # the ditribution is narrow when yita_c is largeer
        self.yita_c = yita[0]
        # the parent and offspring are more different when yita_m is smaller
        self.yita_m = yita[1]
        self.x_low = x_range[0]
        self.x_up = x_range[1]
        self.pop_num = pop_num

    def select(self,):
        'choose the one to cross'
        parent = None
        return parent

    def cross(self, pop):
        'TODO:add select the parent'
        parent1 = None
        parent2 = None
        "deal with double x range"
        alpha1 = 2 - np.power(1 + ((2 * (parent1 - self.x_low)) /
                                   (parent2 - parent1)), -(self.yita_c + 1))

        alpha2 = 2 - np.power(1 + ((2 * (self.x_up - parent2)) /
                                   (parent2 - parent1)), -(self.yita_c + 1))

        p = np.random.rand()

        beta1 = self.__get_beta(alpha1, p)
        beta2 = self.__get_beta(alpha2, p)

        offspring1 = 0.5 * (parent1 + parent2 - beta1 * (parent2 - parent1))
        offspring2 = 0.5 * (parent1 + parent2 + beta1 * (parent2 - parent1))

        return offspring1, offspring2

    def __get_beta(self, alpha, p):

        if p < 1 / alpha:
            beta = np.power(p * alpha, 1 / (self.yita_c + 1))
        else:
            beta = np.power(1 / (2 - p * alpha), 1 / (self.yita_c + 1))

        return beta

    def mutation(self, pop):
        'TODO:add select the parent'
        parent = None
        p = np.random.rand()
        "deal with double x range"
        if p <= 0.5:
            epsq = np.power(2 * p + (1 - 2 * p) * (1 - (parent -
                                                        self.x_low) / (self.x_up - self.x_low)), 1 / (self.yita_m + 1))
        else:
            epsq = 1 - np.power(2 * (1 - p) + 2 * (p - 0.5) *
                                (1 - (self.x_up - parent) / (self.x_up - self.x_low)), 1 / (self.yita_m + 1))
        offspring = parent + epsq * (self.x_up - self.x_low)

        return offspring

    def __fast_Usort(self, values, dim):

        num = values.shape[0]
        pn = np.zeros([num])
        sp = [[] for i in range(num)]
        rank = np.zeros([num], dtype=np.int32)
        F1 = []
        Usort = []

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
                        pn[p] += 1  # 支配p的个体，比p值小（求最小值）

            if pn[p] == 0:
                rank[p] = 1

            F1.append(p)

        Usort.append(F1)

        i = 0
        while Usort[i] != []:
            Q = []
            for p in Usort[i]:
                for q in sp[p]:
                    if q not in Q:
                        pn[q] -= 1
                        if pn[q] == 0:
                            # 该个体Pareto级别为当前最高级别加1。此时i初始值为0，所以要加2
                            rank[q] = i + 2
                            Q.append(q)
            Usort.append(Q)
            i += 1

        return Usort

    def __cal_Cdis(self, num, values, dim):
        'need test'
        # num = len(Usort)
        dis = np.zeros([num])
        sort_idx = np.zeros([dim, num], dtype=np.int32)
        dis_dim = np.empty([dim, num])

        for d in range(dim):
            sort_idx[d] = np.argsort(values[:, d])
            dis_dim[d][sort_idx[d][0]] = np.inf
            dis_dim[d][sort_idx[d][-1]] = np.inf

            for i in range(1, num - 1):
                dis_dim[d][sort_idx[d][i]] = (values[sort_idx[d][i - 1], d] - values[sort_idx[d][i + 1], d]) / (
                    np.max(values[:, d]) - np.min(values[:, d]))

        for i in range(num):
            for d in range(dim):
                dis[i] += dis_dim[d][i]

        return dis

    def dis_sort(self, values, dim):

        Usort = self.__fast_Usort(values, dim)
        rank_num = len(Usort)
        distance = []
        Usort_idx = []
        for rn in range(rank_num):
            Usort_num = len(Usort[rn])
            dis = self.__cal_Cdis(Usort_num, values[:, Usort[rn]], dim)
            distance.append(dis)

        return Usort, distance

    def elitism(self, new_pop, Usort, dis):

        num = 0
        next_pop = np.empty(self.pop_num, new_pop.shape[1])

        for i in range(len(Usort)):
            num += len(Usort[i])

            if num > self.pop_num:
                idx = np.argsort(dis[i])
                diff = num - self.pop_num
                stay = idx[:diff]
                Usort = Usort[stay]
                num = self.pop_num

            next_pop[(num - len(Usort)):num, :] = new_pop[Usort, :]

        return next_pop
