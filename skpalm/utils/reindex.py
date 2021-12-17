import numpy as np


def reindex(exchangeability_blocks, method="fixleaves"):
    if method == "continuous":
        exchangeability_blocks_reindexed = np.zeros_like(exchangeability_blocks)
        for b in range(exchangeability_blocks.shape[1]):
            cnt = 0
            if b > 0:
                for u in np.unique(exchangeability_blocks_reindexed[:, b - 1]):
                    idx = exchangeability_blocks_reindexed[:, b - 1] == u
                    exchangeability_blocks_reindexed[idx, b] = np.squeeze(
                        renumber(
                            exchangeability_blocks[idx, b][:, None],
                            start=cnt,
                            continuous=True,
                        )[0]
                    )
                    cnt += len(np.unique(exchangeability_blocks_reindexed[idx, b]))
            else:
                exchangeability_blocks_reindexed[:, b][:, None] = renumber(
                    exchangeability_blocks[:, b][:, None], start=cnt
                )[0]
    elif method == "restart":
        exchangeability_blocks_reindexed = renumber(exchangeability_blocks)[0]
    elif method == "mixed":
        exchangeability_blocks_reindexed = np.hstack(
            (
                reindex(exchangeability_blocks, method="restart")[:, :-1],
                reindex(exchangeability_blocks, method="continuous")[:, -1][:, None],
            )
        )
    elif method == "fixleaves":
        exchangeability_blocks_reindexed, addcol = renumber(exchangeability_blocks)
        if addcol:
            exchangeability_blocks_reindexed = np.hstack(
                (
                    exchangeability_blocks_reindexed,
                    (np.arange(exchangeability_blocks_reindexed.shape[0]).T + 1)[
                        :, None
                    ],
                )
            )
            exchangeability_blocks_reindexed = renumber(
                exchangeability_blocks_reindexed
            )[0]
    else:
        raise ValueError("method not implemented")

    return exchangeability_blocks_reindexed


def renumber(B, start=0, continuous=False):
    Br = np.zeros_like(B)
    B1 = B[:, 0].copy()
    U = np.unique(B1)
    addcolvec = np.zeros_like(U)
    for i, u in enumerate(U):
        idx = B1 == u
        Br[idx, 0] = (i + 1 + start) * np.sign(u)
        if Br.shape[1] > 1:
            Br[idx, 1:], addcolvec[i] = renumber(B[idx, 1:], start=0)
        elif np.sum(idx) > 1:
            addcol = True
            if continuous:
                pass
            else:
                Br[idx] = -np.abs(B[idx])
        else:
            addcol = False
    if B.shape[1] > 1:
        addcol = np.any(addcolvec)
    return Br, addcol
