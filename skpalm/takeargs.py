import numpy as np
from absl import flags

from skpalm.permutations.utils.ptree2vg import ptree2vg
from skpalm.permutations.utils.tree import tree
from skpalm.plm_default import plm_default
from skpalm.utils.miscread import miscread
from skpalm.utils.ready import ready
from skpalm.utils.reindex import reindex

FLAGS = flags.FLAGS


def takeargs():
    if FLAGS.T:
        FLAGS.tfce = {"uni_do": True, "npc_do": True, "mv_do": True, "stat": "tfce"}
    if FLAGS.vg == "single":
        FLAGS.singlevg = True
    else:
        FLAGS.singlevg = False
    if FLAGS.C is not None:
        FLAGS.cluster = {
            "uni_do": True,
            "uni_thr": FLAGS.C,
            "npc_do": True,
            "npc_thr": FLAGS.C,
            "mv_do": True,
            "mv_thr": FLAGS.C,
        }
    if FLAGS.npccon:
        FLAGS.NPC = True
        FLAGS.syncperms = True
    if FLAGS.quiet:
        FLAGS.showprogress = False

    plm = plm_default()
    if FLAGS.m is not None:
        plm.nm = len(FLAGS.m)
        if plm.nm == 1:
            FLAGS.m = [FLAGS.m] * len(FLAGS.i)
    if FLAGS.accel is not None:
        methlist = FLAGS.accel
        flags.accel = dict.fromkeys(FLAGS.accel)
        if "negbin" in flags.accel:
            pass
        elif "tail" in flags.accel:
            pass
        elif "gamma" in flags.accel:
            pass
        elif "lowrank" in flags.accel:
            pass

    """
    Read Inputs
    """
    if FLAGS.m is None:
        FLAGS.m = [None] * len(FLAGS.i)
    plm.Yset = [ready(i, maskstruct) for i, maskstruct in zip(FLAGS.i, flags.m)]
    if plm.subjidx is not None:
        plm.Yset = [Y[plm.subjidx] for Y in plm.Yset]
    """
    Check all data have the same size
    """
    if FLAGS.npcmod or FLAGS.MV:
        # TODO check sizes
        pass
    """
    Check no empty modalities
    """

    """
    If MV then check Y is full rank
    """

    """
    Adjust EE and ISE options
    """
    if not FLAGS.ee and not FLAGS.ise:
        FLAGS.ee = True

    if not FLAGS.cmcx:
        seqtmp = np.zeros(plm.N, sum(plm.nC))
        plm.seq = [] * plm.nM
        for m in range(plm.nM):
            plm.seq[m] = [] * plm.nC
            for c in range(plm.nC):
                # TODO
                raise NotImplementedError  # Line 2364 https://github.com/andersonwinkler/PALM/blob/master/palm_takeargs.m
                # Xtmp=partition()
                # [~,~,plm.seq{m}{c}] = unique(Xtmp,'rows');
                # seqtmp(:,j) = plm.seq{m}{c};
    else:
        plm.seq = [] * plm.nM
        for m in range(plm.nM):
            plm.seq[m] = [] * plm.nC
            for c in range(plm.nC):
                plm.seq[m][c] = np.arange(plm.N)

    """
    Read the exchangeability blocks. If none is specified, all observations are assumed to be in the same large block
    """
    if FLAGS.eb is None:
        plm.EB = []
    else:
        plm.EB = miscread(FLAGS.EB).data
        if plm.subjidx is not None:
            plm.EB = plm.EB[plm.subjidx]

        plm.EB = reindex(plm.EB, method="fixleaves")
    """
    Load variance groups
    """
    if FLAGS.singlevg:
        plm.VG = np.ones(plm.N)
    elif FLAGS.VG == "auto":
        if len(plm.EB) == 0:
            plm.VG = np.ones(plm.N)
        else:
            Ptree = tree(plm.EB)
            plm.VG = ptree2vg(Ptree)
    else:
        plm.VG = miscread(FLAGS.vg).data
    if plm.subjidx is not None:
        plm.VG = plm.VG[plm.subjidx]
