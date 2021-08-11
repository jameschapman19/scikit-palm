from .permutation_test import PermutationTest


# TODO
class CCAPermutationTest(PermutationTest):
    def __init__(self, estimator, n_permutations=100, n_jobs=None, random_state=0, verbose=0, fit_params=None,
                 exchangeable_errors=True, is_errors=False, ignore_repeat_rows=False, ignore_repeat_perms=False,
                 wilks=True, lawley_hotelling=True, pillai=True, roy_ii=True, roy_iii=True):
        super().__init__(estimator, n_permutations, n_jobs, random_state, verbose, fit_params, exchangeable_errors,
                         is_errors, ignore_repeat_rows, ignore_repeat_perms)
        self.wilks = wilks
        self.lawley_hotelling = lawley_hotelling
        self.pillai = pillai
        self.roy_ii = roy_ii
        self.roy_iii = roy_iii

    def get_metrics(self, score, permutation_scores):
        self.metrics = {}
        if self.wilks:
            self.metrics['wilks'] = _wilks()
        if self.lawley_hotelling:
            self.metrics['lawley_hotelling'] = _lawley_hotelling()
        if self.pillai:
            self.metrics['pillai'] = _pillai()
        if self.roy_ii:
            self.metrics['roy_ii'] = _roy_ii()
        if self.roy_iii:
            self.metrics['roy_iii'] = _roy_iii()


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
