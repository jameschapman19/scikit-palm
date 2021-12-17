import warnings
from copy import deepcopy

import numpy as np

from skpalm.permutations.utils.maxshuf import maxshuf
from skpalm.utils.binary import incrbin


def fliptree(
    permutation_tree, flips, conditional_monte_carlo: bool = False, max_flips=np.inf
):
    permutation_tree = deepcopy(permutation_tree)
    permutation_set = pickflip(permutation_tree, [], np.ones(len(permutation_tree)))
    permutation_set = np.hstack(
        (
            np.array(permutation_set, ndmin=2),
            np.zeros((len(permutation_set), flips - 1)),
        )
    )

    if max_flips is None:
        max_flips = maxshuf(permutation_tree, "flips")

    if flips == 1:
        pass
    elif flips == 0 or flips == max_flips:
        if flips > 1e5:
            warnings.warn(
                f"Number of possible sign flips is {max_flips}. Performing all exhaustively"
            )
        for p in range(1, max_flips):
            permutation_tree = nextflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, [])
    elif conditional_monte_carlo or flips > max_flips:
        for p in range(1, max_flips):
            permutation_tree = randomflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, [])
    else:
        if flips > max_flips / 2:
            warnings.warn(
                f"The maximum number of sign flips {max_flips} is not much larger than"
                f"the number you chose to run {flips}. This means it may take a while - "
                f"from a few seconds to several minutes. To find non-repeated sign flips"
                f"consider instead running exhaustively"
            )
        for p in range(1, flips):
            whiletest = True
            while whiletest:
                permutation_tree = randomflip(permutation_tree)
                permutation_set[:, p] = pickflip(
                    permutation_tree, [], np.ones(len(permutation_tree))
                )
                whiletest = np.any(
                    np.all(permutation_set[:, p] == permutation_set[:, : p - 1])
                )

    idx = np.argsort(permutation_set[:, 0])
    permutation_set = permutation_set[idx, :]
    return permutation_set


def nextflip(permutation_tree):
    nU = len(permutation_tree)

    for u in range(nU):
        if permutation_tree[u][1] is None:
            if (
                permutation_tree[u][2] is not None
                and len(permutation_tree[u][2][0]) > 1
            ):
                permutation_tree[u][2], incremented = nextflip(permutation_tree[u][2])
                if incremented:
                    if u > 0:
                        permutation_tree[: u - 1] = resetflips(
                            permutation_tree[: u - 1]
                        )
                    break
        else:
            if sum(permutation_tree[u][1] < permutation_tree[u][1].size):
                permutation_tree[u][1] = incrbin(permutation_tree[u][1])
                incremented = True
                if u > 0:
                    permutation_tree[: u - 1] = resetflips(permutation_tree[: u - 1])
                break
            else:
                incremented = False
    return permutation_tree, incremented


def resetflips(permutation_tree):
    for u in range(len(permutation_tree)):
        if permutation_tree[u][1] is not None and len(permutation_tree[u][2][0]) > 1:
            permutation_tree[u][2] = resetflips(permutation_tree[u][2])
        else:
            permutation_tree[u][1] = np.zeros(len(permutation_tree[u][1]))
    return permutation_tree


def randomflip(permutation_tree):
    nU = len(permutation_tree)
    for u in range(nU):
        if (
            permutation_tree[u][1] is None
            or len(permutation_tree[u][1]) == 0
            and len(permutation_tree[u][2][0]) > 1
        ):
            permutation_tree[u][2] = randomflip(permutation_tree[u][2])
        else:
            permutation_tree[u][1] = np.random.rand(len(permutation_tree[u][2])) > 0.5
    return permutation_tree


def pickflip(permutation_tree, P, sgn):
    nU = len(permutation_tree)
    if len(permutation_tree[0]) == 3:
        for u in range(nU):
            if permutation_tree[u][1] is None or len(permutation_tree[u][1]) == 0:
                bidx = sgn[u] * np.ones(len(permutation_tree[u][2]))
            else:
                bidx = np.logical_not(permutation_tree[u][1]).astype(float)
                bidx[permutation_tree[u][1].astype(bool)] = -1
            P = pickflip(permutation_tree[u][2], P, bidx)
    elif len(permutation_tree[0]) == 1:
        for u in range(nU):
            if sgn.size == 1:
                v = 0
            else:
                v = u
            P.append(sgn[v] * np.ones(len(permutation_tree[u])))
    return P
