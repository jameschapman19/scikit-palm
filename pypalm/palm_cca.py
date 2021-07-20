from mvlearn.embed import CCA as CCA

from pypalm._base import PermutationTest


class PypalmCCA(PermutationTest):
    def __init__(self, cca_estimator=CCA(), groups=None, cv=None,
                 n_permutations=100, n_jobs=None, random_state=0,
                 verbose=0, fit_params=None, df=0):
        super().__init__(estimator=cca_estimator, groups=groups, cv=cv, n_permutations=n_permutations, n_jobs=n_jobs,
                         random_state=random_state,
                         verbose=verbose, fit_params=fit_params)
        self.df = df




def main():
    import numpy as np
    X = np.random.rand(100, 10)
    Y = np.random.rand(100, 19)
    p = PypalmCCA(n_permutations=5)
    p.permutation_test_score(X, Y)

    print()


if __name__ == "__main__":
    main()
