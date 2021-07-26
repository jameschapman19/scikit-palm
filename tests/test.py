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
        dec=121
        bin=d2b(dec,5)

