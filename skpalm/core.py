from absl import flags
import time

from skpalm.permutations.utils.shuffree import shuffree
from skpalm.permutations.utils.shuftree import shuftree
from skpalm.permutations.utils.tree import tree

FLAGS = flags.FLAGS


def outer_permutation(plm, po):
    for m in range(plm.nM):
        for c in range(plm.nC(m)):
            if FLAGS.syncperms:
                pi = po
                plm.nP[m][c] = plm.nP[0][0]


def inner_permutation(plm, po, pi):
    pass


def core(plm):
    # TODO
    """
    To calculate progress
    """

    """
    Create permutation set while taking care of synchronized permutations
    """
    if FLAGS.syncperms:
        if FLAGS.accel is None or not "noperm" in flags.accel:
            if "EB" in plm:
                plm.Pset, plm.nP, plm.metr = shuffree(
                    plm.seq[0][0],
                    FLAGS.nP0,
                    conditional_monte_carlo=FLAGS.cmcp,
                    exchangeable_errors=FLAGS.ee,
                    is_errors=FLAGS.ise,
                    random_state=None,
                )
            else:
                plm.Pset, plm.nP, plm.metr = shuftree(
                    tree(plm.EB, plm.seq),
                    FLAGS.nP0,
                    conditional_monte_carlo=FLAGS.cmcp,
                    exchangeable_errors=FLAGS.ee,
                    is_errors=FLAGS.ise,
                    random_state=None,
                )
            p_outer = plm.nP
        else:
            p_outer = 1
    else:
        p_outer = 1

    ticP = time.time()
    for po in p_outer:
        outer_permutation(plm, po)

    tocP = time.time() - ticP
    print(f"Elapsed time with permutations : {tocP}")

    ticS = time.time()
    tocS = time.time() - ticS

    print()

    print(f"Overall elapsed time : ")
