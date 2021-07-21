import numpy as np


def reindex(exchangeability_blocks, method='fixleaves'):
    if method == 'fixleaves':
        exchangeability_blocks_reindexed, addcol = renumber(exchangeability_blocks)
        if addcol:
            exchangeability_blocks_reindexed = np.hstack(
                (exchangeability_blocks_reindexed, np.arange(exchangeability_blocks_reindexed.shape[1]).T))
            exchangeability_blocks_reindexed = renumber(exchangeability_blocks_reindexed)
    # TODO mixed,restart,continous

    return exchangeability_blocks_reindexed


def renumber(B):
    B1 = B[:, 0]
    U = np.unique(B1)
    addcolvec = np.zeros_like(U)
    nU = len(U)
    Br = np.zeros_like(B)
    for u in range(nU):
        idx = B1 == U[u]
        Br[idx, 0] = u * np.sign(U[u])
        if B.shape[1] > 1:
            Br[idx, 1:], addcolvec[u] = renumber(B[idx, 1:])
        elif np.sum(idx) > 1:
            addcol = True
            Br[idx] = -np.abs(B[idx])
        else:
            addcol = False

    if B.shape[1] > 1:
        addcol = np.any(addcolvec)
    return Br, addcol
