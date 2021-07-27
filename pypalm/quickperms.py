import numpy as np

from pypalm.reindex import reindex
from pypalm.shuffree import shuffree
from pypalm.shuftree import shuftree
from pypalm.tree import tree


def quickperms(design_matrix=None, exchangeability_blocks=None, perms=100, exchangeable_errors=True,
               is_errors=False, ignore_repeat_rows=False, ignore_repeat_perms=False, return_variance_groups=False):
    if design_matrix is None:
        if exchangeability_blocks is None:
            raise ValueError('Cant both be empty')
        else:
            n_subects = exchangeability_blocks.shape[0]
    else:
        if exchangeability_blocks is None:
            n_subects = design_matrix.shape[0]
        else:
            n_subjects = max(design_matrix.shape[0], exchangeability_blocks.shape[0])

    # Create shufflings
    if exchangeability_blocks is None:
        simple = True
        permutation_set = shuffree(design_matrix, perms, ignore_repeat_rows, exchangeable_errors, is_errors)
    else:
        simple = False
        exchangeability_blocks = reindex(exchangeability_blocks, 'fixleaves')
        permutation_tree = tree(exchangeability_blocks, design_matrix)
        permutation_set = shuftree(permutation_tree, perms, ignore_repeat_perms,
                                   exchangeable_errors=exchangeable_errors, is_errors=is_errors)

    # Define variance groups
    if return_variance_groups:
        if simple:
            variance_groups = np.ones(n_subjects, 1)
        else:
            pass
            # variance_groups = ptree2vg(Ptree)
        return permutation_set, variance_groups
    return permutation_set


def main():
    import pandas as pd
    np.random.seed(42)
    EB = pd.read_csv('C:/Users/chapm/OneDrive/Documents/PALM-master/eb.csv',header=None).values
    M = np.random.normal(5, size=(EB.shape[0], 5))
    A = quickperms(M, EB, 1698, ignore_repeat_perms=False, is_errors=True)
    function_perms = len(np.unique(A[0], axis=1, return_counts=True)[1])
    print(f'function calculated permutations without sign flips: {function_perms}')



if __name__ == "__main__":
    main()
