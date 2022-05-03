import numpy as np

from skpalm.utils.reindex import reindex
from .utils.shuffree import shuffree
from .utils.shuftree import shuftree
from .utils.tree import tree


def quickperms(
        design_matrix: np.ndarray = None,
        exchangeability_blocks: np.ndarray = None,
        perms: int = 100,
        exchangeable_errors: bool = True,
        is_errors: bool = False,
        ignore_repeat_rows: bool = False,
        ignore_repeat_perms: bool = False,
        return_variance_groups: bool = False,
):
    """

    Parameters
    ----------
    design_matrix :
        Design matrix. It can be the full, unpartitioned design, or
        if there are nuisance, simply the part that contains the EVs
        of interest. This distinction is only relevant if there are
        discrete EVs of interest and nuisance variables that are
        continuous. You may consider a partitioning as in the
        function palm_partition.m.
        If you have no idea what to use, it is in general, it is in
        general safe to use as M simply a vector (1:N)'.
        You can also simply leave it empty ([]) if EB is supplied, and
        by default it will be (1:N)'. If an EB isn't supplied, you can
        simply use N and by default it will be (1:N)'.
    exchangeability_blocks :
        Exchangeability blocks (can be multi-level). For freely
        exchangeable data, use ones(N,1). You can also leave it
        empty ([]) if a valid, non-empty M was supplied.
    perms :
        Desired number of permutations. The actual number may be
        smaller if N is too small. Use 0 for exhaustive.
    exchangeable_errors :
        True/False indicating whether to assume exchangeable errors,
        which allow permutations.
    is_errors :
        True/False indicating whether to assume independent and
        symmetric errors, which allow sign-flippings.
    ignore_repeat_rows :
        True/False indicating whether repeated rows in the design
        should be be ignored. Default is false.
    ignore_repeat_perms :
        True/False indicating whether repeated permutations should
        be ignored. Default is false.
    return_variance_groups

    Returns
    -------
    permutation_set : Permutation set. It contains one permutation per column.
    """
    if design_matrix is None:
        if exchangeability_blocks is None:
            raise ValueError("Cant both be empty")
        else:
            n_subjects = exchangeability_blocks.shape[0]
            design_matrix = np.expand_dims(np.arange(n_subjects), 1)
    else:
        if exchangeability_blocks is None:
            n_subjects = design_matrix.shape[0]
        else:
            n_subjects = max(design_matrix.shape[0], exchangeability_blocks.shape[0])

    # Create shufflings
    if exchangeability_blocks is None:
        simple = True
        permutation_set = shuffree(
            design_matrix, perms, ignore_repeat_rows, exchangeable_errors, is_errors
        )
    else:
        simple = False
        exchangeability_blocks = reindex(exchangeability_blocks, "fixleaves")
        permutation_tree = tree(exchangeability_blocks, design_matrix)
        permutation_set = shuftree(
            permutation_tree,
            perms,
            ignore_repeat_perms,
            exchangeable_errors=exchangeable_errors,
            is_errors=is_errors,
        )

    # Define variance groups
    if return_variance_groups:
        if simple:
            variance_groups = np.ones(n_subjects)
        else:
            pass
            # variance_groups = ptree2vg(Ptree)
        return permutation_set, variance_groups
    return permutation_set
