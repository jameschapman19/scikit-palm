import numpy as np


def nextperm(a):
    n = a.shape[0]
    j = n - 1

    while j > 0 and a[j - 1, 0] >= a[j, 0]:
        j = j - 1

    if j > 0:
        l = n
        while a[j - 1, 0] >= a[l - 1, 0]:
            l = l - 1
        tmp = a[j - 1, :].copy()
        a[j - 1, :] = a[l - 1, :].copy()
        a[l - 1, :] = tmp.copy()
        k = j + 1
        l = n
        while k < l:
            tmp = a[k - 1, :].copy()
            a[k - 1, :] = a[l - 1, :].copy()
            a[l - 1, :] = tmp.copy()
            k = k + 1
            l = l - 1
    else:
        a = np.flipud(a)
    return a
