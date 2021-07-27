from unittest import TestCase
import numpy as np
from skperm.utils.binary import d2b, incrbin
from skperm.utils.reindex import reindex


class Test(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_binary(self):
        bin_dim = 5
        dec = [25, 26]
        dec_plus_one = [e + 1 for e in dec]
        bin = d2b(dec, bin_dim)
        bin_plus_one = incrbin(bin)
        assert (bin.shape[1] == 5), 'maximum dimensionality of binary representation not equal to {bin_dim}'
        assert np.array_equal(bin_plus_one, d2b(dec_plus_one, bin_dim))

    def test_reindex(self):
        import pandas as pd
        EB = pd.read_csv('../tests/data/eb.csv', header=None).values
        EB_c = pd.read_csv('../tests/data/eb_c.csv', header=None).values
        EB_r = pd.read_csv('../tests/data/eb_r.csv', header=None).values
        EB_m = pd.read_csv('../tests/data/eb_m.csv', header=None).values
        EB_fl = pd.read_csv('../tests/data/eb_fl.csv', header=None).values

        eb_fl = reindex(EB)
        eb_r = reindex(EB, method='restart')
        eb_c = reindex(EB, method='continuous')
        eb_m = reindex(EB, method='mixed')

        np.testing.assert_array_almost_equal(EB_fl, eb_fl)
        np.testing.assert_array_almost_equal(EB_r, eb_r)
        np.testing.assert_array_almost_equal(EB_c, eb_c)
        np.testing.assert_array_almost_equal(EB_m, eb_m)
