import numpy as np


def swapfmt(permutation_set):
    if isinstance(permutation_set, list):
        Pnew = np.zeros(permutation_set[0].shape[0], len(permutation_set))
        I = np.arange(permutation_set[0].shape[0]).T
        for p in range(len(permutation_set)):
            Pnew[:, p] = permutation_set[p] * I
        if np.unique(np.abs(Pnew).T, axis=0).shape[0] == 1:
            Pnew = np.sign(Pnew)
    elif isinstance(permutation_set, np.ndarray):
        P = np.eye(permutation_set.shape[0])
        Pnew = [] * permutation_set.shape[1]
        for p in range(permutation_set.shape[1]):
            sgn = np.sign(permutation_set[:, p])
            idx = np.abs(permutation_set[:, p]).astype(int)
            # if just sign flips
            if np.all(np.ones_like(idx) == idx):
                Pnew[p] = np.diag(sgn)
            else:
                Pnew[p] = np.diag(sgn) @ P[idx - 1, :]
    return Pnew
