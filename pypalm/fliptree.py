import numpy as np

import numpy as np

from pypalm.maxshuf import maxshuf


def fliptree(permutation_tree, perms, conditional_monte_carlo=False):
    permutation_set = pickflip(permutation_tree, []).T
    permutation_set = np.hstack((permutation_set, np.zeros((len(permutation_set), perms - 1))))

    maxP = maxshuf(permutation_tree, 'perms')

    if perms == 1:
        pass
    elif perms == 0 or perms == maxP:
        if perms > 1e5:
            # TODO warning
            pass
        for p in range(1, maxP):
            permutation_tree = nextflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, []).T
    elif conditional_monte_carlo or perms > maxP:
        for p in range(1, maxP):
            permutation_tree = randomflip(permutation_tree)
            permutation_set[:, p] = pickflip(permutation_tree, []).T
    else:
        if perms > maxP / 2:
            pass
            # TODO warning
        for p in range(1, perms):
            whiletest = True
            while whiletest:
                permutation_tree = randomflip(permutation_tree)
                permutation_set[:, p] = pickflip(permutation_tree, []).T
                whiletest = np.any(np.all(permutation_set[:, p] == permutation_set[:, :p - 1]))

    idx = np.argsort(permutation_set[:, 0])
    permutation_set = permutation_set[idx, :]
    return permutation_set


def nextflip(permutation_tree):
    nU=len(permutation_tree)
    sucs=np.zeros(nU)

    if len(permutation_tree[0])>1:
        for u in range(nU):
            permutation_tree[u][2],sucs[u]=nextflip(permutation_tree[u][2])
            if sucs[u]:
                if u>0:
                    permutation_tree[:u-1,:]=resetflips(permutation_tree[:u-1])
                break
            elif not np.isnan(permutation_tree[u][0]):
                permutation_tree[u][0][:,2]=np.arange(len(permutation_tree[u][0])).T
                tmp,sucs[u]=nextflip(permutation_tree[u][0])
                if sucs[u]:
                    permutation_tree[u][0]=tmp
                    permutation_tree[u][2]=resetflips(permutation_tree[u][2])
                    permutation_tree[u][2]=permutation_tree[u][2][permutation_tree[u][0][:,2]]
                    if u>0:
                        permutation_tree[:u-1,:]=resetflips(permutation_tree[:u-1])
    return permutation_tree


def resetflips(permutation_tree):
    if len(permutation_tree[0])>1:
        for u in range(len(permutation_tree)):
            if np.isnan(permutation_tree[u][0]):
                permutation_tree[u][2]=resetflips(permutation_tree[u][2])
            else:
                permutation_tree[u][0][:,2]=permutation_tree[u][0][:,1]
                permutation_tree[u][0],idx = permutation_tree[u][0][np.argsort(permutation_tree[u][0][:,0])]
                permutation_tree[u][2]=permutation_tree[u][2][idx]
                permutation_tree[u][2]=resetflips(permutation_tree[u][2])

    return permutation_tree


def randomflip(permutation_tree):
    nU = len(permutation_tree)
    for u in range(nU):
        if not np.isnan(permutation_tree[u][0][0]):
            tmp = permutation_tree[u][0][:, 0]
            permutation_tree[u][0] = permutation_tree[u][0][np.random.permutation(len(permutation_tree[u][0]))]
            if np.any(tmp != permutation_tree[u][0][:, 0]):
                permutation_tree[u][2] = permutation_tree[u][2][permutation_tree[u][0][:, 2]]
        if len(permutation_tree[u][2][0]) > 1:
            permutation_tree[u][2] = randomflip(permutation_tree[u][2])
    return permutation_tree


def pickflip(permutation_tree, P):
    nU = len(permutation_tree)
    if len(permutation_tree[0]) == 3:
        for u in range(nU):
            P = pickflip(permutation_tree[u][2], P)
    elif len(permutation_tree[0]) == 1:
        for u in range(nU):
            P[len(P):len(P) + len(permutation_tree[u][0])] = permutation_tree[u][0]
    return P
