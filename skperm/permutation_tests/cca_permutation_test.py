from sklearn.utils.metaestimators import _safe_split
from sklearn.utils.validation import _check_fit_params
import numpy as np
from permutation_test import PermutationTest

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

    @staticmethod
    def _permutation_test_score(estimator, X, y, groups, cv, scorer,
                                fit_params):
        """Auxiliary function for permutation_test_score"""
        # Adjust length of sample weights
        fit_params = fit_params if fit_params is not None else {}
        avg_score = []
        for train, test in cv.split(X, y, groups):
            X_train, y_train = _safe_split(estimator, X, y, train)
            X_test, y_test = _safe_split(estimator, X, y, test, train)
            fit_params = _check_fit_params(X, fit_params, train)
            estimator.fit(X_train, y_train, **fit_params)
            avg_score.append(scorer(estimator, X_test, y_test))
        return np.mean(avg_score)


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


def main():
    import numpy as np
    import pandas as pd
    from sklearn.cross_decomposition import CCA
    EB = pd.read_csv('../tests/data/eb.csv', header=None).values
    X = np.random.rand(EB.shape[0], 5)
    y = np.random.normal(size=(EB.shape[0], 5))
    cca = CCA(n_components=3)
    blah = PermutationTest(cca)
    a = blah.score(X, y)
    print()


if __name__ == '__main__':
    main()
