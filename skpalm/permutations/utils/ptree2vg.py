import numpy as np

from skpalm.permutations.utils.permtree import permtree


def ptree2vg(permutation_tree):
    VG, n = pickvg(permutation_tree, np.isnan(permutation_tree[0][0]), 1)
    _, VG = np.unique(VG)
    _, idx = permtree(permutation_tree, 1, False)
    return VG[idx]


def pickvg(permutation_tree, within_block, n):
    nU = len(permutation_tree)
    VG = []

    if permutation_tree:
        if within_block:
            for u in range(nU):
                [VGu, n] = pickvg(
                    permutation_tree[u][2], np.isnan(permutation_tree[u][0]), n
                )
                VG = np.vstack((np.array(VG), np.array(VGu)))
        else:
            [VGu, n] = pickvg(
                permutation_tree[0][2], np.isnan(permutation_tree[0][0]), n
            )
            VG = np.repeat(VGu, (nU, 1))
    else:
        if within_block:
            sz = len(permutation_tree) - 1
            VG = np.arange(n, n + sz)
            n += sz + 1
        else:
            VG = n * np.ones(len(permutation_tree))
            n += 1
    return VG, n
