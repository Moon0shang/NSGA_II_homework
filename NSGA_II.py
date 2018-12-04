import numpy as np


class NSGA_II(object):

    def __init__(self, gen, pop_num, prob, yita, x_range):

        # the ditribution is narrow when yita_c is largeer
        self.yita_c = yita[0]
        # the parent and offspring are more different when yita_m is smaller
        self.yita_m = yita[1]
        # cross and mutate probabilities
        self.prob_c = prob[0]
        self.prob_m = prob[1]
        self.x_range = x_range
        self.pop_num = pop_num

    # def select(self,):
    #     'choose the one to cross'
    #     parent = None
    #     return parent

    def cross(self, pop):

        p = np.random.rand(pop.shape[0])
        mating = pop[p < self.prob_c]
        # shuffle the mating parent
        np.random.shuffle(mating)
        # force mat_l to be even to gen couples
        mat_l = len(mating)
        if mat_l == 0:
            return None
        elif mat_l % 2 != 0:
            mating = mating[:-1]
            mat_l -= 1

        cross_pop = np.empty(mat_l, pop.shape[1])
        for i in range(mat_l // 2):

            parent1 = mating[2 * i]
            parent2 = mating[2 * i + 1]

            if len(pop) == 2:
                offspring1, offspring2 = self.__single_cross(
                    parent1, parent2, self.x_range)
            else:
                offspring1 = np.empty(parent1.shape)
                offspring2 = np.empty(parent1.shape)
                offspring1[0] = self.__single_cross(
                    parent1[0], parent2[0], self.x_range[:2])
                offspring1[1:] = self.__single_cross(
                    parent1[1:], parent2[1:], self.x_range[2:])

            cross_pop[2 * i, :] = offspring1
            cross_pop[2 * i + 1, :] = offspring2

        return cross_pop

    def __single_cross(self, parent1, parent2, x_range):

        x_low = x_range[0]
        x_up = x_range[1]

        alpha1 = 2 - np.power(1 + ((2 * (parent1 - x_low)) / (parent2 - parent1)),
                              -(self.yita_c + 1))

        alpha2 = 2 - np.power(1 + ((2 * (x_up - parent2)) / (parent2 - parent1)),
                              -(self.yita_c + 1))

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
        p = np.random.rand(pop.shape[0])
        mutate = pop[p < self.prob_m]

        mut_pop = np.empty(mutate.shape)
        for i, parent in enumerate(mutate):

            if len(self.x_range) == 2:
                offspring = self.__single_mu(parent, self.x_range)
            else:
                offspring = np.empty(parent.shape)
                offspring[0] = self.__single_mu(parent[0], self.x_range[:2])
                offspring[1:] = self.__single_mu(parent[1:], self.x_range[2:])

            mut_pop[i, :] = offspring

        return mut_pop

    def __single_mu(self, parent, x_range):

        x_low = x_range[0]
        x_up = x_range[1]

        p = np.random.rand()
        if p <= 0.5:
            epsq = np.power(2 * p + (1 - 2 * p) * (1 - (parent - x_low) / (x_up - x_low)),
                            1 / (self.yita_m + 1))
        else:
            epsq = 1 - np.power(2 * (1 - p) + 2 * (p - 0.5) * (1 - (x_up - parent) / (x_up - x_low)),
                                1 / (self.yita_m + 1))

        offspring = parent + epsq * (x_up - x_low)

        return offspring

    def dis_sort(self, values, dim):

        Usort = self.__fast_Usort(values, dim)
        rank_num = len(Usort)
        distance = []
        # Usort_idx = []
        for rn in range(rank_num):
            Usort_num = len(Usort[rn])
            dis = self.__cal_Cdis(Usort_num, values[Usort[rn], :], dim)
            distance.append(dis)

        return Usort, distance

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
                    if values[p, d] == values[q, d]:
                        T[0] += 1
                    elif values[p, d] < values[q, d]:
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
        sort_idx = np.zeros([num, dim], dtype=np.int32)
        dis_dim = np.empty([num, dim])

        for d in range(dim):
            sort_idx[:, d] = np.argsort(values[:, d])
            dis_dim[sort_idx[0][d]][d] = np.inf
            dis_dim[sort_idx[-1][d]][d] = np.inf

            for i in range(1, num - 1):
                dis_dim[sort_idx[i][d]][d] = (values[sort_idx[i - 1][d], d] - values[sort_idx[i + 1][d], d]) / (
                    np.max(values[:, d]) - np.min(values[:, d]))

        for i in range(num):
            for d in range(dim):
                dis[i] += dis_dim[i][d]

        return dis

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
