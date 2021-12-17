from absl import flags
import time

from skpalm.permutations.utils.shuffree import shuffree
from skpalm.permutations.utils.shuftree import shuftree
from skpalm.permutations.utils.tree import tree

FLAGS = flags.FLAGS

def get_pset(plm,m=0,c=0):
    if FLAGS.accel is None or not "noperm" in flags.accel:
        if "EB" in plm:
            plm.Pset, plm.nP[0][0], plm.metr[0][0] = shuffree(
                plm.seq[0][0],
                FLAGS.nP0,
                conditional_monte_carlo=FLAGS.cmcp,
                exchangeable_errors=FLAGS.ee,
                is_errors=FLAGS.ise,
                random_state=None,
            )
        else:
            plm.Pset, plm.nP[0][0], plm.metr[0][0] = shuftree(
                tree(plm.EB, plm.seq),
                FLAGS.nP0,
                conditional_monte_carlo=FLAGS.cmcp,
                exchangeable_errors=FLAGS.ee,
                is_errors=FLAGS.ise,
                random_state=None,
            )
    return plm

def outer_permutation(plm, po):
    for m in range(plm.nM):
        for c in range(plm.nC(m)):
            if FLAGS.syncperms:
                pi = po
                plm.nP[m][c] = plm.nP[0][0]
            else:
                plm=get_pset(plm,m,c)

def inner_permutation(plm, po, pi):
    if FLAGS.designperinput:
        loopY=m
    else:
        loopY=plm.nY
    for y in range(loopY):



def core(plm):
    # TODO
    """
    To calculate progress
    """

    """
    Create permutation set while taking care of synchronized permutations
    """
    if FLAGS.syncperms:
        plm, p_outer=get_pset(plm)
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
