import warnings

import numpy as np

from pypalm.incrbin import incrbin
from pypalm.maxshuf import maxshuf


def fliptree(permutation_tree, perms, conditional_monte_carlo=False, max_perms=np.inf):
    permutation_set = pickflip(permutation_tree, [])
    permutation_set = np.hstack((np.array(permutation_set, ndmin=2).T, np.zeros((len(permutation_set), perms - 1))))

    maxP = maxshuf(permutation_tree, 'flips')

    if perms == 1:
        pass
    elif perms == 0 or perms == maxP:
        if perms > 1e5:
            warnings.warn(f'Number of possible sign flips is {maxP}. Performing all exhaustively')
        for p in range(1, maxP):
            permutation_tree = nextflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, [])
    elif conditional_monte_carlo or perms > maxP:
        for p in range(1, maxP):
            permutation_tree = randomflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, [])
    else:
        if perms > maxP / 2:
            warnings.warn(f'The maximum number of sign flips {maxP} is not much larger than'
                          f'the number you chose to run {perms}. This means it may take a while - '
                          f'from a few seconds to several minutes. To find non-repeated sign flips'
                          f'consider instead running exhaustively')
        for p in range(1, perms):
            whiletest = True
            while whiletest:
                permutation_tree = randomflip(permutation_tree)
                permutation_set[:, p] = pickflip(permutation_tree, [])
                whiletest = np.any(np.all(permutation_set[:, p] == permutation_set[:, :p - 1]))

    idx = np.argsort(permutation_set[:, 0])
    permutation_set = permutation_set[idx, :]
    return permutation_set


def nextflip(permutation_tree):
    nU = len(permutation_tree)

    for u in range(nU):
        if permutation_tree[u][1] is None:
            if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
                permutation_tree[u][2], incremented = nextflip(permutation_tree[u][2])
                if incremented:
                    if u > 0:
                        permutation_tree[:u - 1] = resetflips(permutation_tree[:u - 1])
                    break
        else:
            if sum(permutation_tree[u][1] < permutation_tree[u][1].size):
                permutation_tree[u][1] = incrbin(permutation_tree[u][1])
                incremented = True
                if u > 0:
                    permutation_tree[:u - 1] = resetflips(permutation_tree[:u - 1])
                break
            else:
                incremented = False
    return permutation_tree, incremented


def resetflips(permutation_tree):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][1] is not None and len(permutation_tree[u][2][0]) > 1:
            permutation_tree[u][2] = resetflips(permutation_tree[u][2])
        else:
            permutation_tree[u][1] = np.zeros(len(permutation_tree
                                                  [u][1]))
    return permutation_tree


def randomflip(permutation_tree):
    nU = len(permutation_tree)
    for u in range(nU):
        if permutation_tree[u][2] is not None and len(permutation_tree[u][2][0]) > 1:
            permutation_tree[u][2] = randomflip(permutation_tree[u][2])
        else:
            permutation_tree[u][1] = np.random.rand(len(permutation_tree[u][2][0])) > 0.5
    return permutation_tree


def pickflip(permutation_tree, P, sgn):
    nU = len(permutation_tree)
    if len(permutation_tree[0]) == 3:
        for u in range(nU):
            if permutation_tree[u][1] is None:
                bidx = np.ones(len(permutation_tree[u][2]))
            else:
                bidx = np.logical_not(permutation_tree[u][1])
                bidx[permutation_tree[u][1]] = -1
            P = pickflip(permutation_tree[u][2], P, bidx)
    elif len(permutation_tree[0]) == 1:
        for u in range(nU):
            if sgn.size==1:
                v=1
            else:
                v=u
            P[len(P)] = np.sign(v)*np.ones(len(permutation_tree[u]))
    return P
