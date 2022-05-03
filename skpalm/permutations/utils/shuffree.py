import numpy as np
from sklearn.utils.validation import check_random_state

from skpalm.permutations.utils.nextperm import nextperm
from skpalm.utils.binary import d2b, incrbin
from skpalm.utils.logfactorial import logfactorial


def shuffree(
    design_matrix,
    perms,
    conditional_monte_carlo=False,
    exchangeable_errors=True,
    is_errors=False,
    random_state=None,
):
    """

    Parameters
    ----------
    design_matrix : matrix containing subject IDs
    perms : number of permutations
    conditional_monte_carlo : whether to randomly permute or ensure that we obtain all permutations
    exchangeable_errors : allow permutations
    is_errors : allow sign flips
    random_state : random state

    Returns
    -------

    """
    random_state = check_random_state(random_state)
    n_subjects = design_matrix.shape[0]
    _, seq = np.unique(design_matrix, axis=0, return_inverse=True)
    seqS = np.hstack((seq[:, None], np.arange(n_subjects)[:, None])).astype(int)
    seqS = seqS[np.argsort(seqS[:, 0])] + 1
    U = np.unique(seq + 1)

    # logs to help later
    lfac = logfactorial(n_subjects)

    maxP = 1
    maxS = 1
    lmaxP = 0
    lmaxS = 0
    if exchangeable_errors:
        nrep = np.zeros_like(U)
        for u in range(len(U)):
            nrep[u] = np.sum(seqS[:, 0] == U[u])
        lmaxP = lfac[n_subjects] - np.sum(lfac[nrep])
        maxP = np.round(np.exp(lmaxP))
        if U.size == n_subjects:
            if np.isinf(maxP):
                print(
                    f"Number of possible permutations is exp({lmaxP}) = {n_subjects}!.\n"
                )
            else:
                print(f"Number of possible permutations is {maxP} = {n_subjects}!.\n")
        else:
            if np.isinf(maxP):
                print(f"Number of possible permutations is exp({lmaxP}).\n")
            else:
                print(f"Number of possible permutations is {maxP}.\n")
    if is_errors:
        lmaxS = n_subjects * np.log(2)
        maxS = 2 ** n_subjects
        if np.isinf(maxS):
            print(f"Number of possible sign-flips is exp({lmaxS}) = 2^{n_subjects}.\n")
        else:
            print(f"Number of possible sign-flips is {maxS} = 2^{n_subjects}.\n")
    maxB = maxP * maxS
    lmaxB = lmaxP + lmaxS

    if exchangeable_errors and not is_errors:
        whatshuf = "permutations only"
    elif is_errors and not exchangeable_errors:
        whatshuf = "sign flips only"
    elif exchangeable_errors and is_errors:
        whatshuf = "permutations and sign flips"

    # ensures at least 1 perm and 1 sign flipping
    permutation_set = seqS[:, 1].copy().astype(int)
    Sset = np.ones((n_subjects, 1))

    if perms == 0 or perms > maxB:
        # run exhaustively
        print(f"Generating {maxB} shufflings ({whatshuf}).\n")
        if exchangeable_errors:
            permutation_set = np.hstack(
                (
                    permutation_set[:, np.newaxis],
                    np.zeros((n_subjects, maxP - 1), dtype=int),
                )
            )
            for p in range(1, maxP):
                seqS = nextperm(seqS)
                permutation_set[:, p] = seqS[:, 1]
        if is_errors:
            if n_subjects <= 52:
                Sset = d2b(np.arange(maxS), n_subjects).T
                Sset[np.logical_not(np.logical_not(Sset))] = -1
                Sset[np.logical_not(Sset)] = 1
                Sset = np.flipud(Sset)
            else:
                Sset = np.zeros((n_subjects, maxS), dtype=bool)
                for s in range(1, maxS):
                    Sset[:, s] = incrbin(Sset[:, s - 1])
    elif perms < maxB:
        if exchangeable_errors:
            if perms >= maxP:
                permutation_set = np.hstack(
                    (
                        permutation_set[:, None],
                        np.zeros((n_subjects, maxP - 1), dtype=int),
                    )
                )
                for p in range(1, maxP):
                    seqS = nextperm(seqS)
                    permutation_set[:, p] = seqS[:, 1]
            else:
                permutation_set = np.hstack(
                    (
                        permutation_set[:, None],
                        np.zeros((n_subjects, perms - 1), dtype=int),
                    )
                )
                if conditional_monte_carlo:
                    for p in range(perms):
                        permutation_set[:, p] = np.random.permutation(n_subjects).T
                else:
                    Pseq = np.zeros_like(permutation_set)
                    Pseq[:, 0] = seqS[:, 0]
                    for p in range(1, perms):
                        whiletest = True
                        while whiletest:
                            permutation_set[:, p] = np.random.permutation(n_subjects)
                            Pseq[:, p] = seqS[permutation_set[:, p], 0]
                            whiletest = np.any(np.all(Pseq[:, p] == Pseq[:, : p - 1]))

        if is_errors:
            if perms >= maxS:
                Sset = d2b(np.arange(maxS), n_subjects).T
                Sset[np.logical_not(np.logical_not(Sset))] = -1
                Sset[np.logical_not(Sset)] = 1
            else:
                if conditional_monte_carlo:
                    Sset = np.random.rand(n_subjects, perms) > 0.5
                    Sset[:, 0] = 0
                    Sset[np.logical_not(np.logical_not(Sset))] = -1
                    Sset[np.logical_not(Sset)] = 1
                else:
                    Sset = np.zeros((n_subjects, perms))
                    for p in range(1, perms):
                        whiletest = True
                        while whiletest:
                            Sset[:, p] = np.random.rand(n_subjects, 1) > 0.5
                            whiletest = np.any(np.all(Sset[:, p] == Sset[:, : p - 1]))
                    Sset[np.logical_not(np.logical_not(Sset))] = -1
                    Sset[np.logical_not(Sset)] = 1

    nP = permutation_set.shape[1]
    nS = Sset.shape[1]
    if nS == 1:
        Bset = permutation_set
    elif nP == 1:
        pass
        # TODO If only 1 permutation is possible, ignore it.
    elif perms == 0 or perms >= maxB:
        Bset = np.zeros((n_subjects, maxB))
        b = 0
        for p in range(permutation_set.shape[1]):
            for s in range(Sset.shape[1]):
                Bset[:, b] = permutation_set[:, p] * Sset[:, s]
                b = b + 1
    else:
        Bset = np.zeros((n_subjects, perms))
        Bset[:, 0] = np.arange(n_subjects) + 1
        if conditional_monte_carlo:
            for b in range(1, perms):
                Bset[:, b] = (
                    permutation_set[:, random_state.randint(nP)]
                    * Sset[:, random_state.randint(nS)]
                )
        else:
            bidx = np.argsort(random_state.rand(nP * nS))
            bidx = bidx[:perms]
            pidx, sidx = np.unravel_index(bidx, (nP, nS))
            for b in range(1, perms):
                Bset[:, b] = np.squeeze(permutation_set[:, pidx[b]] * Sset[:, sidx[b]])

    nB = Bset.shape[1]

    Bset = Bset[np.argsort(Bset[:, 0])]

    # TODO metric
    mtr = np.zeros(9)

    # TODO permutation matrices instead of indices

    return Bset.astype(int), nB, mtr
