from .permutation_test import PermutationTest


# TODO
class CCAPermutationTest(PermutationTest):
    def __init__(self, estimator, n_permutations=100, n_jobs=None, random_state=0, verbose=0, fit_params=None,
                 exchangeable_errors=True, is_errors=False, ignore_repeat_rows=False, ignore_repeat_perms=False):

        super().__init__(estimator, n_permutations, n_jobs, random_state, verbose, fit_params, exchangeable_errors,
                         is_errors, ignore_repeat_rows, ignore_repeat_perms)

    def score(self):
        self.metrics = {}
        if self.wilks:
            self.metrics['wilks'] = self._wilks()
        if self.lawley_hotelling:
            self.metrics['lawley_hotelling'] = self._lawley_hotelling()
        if self.pillai:
            self.metrics['pillai'] = self._pillai()
        if self.roy_ii:
            self.metrics['roy_ii'] = self._roy_ii()
        if self.roy_iii:
            self.metrics['roy_iii'] = self._roy_iii()


def _wilks():
    # TODO
    pass


def _lawley_hotelling():
    # TODO
    pass


def _pillai():
    # TODO
    pass


def _roy_ii():
    # TODO
    pass


def _roy_iii():
    # TODO
    pass
