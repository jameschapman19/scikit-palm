from copy import deepcopy

import numpy as np
from sklearn.utils.validation import check_random_state

from pypalm.fliptree import fliptree
from pypalm.maxshuf import maxshuf
from pypalm.permtree import permtree


def shuftree(permutation_tree, perms, conditional_monte_carlo=False, exchangeable_errors=True, is_errors=False,
             random_state=None):
    permutation_set = None
    Sset = None
    random_state = check_random_state(random_state)
    maxP = 1
    maxS = 1
    if exchangeable_errors:
        lmaxP = maxshuf(permutation_tree, 'permutations', True)
        maxP = np.exp(lmaxP)
        if np.isinf(maxP):
            print(f'Number of possible permutations is exp({lmaxP}).\n')
        else:
            print(f'Number of possible permutations is {maxP}.\n')
    if is_errors:
        lmaxS = maxshuf(permutation_tree, 'flips', True)
        maxS = np.exp(lmaxS)
        if np.isinf(maxS):
            print(f'Number of possible sign-flips is exp({lmaxS}).\n')
        else:
            print(f'Number of possible sign-flips is {maxS}.\n')

    maxB = maxP * maxS

    if exchangeable_errors and not is_errors:
        whatshuf = 'permutations only'
    elif is_errors and not exchangeable_errors:
        whatshuf = 'sign flips only'
    elif exchangeable_errors and is_errors:
        whatshuf = 'permutations and sign flips'

    if perms == 0 or perms > maxB:
        # run exhaustively
        print(f'Generating {maxB} shufflings ({whatshuf}).\n')
        if exchangeable_errors:
            permutation_set = permtree(permutation_tree, int(np.round(maxP)), np.round(maxP))
        if is_errors:
            Sset = fliptree(permutation_tree, int(np.round(maxP)), np.round(maxP))
    elif perms < maxB:
        if exchangeable_errors:
            if perms > maxP:
                permutation_set = permtree(permutation_tree, int(np.round(maxP)), conditional_monte_carlo,
                                           np.round(maxP))
            else:
                permutation_set = permtree(permutation_tree, perms, conditional_monte_carlo, np.round(maxP))
        if is_errors:
            if perms > maxS:
                Sset = fliptree(permutation_tree, int(np.round(maxS)), conditional_monte_carlo, np.round(maxS))
            else:
                Sset = fliptree(permutation_tree, perms, conditional_monte_carlo, np.round(maxS))

    if permutation_set is not None:
        nP = permutation_set.T.shape[0]
    else:
        nP = 0
    if Sset is not None:
        nS = Sset.T.shape[0]
    else:
        nS = 0

    if nP > 0 and nS == 0:
        Sset = deepcopy(permutation_set)
        nS = 1
    elif nP == 0 and nS > 0:
        permutation_set = deepcopy(Sset)
        nP = 1

    Bset = np.empty_like(permutation_set)
    if nS == 1:
        Bset = permutation_set
    elif nP == 1:
        Bset = Sset
    elif perms == 0 and perms > maxB:
        # As many as possible
        b = 0
        for p in range(permutation_set.shape[1]):
            for s in range(Sset.shape[1]):
                Bset[:,b] = permutation_set[p] * Sset[s]
                b += 1
    else:
        Bset[:,0] = permutation_set[:,0] * Sset[:,0]
        if conditional_monte_carlo:
            for b in range(1, perms):
                Bset[b] = permutation_set[random_state.randint(nP)] * Sset[random_state.randint(nS)]
        else:
            bidx = np.argsort(random_state.rand(nP * nS))
            bidx = bidx[:perms]
            pidx, sidx = np.unravel_index(bidx, (nP, nS))
            for b in range(1, perms):
                Bset[:,b] = permutation_set[:, pidx[b]] * Sset[:, sidx[b]]
    nB = Bset.shape[1]

    # TODO metric
    mtr = np.zeros(9)

    return Bset, nB, mtr
