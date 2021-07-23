import numpy as np
from sklearn.preprocessing import OrdinalEncoder


def reindex(exchangeability_blocks, method='fixleaves'):
    oe = OrdinalEncoder()
    exchangeability_blocks = oe.fit_transform(exchangeability_blocks) + 1

    if method == 'continuous':
        exchangeability_blocks_reindexed = renumber(exchangeability_blocks, continuous=True)
    if method == 'restart':
        exchangeability_blocks_reindexed = renumber(exchangeability_blocks, continuous=False)
    if method == 'mixed':
        exchangeability_blocks_reindexed = np.hstack(
            (renumber(exchangeability_blocks, continuous=True), renumber(exchangeability_blocks, continuous=False)))
    if method == 'fixleaves':
        exchangeability_blocks_reindexed = renumber(exchangeability_blocks, continuous=False)
        exchangeability_blocks_reindexed = np.hstack((exchangeability_blocks_reindexed, (np.arange(exchangeability_blocks_reindexed.shape[0]).T+1)[:,None]))
        exchangeability_blocks_reindexed = renumber(exchangeability_blocks_reindexed, continuous=False)
        """
        exchangeability_blocks_reindexed, addcol = renumber(exchangeability_blocks)
        if addcol:
            exchangeability_blocks_reindexed = np.hstack(
                (exchangeability_blocks_reindexed, np.arange(exchangeability_blocks_reindexed.shape[1]).T))
            exchangeability_blocks_reindexed = renumber(exchangeability_blocks_reindexed)
        """
    # TODO mixed,restart,continous

    return exchangeability_blocks_reindexed


def renumber(B, start=0, continuous=True):
    Br = np.zeros_like(B)
    B1 = B[:, 0].copy()
    U = np.unique(B1)
    for u in U:
        idx = B1 == u
        if Br.shape[1] > 1:
            if continuous:
                Br[idx, 1:] = renumber(B[idx, 1:], start=start + len(U))
            else:
                Br[idx, 1:] = renumber(B[idx, 1:], start=0)
        Br[idx, 0] = start + u
    return Br

    """
    B1 = B[:, 0]
    U = np.unique(B1)
    addcolvec = np.zeros_like(U)
    nU = len(U)
    Br = np.zeros_like(B)
    for u in range(nU):
        idx = B1 == U[u]
        Br[idx, 0] = (u+1)
        if B.shape[1] > 1:
            Br[idx, 1:], addcolvec[u] = renumber(B[idx, 1:])
        elif np.sum(idx) > 1:
            addcol = True
            Br[idx] = -np.abs(B[idx])
        else:
            addcol = False

    if B.shape[1] > 1:
        addcol = np.any(addcolvec)
    """
    return Br, addcol
