from miscread import miscread
import numpy as np


def ready(Yfile, maskstruct=None):
    """
    Preparation
    """
    Y = miscread(Yfile)
    if maskstruct is None:
        mask = ~(np.isnan(Y) + np.isinf(Y))
    return Y[mask]
