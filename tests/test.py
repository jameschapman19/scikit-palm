from unittest import TestCase
import numpy as np
from pypalm.d2b import d2b
from pypalm.incrbin import incrbin


class Test(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_binary(self):
        bin_dim=5
        dec=[25,26]
        dec_plus_one=[e+1 for e in dec]
        bin=d2b(dec,bin_dim)
        bin_plus_one=incrbin(bin)
        assert(bin.shape[1]==5,'maximum dimensionality of binary representation not equal to {bin_dim}')
        assert np.array_equal(bin_plus_one,d2b(dec_plus_one,bin_dim))

