import numpy as np
from sklearn.utils.validation import check_random_state

from pypalm.maxshuf import maxshuf
from pypalm.swapfmt import swapfmt


def shuftree(permutation_tree, perms, ignore_repeat_perms=False, exchangeable_errors=True, is_errors=False,
             random_state=None):
    random_state = check_random_state(random_state)
    maxP = 1
    maxS = 1
    if exchangeable_errors:
        lmaxP = maxshuf(permutation_tree, 'perms', True)
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
        if exchangeable_errors:
            permutation_set = permtree(permutation_tree, int(np.round(maxP)), False, int(np.round(maxP)))
        if is_errors:
            Sset = fliptree(permutation_tree, int(np.round(maxP)), False, int(np.round(maxP)))
    elif perms < maxB:
        if exchangeable_errors:
            if perms > maxP:
                Sset = permtree(permutation_tree, int(np.round(maxP)), ignore_repeat_perms, False, int(np.round(maxP)))
            else:
                Sset = permtree(permutation_tree, perms, ignore_repeat_perms, False, int(np.round(maxP)))
        if is_errors:
            if perms > maxS:
                Sset = fliptree(permutation_tree, int(np.round(maxS)), ignore_repeat_perms, False, int(np.round(maxS)))
            else:
                Sset = fliptree(permutation_tree, perms, ignore_repeat_perms, False, int(np.round(maxS)))

    nP = permutation_set.size()
    nS = Sset.size()

    if nP > 0 and nS == 0:
        Sset = permutation_set
        nS = 1
    elif nP == 0 and nS > 0:
        permutation_set = Sset
        nP = 1

    if nS == 1:
        Bset = permutation_set
    elif nP == 1:
        Bset = Sset
    elif perms == 0 and perms > maxB:
        # As many as possible
        Bset = []
        for p in range(permutation_set.shape[1]):
            for s in range(Sset.shape[1]):
                Bset.append(permutation_set[p] * Sset[s])
    else:
        Bset = []
        Bset.append(permutation_set[0] * Sset[0])
        if ignore_repeat_perms:
            for b in range(1, perms):
                Bset.append(permutation_set[random_state.randint(nP)] * Sset[random_state.randint(nS)])
        else:
            bidx = np.argsort(random_state.rand(nP * nS))
            bidx = bidx[:perms]
            pidx, sidx = np.unravel_index(bidx, (nP, nS))
            for b in range(1, perms):
                Bset.append(np.squeeze(permutation_set[:, pidx[b]] * Sset[:, sidx[b]]))
    nB = Bset.size()

    Bset = swapfmt(Bset)

    # TODO metric
    mtr = np.zeros(9)

    return Bset, nB, mtr
