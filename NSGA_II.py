import numpy as np


class NSGA_II(object):

    def __init__(self, gen, pop_num, prob, yita, func):

        self.yita_c = yita_c   # the ditribution is narrow when yita_c is largeer
        self.yita_m = yita_m   # the parent and offspring are more different when yita_m is smaller
        self.x_low = func[0]
        self.x_up = func[1]

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

    def fast_Usort(self,):
        pass

    def cal_Cdis(self, value1, value2, front):

        front_num = len(front)
        dis = np.zeros([front_num])
        dis[0], dis[-1] = np.inf, np.inf
        ordered1 = np.argsort(value1)[:front_num]
        ordered2 = np.argsort(value2)[:front_num]

    def select(self,):
        pass

    def merge_all(self,):
        pass

    def elitism(self,):
        pass
