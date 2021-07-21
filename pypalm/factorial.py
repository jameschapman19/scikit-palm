import numpy as np


def factorial(n):
    lf = np.zeros((n + 1, 1))
    for n_ in range(1, n + 1):
        lf[n_] = np.log(n_) + lf[n_ - 1]
    return lf
