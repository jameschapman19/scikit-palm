import numpy as np


def tree(exchangeability_blocks, design_matrix=None):
    if design_matrix is None:
        design_matrix = np.arange(exchangeability_blocks.shape[0])

    Bs = exchangeability_blocks[np.argsort(exchangeability_blocks[:, 0])]

    O = np.arange(1, design_matrix.shape[0] + 1)

    wholeblock = np.all(exchangeability_blocks[0] > 0)
    permutation_tree = [[None] * 3]
    permutation_tree[0][0], permutation_tree[0][2] = maketree(
        exchangeability_blocks[:, 1:], design_matrix, O, wholeblock, wholeblock
    )
    if wholeblock:
        permutation_tree[0][1] = np.zeros((len(permutation_tree[2]), 1))
    else:
        permutation_tree[0][1] = np.array([])
    return permutation_tree


def maketree(exchangeability_blocks, design_matrix, O, wholeblock=False, nosf=False):
    B1 = exchangeability_blocks[:, 0]
    U = np.unique(B1)
    nU = len(U)
    if exchangeability_blocks.shape[1] > 1:
        permutation_tree = [[None] * 3 for _ in range(nU)]
    else:
        permutation_tree = [[None] for _ in range(nU)]

    for u in range(nU):
        idx = B1 == U[u]

        if exchangeability_blocks.shape[1] > 1:
            wholeblockb = exchangeability_blocks[np.where(idx)[0][0], 0] > 0
            permutation_tree[u][0], permutation_tree[u][2] = maketree(
                exchangeability_blocks[idx, 1:],
                design_matrix[idx, :],
                O[idx],
                wholeblockb,
                wholeblockb or nosf,
            )
            permutation_tree[u][1] = np.array([])
            if nosf:
                permutation_tree[u][1] = np.array([])
            elif len(permutation_tree[u][2]) > 1:
                if isinstance(permutation_tree[u][0], np.ndarray):
                    if np.isnan(permutation_tree[u][0][0]):
                        permutation_tree[u][1] = np.array([])
                else:
                    permutation_tree[u][1] = np.zeros((len(permutation_tree[u][2]), 1))
            else:
                permutation_tree[u][1] = np.zeros((len(permutation_tree[u][2]), 1))
        else:
            permutation_tree[u][0] = O[idx]

    if wholeblock and nU > 1:
        Ms = design_matrix[np.argsort(B1)]
        _, S = np.unique(
            np.reshape(Ms.T, (int(Ms.size / nU), nU)).T, axis=0, return_inverse=True
        )
        idx = np.argsort(S)
        S = S[idx] + 1
        S = [S, np.arange(1, S.size + 1), np.arange(1, S.size + 1)]
        permutation_tree = [permutation_tree[idx_] for idx_ in idx]

    elif wholeblock and nU == 1:
        S = [1, 1, 1]
    else:
        S = np.nan
    return S, permutation_tree
