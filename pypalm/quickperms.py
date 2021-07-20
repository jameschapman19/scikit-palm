import numpy as np
from pypalm.shuffree import shufree
from pypalm.reindex import reindex
from pypalm.tree import tree
from pypalm.shuftree import shuftree

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
        permutation_set = shufree(design_matrix, perms, ignore_repeat_rows, exchangeable_errors, is_errors)
    else:
        simple = False
        exchangeability_blocks = reindex(exchangeability_blocks, 'fixleaves')
        permutation_tree = tree(exchangeability_blocks, design_matrix)

        permutation_set = shuftree(permutation_tree,perms,ignore_repeat_perms, exchangeable_errors=exchangeable_errors, is_errors=is_errors)

    # Define variance groups
    if return_variance_groups:
        if simple:
            variance_groups = np.ones(n_subjects, 1)
        else:
            variance_groups = ptree2vg(Ptree)
        return permutation_set, variance_groups
    return permutation_set
