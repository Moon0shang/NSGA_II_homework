import numpy as np
import time


class NSGA_II(object):

    def __init__(self,  pop_num, prob, yita, x_range):

        # the ditribution is narrow when yita_c is largeer
        self.yita_c = yita[0]
        # the parent and offspring are more different when yita_m is smaller
        self.yita_m = yita[1]
        # cross and mutate probabilities
        self.prob_c = prob[0]
        self.prob_m = prob[1]
        self.x_range = x_range
        self.pop_num = pop_num

    def select(self, pop,  dis, rank, Usort):
        'choose the one to cross'
        pnum = len(pop)
        pool_size = pnum//2
        if pool_size % 2 != 0:
            pool_size += 1

        parent = np.empty([pool_size, pop.shape[1]])
        for i in range(pool_size):
            candidate = np.zeros([2], dtype=np.int32)
            for j in range(2):
                candidate[j] = np.round(
                    np.random.random() * pnum).astype(np.int32)
                if candidate[j] < 1:
                    candidate[j] = 1

            while candidate[0] == candidate[1]:
                candidate[1] = np.round(
                    np.random.random() * pnum).astype(np.int32)
                if candidate[1] < 1:
                    candidate[1] = 1

            if rank[candidate[0]] == rank[candidate[1]]:
                pos1 = self.find_pos(Usort, candidate[0])
                pos2 = self.find_pos(Usort, candidate[1])
                if dis[pos1[0]][pos1[1]] >= dis[pos2[0]][pos2[1]]:
                    parent[i, :] = pop[candidate[0], :]
                else:
                    parent[i, :] = pop[candidate[1], :]
            elif rank[candidate[0]] > rank[candidate[1]]:
                parent[i, :] = pop[candidate[0], :]
            else:
                parent[i, :] = pop[candidate[1], :]

        return parent

    def find_pos(self, Usort, can):
        for i, r in enumerate(Usort):
            for j, rr in enumerate(r):
                if rr == can:
                    return i, j
    # def cross_mutate(self, parent):
    #     cr_pop = self.cross(parent)
    #     new_pop = np.vstack((cr_pop, parent))
    #     mut_pop = self.mutation(parent)
    #     new_pop = np.vstack((new_pop, mut_pop))

    #     return new_pop

    def cross(self, pop):

        # p = np.random.rand(pop.shape[0])
        # mating = pop[p < self.prob_c]
        # # shuffle the mating parent
        # np.random.shuffle(mating)
        # # force mat_l to be even to gen couples
        # mat_l = len(mating)
        # if mat_l == 0:
        #     return None
        # elif mat_l % 2 != 0:
        #     mating = mating[:-1]
        #     mat_l -= 1

        # cross_pop = np.empty([mat_l, pop.shape[1]])

        cross_pop = np.empty(pop.shape)
        valid = 0
        for i in range(pop.shape[0] // 2):

            if np.random.random() < self.prob_c:
                p1 = np.round(len(pop) * np.random.random()).astype(np.int32)
                p2 = np.round(len(pop) * np.random.random()).astype(np.int32)
                while p1 == p2:
                    p2 == np.round(len(pop) * np.random.random()
                                   ).astype(np.int32)

                parent1 = pop[p1]
                parent2 = pop[p2]

                offspring1, offspring2 = self.__single_cross(
                    parent1, parent2, self.x_range)

                cross_pop[2 * valid, :] = offspring1
                cross_pop[2 * valid + 1, :] = offspring2
                valid += 1

        return cross_pop[2*valid, :]

    def __single_cross(self, parent1, parent2, x_range):

        x_low = x_range[0]
        x_up = x_range[1]

        offspring1 = np.empty(parent1.shape)
        offspring2 = np.empty(parent2.shape)
        for i in range(len(parent1)):

            p = np.random.rand()
            if p <= 0.5:
                beta = np.power(2 * (p), (1 / (self.yita_c + 1)))
            else:
                beta = np.power(1/(2*(1-p)), (1 / (self.yita_c + 1)))

            offspring1[i] = 0.5 * \
                ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
            offspring2[i] = 0.5 * \
                ((1 - beta) * parent1[i] + (1 + beta) * parent2[i])
            if offspring1[i] < x_low:
                offspring1[i] = x_low
            if offspring1[i] > x_up:
                offspring1[i] = x_up
            if offspring2[i] < x_low:
                offspring2[i] = x_low
            if offspring2[i] > x_up:
                offspring2[i] = x_up
            # if parent1[i] == parent2[i]:
            #     offspring1[i] = parent1[i]
            #     offspring2[i] = parent1[i]
            #     # print(offspring2[i], i)
            # else:
            #     if parent1[i] > parent2[i]:
            #         parent1[i], parent2[i] = parent2[i], parent1[i]

            #     if len(self.x_range) == 2:
            #         x_low = self.x_range[0]
            #         x_up = self.x_range[1]
            #     else:
            #         if i > 0:
            #             x_low = self.x_range[3]
            #             x_up = self.x_range[4]

            #     alpha1 = 2 - np.power(1 + ((2 * (parent1[i] - x_low)) / (parent2[i] - parent1[i])),
            #                           -(self.yita_c + 1))

            #     alpha2 = 2 - np.power(1 + ((2 * (x_up - parent2[i])) / (parent2[i] - parent1[i])),
            #                           -(self.yita_c + 1))

            #     beta1 = self.__get_beta(alpha1)
            #     beta2 = self.__get_beta(alpha2)

            #     offspring1[i] = 0.5 * (parent1[i] + parent2[i] -
            #                            beta1 * (parent2[i] - parent1[i]))
            #     offspring2[i] = 0.5 * (parent1[i] + parent2[i] +
            #                            beta2 * (parent2[i] - parent1[i]))

        return offspring1, offspring2

    def __get_beta(self, alpha):

        p = np.random.rand()

        if p <= 1/alpha:
            beta = np.power(p * alpha, 1 / (self.yita_c + 1))
        else:
            beta = np.power(1 / (2 - p * alpha), 1 / (self.yita_c + 1))
            # print(alpha, beta)
            # time.sleep(0.02)

        return beta

    def mutation(self, pop):
        'TODO:add select the parent'
        # p = np.random.rand(pop.shape[0])
        # mutate = pop[p < self.prob_m]
        l = len(pop)
        mut_pop = np.empty(pop.shape)
        valid = 0
        for i in range(l):

            if np.random.random() < self.prob_m:
                p = np.round(np.random.random * l).astype(np.int32)
                parent = pop[l]
                offspring = self.__single_mu(parent)
                mut_pop[i, :] = offspring
                valid += 1

        return mut_pop[valid, :]

    def __single_mu(self, parent):
        'need modify'
        offspring = np.empty(parent.shape)
        for i in range(len(parent)):

            if len(self.x_range) == 2:
                x_low = self.x_range[0]
                x_up = self.x_range[1]
            else:
                if i > 0:
                    x_low = self.x_range[3]
                    x_up = self.x_range[4]

            p = np.random.rand()

            if p <= 0.5:
                delta = np.power(2 * p, 1 / (self.yita_m + 1)) - 1
            else:
                delta = 1 - np.power(2 * (1 - p), 1 / (self.yita_m + 1))

            offspring[i] = parent[i] + delta

            if offspring[i] < x_low:
                offspring[i] = x_low
            elif offspring[i] > x_up:
                offspring[i] = x_up

            # if p <= 0.5:
            #     epsq = np.power(2 * p + (1 - 2 * p) * (1 - (parent[i] - x_low) / (x_up - x_low)),
            #                     1 / (self.yita_m + 1)) - 1
            # else:
            #     epsq = 1 - np.power(2 * (1 - p) + 2 * (p - 0.5) * (1 - (x_up - parent[i]) / (x_up - x_low)),
            #                         1 / (self.yita_m + 1))

            # offspring[i] = parent[i] + epsq * (x_up - x_low)

        return offspring

    def dis_sort(self, values, dim):

        Usort, rank = self.__fast_Usort(values, dim)
        rank_num = len(Usort)
        distance = []
        # Usort_idx = []
        for rn in range(rank_num):
            Usort_num = len(Usort[rn])
            dis = self.__cal_Cdis(Usort_num, values[Usort[rn], :], dim)
            distance.append(dis)

        return Usort, distance, rank

    def __fast_Usort(self, values, dim):

        num = values.shape[0]
        n_p = np.zeros([num])   # dominate p
        s_p = [[] for i in range(num)]  # be dominated by p
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
                        s_p[p].append(q)  # 被个体p支配的个体，比p的值要大（求最小值）
                    elif T[0] + T[2] == dim:
                        n_p[p] += 1  # 支配p的个体，比p值小（求最小值）

            if n_p[p] == 0:
                rank[p] = 1
                F1.append(p)

        Usort.append(F1)

        i = 0
        while Usort[i] != []:
            Q = []
            for p in Usort[i]:
                for q in s_p[p]:
                    # if q not in Q:
                    n_p[q] -= 1
                    if n_p[q] == 0:
                        # 该个体Pareto级别为当前最高级别加1。此时i初始值为0，所以要加2
                        rank[q] = i + 2
                        Q.append(q)

            Usort.append(Q)
            i += 1

        return Usort[:-1], rank

    def __cal_Cdis(self, num, values, dim):
        'need test'
        # num = len(Usort)
        dis = np.zeros([num])
        sort_idx = np.zeros([num, dim], dtype=np.int)
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
        next_pop = np.ones([self.pop_num, new_pop.shape[1]])

        for i in range(len(Usort)):

            level_num = len(Usort[i])
            if self.pop_num <= (level_num + num):
                diff = self.pop_num - num
                idx = np.argsort(dis[i])
                stay = idx[-diff:]
                stay_idx = []
                for s in stay:
                    stay_idx.append(Usort[i][s])
                try:
                    next_pop[num:self.pop_num, :] = new_pop[stay_idx, :]
                except:
                    print('num:%d,stay:%d' % (num, len(stay)))
                    next_pop[num:self.pop_num, :] = new_pop[stay_idx, :]
                break
            else:
                stay_idx = Usort[i]
                next_pop[num:(num + level_num)] = new_pop[stay_idx, :]
            num += level_num

        return next_pop
