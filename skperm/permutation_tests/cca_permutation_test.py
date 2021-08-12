from sklearn.utils.metaestimators import _safe_split
from sklearn.utils.validation import _check_fit_params
import numpy as np
from skperm.permutation_tests.permutation_test import PermutationTest


def correlation_scorer(estimator, X_test, y_test):
    zx, zy = estimator.transform(X_test, y_test)
    latent_dims = zx.shape[1]
    corrs = np.diag(np.corrcoef(zx, zy, rowvar=False)[:latent_dims, latent_dims:])
    return corrs


class CCAPermutationTest(PermutationTest):
    def __init__(self, estimator, n_permutations=100, n_jobs=None, random_state=0, verbose=0, fit_params=None,
                 exchangeable_errors=True, is_errors=False, ignore_repeat_rows=False, ignore_repeat_perms=False,
                 wilks=True, lawley_hotelling=True, pillai=True, roy_ii=True, roy_iii=True):
        super().__init__(estimator, n_permutations, n_jobs, random_state, verbose, fit_params, exchangeable_errors,
                         is_errors, ignore_repeat_rows, ignore_repeat_perms, scoring=correlation_scorer)
        self.wilks = wilks
        self.lawley_hotelling = lawley_hotelling
        self.pillai = pillai
        self.roy_ii = roy_ii
        self.roy_iii = roy_iii

    def get_metrics(self, score, permutation_scores):
        self.metrics = {}
        self.metrics['pvalue'] = (np.sum(permutation_scores >= score, axis=0) + 1.0) / (self.n_permutations + 1)
        if self.wilks:
            self.metrics['wilks'] = _wilks(score)
        if self.lawley_hotelling:
            self.metrics['lawley_hotelling'] = _lawley_hotelling(score)
        if self.pillai:
            self.metrics['pillai'] = _pillai(score)
        if self.roy_ii:
            self.metrics['roy_ii'] = _roy_ii(score)
        if self.roy_iii:
            self.metrics['roy_iii'] = _roy_iii()


def _wilks(score):
    return np.cumprod(1-score**2)

def _lawley_hotelling(score):
    return np.sum(score**2/(1-score**2))


def _pillai(score):
    return np.sum(score**2)


def _roy_ii(score):
    return np.max(score)/(1+np.max(score))


def _roy_iii():
    # TODO
    pass


def main():
    import numpy as np
    import pandas as pd
    from sklearn.cross_decomposition import CCA
    EB = pd.read_csv('../tests/data/eb.csv', header=None).values
    X = np.random.rand(EB.shape[0], 50)
    y = np.random.normal(size=(EB.shape[0], 50))
    cca = CCA(n_components=3)
    blah = CCAPermutationTest(cca, n_permutations=10)
    a = blah.score(X, y)
    print()


if __name__ == '__main__':
    main()
