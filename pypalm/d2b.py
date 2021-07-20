import numpy as np

def d2b(d,n):
    b=np.array([list(np.binary_repr(d_,n)) for d_ in d]).astype(int)
    return b