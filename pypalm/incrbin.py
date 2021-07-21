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
    k = np.nonzero(~B)[0]
    B[:k] = ~B[:k]
    return B
