import numpy as np

prob_c = None   # the ditribution is narrow when prob_c is largeer
prob_m = None   # the parent and offspring are more different when prob_m is smaller
x_low = None
x_up = None

np.can


def cross(parent1, parent2):

    alpha1 = 2-np.power(1+((2*(parent1-x_low))/(parent2-parent1), -(prob_c+1)))
    alpha2 = 2-np.power(1+((2*(x_up-parent2))/(parent2-parent1), -(prob_c+1)))

    p = np.random.rand()

    beta1 = get_beta(alpha1, p)
    beta2 = get_beta(alpha2, p)

    offspring1 = 0.5 * (parent1 + parent2 - beta1 * (parent2 - parent1))
    offspring2 = 0.5 * (parent1 + parent2 + beta1 * (parent2 - parent1))


def get_beta(alpha, p):

    if p < 1 / alpha:
        beta = np.power(p * alpha, 1 / (prob_c + 1))
    else:
        beta = np.power(1 / (2 - p * alpha), 1 / (prob_c + 1))


def mutation(parent):

    p = np.random.rand()

    if p <= 0.5:
        epsq = np.power(2 * p + (1 - 2 * p) * (1 - (parent -
                                                    x_low) / (x_up - x_low)), 1 / (prob_m + 1))
    else:
        epsq = 1 - np.power(2 * (1 - p) + 2 * (p - 0.5) *
                            (1 - (x_up - parent) / (x_up - x_low)), 1 / (prob_m + 1))
    offspring = parent + epsq * (x_up - x_low)


def fast_Usort():
    pass


def cal_Cdis():
    pass


def select():
    pass


def merge_all():
    pass
