import random
import warnings
from copy import deepcopy

import numpy as np

from pypalm.maxshuf import maxshuf


def permtree(permutation_tree, perms, conditional_monte_carlo=False, max_perms=np.inf):
    permutation_tree = deepcopy(permutation_tree)
    permutation_set = pickperm(permutation_tree, [])
    permutation_set = np.hstack((np.array(permutation_set, ndmin=2).T, np.zeros((len(permutation_set), perms - 1))))

    maxP = maxshuf(permutation_tree, 'permutations')

    if perms == 1:
        pass
    elif perms == 0 or perms == maxP:
        if perms > 1e5:
            warnings.warn(f'Number of possible sign flips is {maxP}. Performing all exhaustively')
        for p in range(1, maxP):
            permutation_tree = nextperm(permutation_tree)
            permutation_set[:, p] = pickperm(permutation_tree, [])
    elif conditional_monte_carlo or perms > maxP:
        for p in range(1, maxP):
            permutation_tree = randomperm(permutation_tree)
            permutation_set[:, p] = pickperm(permutation_tree, [])
    else:
        if perms > maxP / 2:
            warnings.warn(f'The maximum number of sign flips {maxP} is not much larger than'
                          f'the number you chose to run {perms}. This means it may take a while - '
                          f'from a few seconds to several minutes. To find non-repeated sign flips'
                          f'consider instead running exhaustively')
        for p in range(1, perms):
            whiletest = True
            while whiletest:
                permutation_tree = randomperm(permutation_tree)
                permutation_set[:, p] = pickperm(permutation_tree, [])
                whiletest = np.any(np.all(permutation_set[:, p] == permutation_set[:, :p - 1]))

    idx = np.argsort(permutation_set[:, 0])
    permutation_set = permutation_set[idx, :]
    return permutation_set


def nextperm(permutation_tree):
    nU = len(permutation_tree)
    sucs = np.zeros(nU)

    if len(permutation_tree[0]) > 1:
        for u in range(nU):
            permutation_tree[u][2], sucs[u] = nextperm(permutation_tree[u][2])
            if sucs[u]:
                if u > 0:
                    permutation_tree[:u - 1, :] = resetperms(permutation_tree[:u - 1])
                break
            elif not np.isnan(permutation_tree[u][0]):
                permutation_tree[u][0][:, 2] = np.arange(len(permutation_tree[u][0])).T
                tmp, sucs[u] = nextperm(permutation_tree[u][0])
                if sucs[u]:
                    permutation_tree[u][0] = tmp
                    permutation_tree[u][2] = resetperms(permutation_tree[u][2])
                    permutation_tree[u][2] = permutation_tree[u][2][permutation_tree[u][0][:, 2]]
                    if u > 0:
                        permutation_tree[:u - 1, :] = resetperms(permutation_tree[:u - 1])
    return permutation_tree


def resetperms(permutation_tree):
    if len(permutation_tree[0]) > 1:
        for u in range(len(permutation_tree)):
            if np.isnan(permutation_tree[u][0]):
                permutation_tree[u][2] = resetperms(permutation_tree[u][2])
            else:
                permutation_tree[u][0][:, 2] = permutation_tree[u][0][:, 1]
                permutation_tree[u][0], idx = permutation_tree[u][0][np.argsort(permutation_tree[u][0][:, 0])]
                permutation_tree[u][2] = permutation_tree[u][2][idx]
                permutation_tree[u][2] = resetperms(permutation_tree[u][2])

    return permutation_tree


def randomperm(permutation_tree):
    nU = len(permutation_tree)
    for u in range(nU):
        if not np.any(np.isnan(permutation_tree[u][0])):
            tmp = permutation_tree[u][0][0]
            permutation_tree[u][0] = random.sample(permutation_tree[u][0][0]) * 3
            if np.any(tmp != permutation_tree[u][0][0]):
                permutation_tree[u][2] = [permutation_tree[u][2][k] for k in permutation_tree[u][0][2]]
        if len(permutation_tree[u][2][0]) > 1:
            random.shuffle(permutation_tree[u][2])
    return permutation_tree


def pickperm(permutation_tree, P):
    nU = len(permutation_tree)
    if len(permutation_tree[0]) == 3:
        for u in range(nU):
            P = pickperm(permutation_tree[u][2], P)
    elif len(permutation_tree[0]) == 1:
        for u in range(nU):
            P[len(P):len(P) + len(permutation_tree[u][0])] = permutation_tree[u][0]
    return P
