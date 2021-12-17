from absl import flags, app

from skpalm.core import core
from skpalm.takeargs import takeargs
import time

FLAGS = flags.FLAGS
flags.DEFINE_bool("twotail", False, help="")
flags.DEFINE_bool("concordant", False, help="")
flags.DEFINE_bool("reversemasks", False, help="")

flags.DEFINE_multi_string(
    "i",
    None,
    help="Input(s). More than one can be specified, each one preceded by its own -i. All input files must contain the same number of observations (e.g., the same number of subjects). Except for NPC and MV, mixing is allowed (e.g., voxelwise, vertexwise and non-imaging data can be all loaded at once, and later will be all corrected across).",
)
flags.mark_flag_as_required("i")
flags.DEFINE_multi_string(
    "m",
    None,
    help="Mask(s). Either one for all inputs, or one per input supplied in the same order as the respective -i appear.",
)
flags.DEFINE_multi_string(
    "s",
    None,
    help="Surface file(s). When more than one is supplied, each -s should be entered in the same order as the respective -i. This option is needed when the input data is a scalar field over a surface and cluster extent or TFCE have been enabled. The first argument is the surface file itself. The second is an optional area-per-vertex or area-per-face file, or simply a number. If only the surface file is provided, its area is calculated and used for the computation of spatial statistics (cluster extent and TFCE). If the second argument is given, it should contain the areas, which are then used (e.g., average areas from native geometry after areal interpolation). Alternatively, if the areas are not meaningful for cluster extent or TFCE, this argument can be simply a number, such as 1, which is then used as the area of all vertices or faces.",
)
flags.DEFINE_multi_string(
    "d",
    None,
    help="Design matrix. It can be in csv format, or in fsl's vest format. For information on how to construct the design matrix, see the FSL GLM manual.",
)
flags.DEFINE_multi_string(
    "t",
    None,
    help="t-contrasts file, in csv or vest format (the format used by FSL). The option -t can be used more than once, so that more than one t-contrasts file can be loaded.",
)
flags.DEFINE_multi_string(
    "f",
    None,
    help="F-contrasts file, in csv or vest format. The option -f can be used more than once, so that more than one F-contrasts file can be loaded. Each file supplied with a -f corresponds to the file supplied with the option -t immediately before. The option -f cannot be used more than the number of times the option -t is used.",
)
flags.DEFINE_integer(
    "n",
    10000,
    help="Number of permutations. Use -n 0 to run all permutations and/or sign-flips exhaustively. Default is 10000.",
)
flags.DEFINE_string(
    "eb",
    None,
    help="Exchangeability blocks file, in csv or vest format. If omitted, all observations are treated as exchangeable and belonging to a single large exchangeability block.",
)
flags.DEFINE_bool(
    "within",
    False,
    help="If the file supplied with -eb has a single column, this option runs within-block permutation (default). Can be used with '-whole'.",
)
flags.DEFINE_bool(
    "whole",
    False,
    help="If the file supplied with -eb has a single column, this option runs whole-block permutation. Can be used with '-within'.",
)
flags.DEFINE_bool(
    "ee",
    False,
    help="Assume exchangeable errors (EE), to allow permutations (more details below).",
)
flags.DEFINE_bool(
    "ise",
    False,
    help="Assume independent and symmetric errors (ISE), to allow sign-flipping (more details below).",
)
flags.DEFINE_string(
    "vg",
    None,
    help="Variance groups file, in csv or vest format. If omitted, all observations are assumed to belong to the same variance group (i.e. the data is treated as homoscedastic. Use '-vg auto' to define the automatically using a structure that is compatible with the exchangeability blocks (option -eb).",
)
flags.DEFINE_string(
    "npcmethod",
    "fisher",
    help="Do a modified non-parametric combination (NPC), using the the specified method (combining function), which can be one of: Tippett, Fisher, Stouffer, Wilkinson <alpha>, Winer, Edgington, Mudholkar-George, Friston <u>, Darlington-Hayes <r>, Zaykin <alpha>, Dudbridge-Koeleman <r>, Dudbridge-Koeleman2 <r> <alpha>, Taylor-Tibshirani or Jiang <alpha>. Default is Fisher. Note that some methods require 1 or 2 additional parameters to be provided. All methods except Darlington-Hayes and Jiang can also be used to produce parametric p-values (under certain assumptions) and spatial statistics.",
)
flags.DEFINE_bool("npcmod", False, help="Enable NPC over modalities.")
flags.DEFINE_bool("npccon", False, help="Enable NPC over contrasts.")
flags.DEFINE_bool(
    "mv",
    False,
    help="Do classical multivariate analysis (MV), such as MANOVA and MANCOVA, using the the specified statistic, which can be one of: Wilks, HotellingTsq, Lawley, Pillai, Roy_ii, Roy_iii. All but Roy_iii can be used with spatial statistics.",
)
flags.DEFINE_bool(
    "pearson",
    False,
    help="Instead of t, F, v or G, compute the Pearson's correlation coefficient, r (if the constrast has rank=1), or the coefficient of determination, R2 (if the constrast has rank>1). For the contrasts in which some EVs are zeroed out, this option computes the multiple correlation coefficient (or R2) corresponding to the EVs of interest.",
)
flags.DEFINE_bool(
    "T",
    False,
    help="Enable TFCE inference for univariate (partial) tests, as well as for NPC and/or MV if these options have been enabled.",
)
flags.DEFINE_float(
    "C",
    None,
    help="Enable cluster inference for univariate (partial) tests, with the supplied cluster-forming threshold (supplied as the equivalent z-score), as well as for NPC and/or MV if these options have been enabled.",
)
flags.DEFINE_string(
    "Cstat",
    "extent",
    help="Choose which cluster statistic should be used. Accepted statistics are extent and mass.",
)
# TODO tfce1d, tfce2d
flags.DEFINE_bool(
    "corrmod", False, help="Apply FWER-correction of p-values over multiple modalities."
)
flags.DEFINE_bool(
    "corrcon", False, help="Apply FWER-correction of p-values over multiple contrasts."
)
flags.DEFINE_bool("fdr", False, help="Produce FDR-adjusted p-values.")
flags.DEFINE_string(
    "o",
    "palm",
    help="Output prefix. It may itself be prefixed by a path. Default is palm.",
)
flags.DEFINE_bool(
    "logp",
    True,
    help="Save the output p-values as -log10(p) (or -log10(1-p) if the option -save1-p is also used; using both together is not recommended). The -logp is not default but it is strongly recommended.",
)
flags.DEFINE_bool(
    "demean",
    True,
    help="Mean center the data, as well as all columns of the design matrix. If the original design had an intercept, the intercept is removed.",
)
flags.DEFINE_bool(
    "twotail",
    False,
    help="Run two-tailed tests for all the t-contrasts instead of one-tailed. If NPC is used, it also becomes two-tailed for the methods which statistic are symmetric around zero under the null.",
)
flags.DEFINE_bool(
    "concordant",
    False,
    help="For the NPC, favour alternative hypotheses with concordant signs. Cannot be used with -twotail.",
)
# TODO accel
flags.DEFINE_list(
    "accel",
    None,
    help="Run one of various acceleration methods (negbin, tail, noperm, gamma, lowrank)",
)
flags.DEFINE_bool(
    "reversemasks",
    True,
    help="Reverse 0/1 in the masks, so that the zero values are then used to select the voxels/vertices/faces.",
)
flags.DEFINE_bool(
    "quiet", False, help="Don't show progress as the shufflings are performed."
)


def main(argv):
    ticI = time.time()
    plm = takeargs()
    tocI = time.time() - ticI
    core()


if __name__ == "__main__":
    app.run(main)
