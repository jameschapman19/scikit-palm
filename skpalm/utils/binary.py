import numpy as np


def incrbin(B):
    """
    Increment binary number by 1

    Parameters
    ----------
    B : Logical vector

    Returns
    -------

    """
    B = B.copy()
    for b in B:
        k = np.where(np.logical_not(np.flip(b)))[0][0]
        b[-(k + 1) :] = np.logical_not(b[-(k + 1) :])
    return B


def d2b(d, n):
    b = np.array([list(np.binary_repr(d_, n)) for d_ in d]).astype(int)
    return b
