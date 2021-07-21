import numpy as np
import math

from pypalm.logfactorial import logfactorial


def maxshuf(permutation_tree, stype='permutations', log=False):
    if stype == 'permutations':
        maxb = maxpermnode(permutation_tree, log)
    elif stype == 'flips':
        maxb = maxflipnode(permutation_tree, log)
    elif stype == 'both':
        maxp = maxpermnode(permutation_tree, log)
        maxs = maxflipnode(permutation_tree, log)
        maxb = maxp * maxs


def maxpermnode(permutation_tree, log=False):
    for u in range(len(permutation_tree)):
        nperms = nperms * seq2nperms(permutation_tree[u][:, 0])
        if len(permutation_tree[u][2]) > 1:
            nperms = maxpermnode(permutation_tree[u], nperms)
    return nperms

def maxflipnode(permutation_tree, nsignflips):
    for u in range(len(permutation_tree)):
        if len(permutation_tree[u][2]) > 1:
            nsignflips = maxflipnode(permutation_tree[u][2], nsignflips)
        nsignflips = nsignflips * 2 ** len(permutation_tree[u][1])
    return nsignflips

def lmaxpermnode(permutation_tree,nperms):
    for u in range(len(permutation_tree)):
        nperms=nperms+lseq2nperms(permutation_tree[u][0][:,0])
        if len(permutation_tree[u][2][0])>1:
            nperms=lmaxpermnode(permutation_tree[u][2],nperms)

def lmaxflipnode(permutation_tree,nsignflips):
    for u in range(len(permutation_tree)):
        if len(permutation_tree[u][2][0])>1:
            nsignflips=lmaxflipnode(permutation_tree[u][2],nsignflips)
        nsignflips = nsignflips + len(permutation_tree[u][1])
    return nsignflips


def seq2nperms(S):
    U = np.unique(S)
    nU = len(U)
    cnt = np.zeros_like(U)
    for u in range(nU):
        cnt[u] = np.sum(S == U[u])
    nperms = math.factorial(len(S)) / np.prod(math.factorial(cnt))
    return nperms

def lseq2nperms(S):
    nS=len(S)
    U=np.unique(S)
    nU=len(U)
    cnt=np.zeros_like(U)
    for u in range(nU):
        cnt[u]=np.sum(S==U[u])
    lfac=logfactorial(nS)
    nperms=lfac[nS]-np.sum(lfac[cnt])
    return nperms




