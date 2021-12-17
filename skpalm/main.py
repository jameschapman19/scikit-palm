from absl import flags, app

from skpalm.core import core
from skpalm.takeargs import takeargs
import time

FLAGS = flags.FLAGS
flags.DEFINE_bool("twotail", False, help="")
flags.DEFINE_bool("concordant", False, help="")
flags.DEFINE_bool("reversemasks", False, help="")

flags.DEFINE_multi_string("i", None, help="")
flags.mark_flag_as_required("i")
flags.DEFINE_multi_string("m", None, help="")
flags.DEFINE_multi_string("s", None, help="")
flags.DEFINE_multi_string("d", None, help="")
flags.DEFINE_multi_string("t", None, help="")
flags.DEFINE_multi_string("f", None, help="")
flags.DEFINE_integer("n", 10000, help="")
flags.DEFINE_string("eb", None, help="")
flags.DEFINE_bool("within", False, help="")
flags.DEFINE_bool("whole", False, help="")
flags.DEFINE_bool("ee", False, help="")
flags.DEFINE_bool("ise", False, help="")
flags.DEFINE_string("vg", "", help="")
flags.DEFINE_string("npcmethod", "fisher", help="")
flags.DEFINE_bool("npcmod", False, help="")
flags.DEFINE_bool("npccon", False, help="")
flags.DEFINE_bool("mv", False, help="")
flags.DEFINE_bool("pearson", False, help="")
flags.DEFINE_bool("T", False, help="")
flags.DEFINE_float("C", None, help="")
flags.DEFINE_string("Cstat", "extent", help="")
# TODO tfce1d, tfce2d
flags.DEFINE_bool("corrmod", False, help="")
flags.DEFINE_bool("corrcon", False, help="")
flags.DEFINE_bool("fdr", False, help="")
flags.DEFINE_string("o", "palm", help="")
flags.DEFINE_bool("logp", True, help="")
flags.DEFINE_bool("demean", True, help="")
flags.DEFINE_bool("twotail", False, help="")
flags.DEFINE_bool("concordant", False, help="")
# TODO accel
flags.DEFINE_list("accel", None, help="")
flags.DEFINE_bool("reversemasks", True, help="")
flags.DEFINE_bool("quiet", False, help="")


def main(argv):
    ticI = time.time()
    plm = takeargs()
    tocI = time.time() - ticI
    core()


if __name__ == "__main__":
    app.run(main)
