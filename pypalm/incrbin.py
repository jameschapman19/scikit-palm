import numpy as np


def incrbin(B):
    """
    Increment binary number by 1

    Parameters
    ----------
    B : Logical vector

    Returns
    -------

    """
    k = np.where(np.logical_not(B))[0][0]
    B[:k+1] = np.logical_not(B[:k+1])
    return B

def main():
    binary_num=np.array([1,0,1])
    print(incrbin(binary_num))

if __name__ == '__main__':
    main()