import math

import numpy as np

from skpalm.utils.logfactorial import logfactorial

vector_factorial = np.vectorize(math.factorial)


def maxshuf(permutation_tree, stype: str = "permutations", log: bool = False):
    """

    Parameters
    ----------
    permutation_tree
    stype
    log

    Returns
    -------

    """
    if log:
        if stype == "permutations":
            maxb = lmaxpermnode(permutation_tree, 0)
        elif stype == "flips":
            maxb = lmaxflipnode(permutation_tree, 0)
            maxb = maxb / np.log2(np.exp(1))
        elif stype == "both":
            maxp = lmaxpermnode(permutation_tree, 0)
            maxs = lmaxflipnode(permutation_tree, 0)
            maxb = maxp + maxs
    else:
        if stype == "permutations":
            maxb = maxpermnode(permutation_tree, 1)
        elif stype == "flips":
            maxb = maxflipnode(permutation_tree, 1)
        elif stype == "both":
            maxp = maxpermnode(permutation_tree, 1)
            maxs = maxflipnode(permutation_tree, 1)
            maxb = maxp * maxs
    return maxb


def maxpermnode(permutation_tree, nperms):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][0] is not None and not np.any(
            np.isnan(permutation_tree[u][0])
        ):
            nperms = nperms * seq2nperms(permutation_tree[u][0][0])
        else:
            nperms = nperms * 1
        if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
            nperms = maxpermnode(permutation_tree[u][2], nperms)
    return nperms


def maxflipnode(permutation_tree, nflips):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
            nflips = maxflipnode(permutation_tree[u][2], nflips)
        if permutation_tree[u][0] is not None and not np.any(
            np.isnan(permutation_tree[u][0])
        ):
            nflips = nflips * 2 ** len(permutation_tree[u][1])
        else:
            nflips = nflips
    return nflips


def lmaxpermnode(permutation_tree, nperms):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][0] is not None and not np.any(
            np.isnan(permutation_tree[u][0])
        ):
            nperms = nperms + lseq2nperms(permutation_tree[u][0][0])
        else:
            nperms = nperms
        if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
            nperms = lmaxpermnode(permutation_tree[u][2], nperms)
    return nperms


def lmaxflipnode(permutation_tree, nflips):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
            nflips = lmaxflipnode(permutation_tree[u][2], nflips)
        if permutation_tree[u][1] is None:
            nflips = nflips
        else:
            nflips = nflips + len(permutation_tree[u][1])
    return nflips


def seq2nperms(S):
    if isinstance(S, (float, int, np.integer)):
        S = [int(S)]
    U = np.unique(S)
    nU = len(U)
    cnt = np.zeros_like(U)
    for u in range(nU):
        cnt[u] = np.sum(S == U[u])
    nperms = math.factorial(len(S)) / np.prod(vector_factorial(cnt))
    return nperms


def lseq2nperms(S):
    if isinstance(S, int):
        S = [S]
    nS = len(S)
    U = np.unique(S)
    nU = len(U)
    cnt = np.zeros_like(U)
    for u in range(nU):
        cnt[u] = np.sum(S == U[u])
    lfac = logfactorial(nS)
    nperms = lfac[nS] - np.sum(lfac[cnt])
    return nperms
