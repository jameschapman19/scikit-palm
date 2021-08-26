import numpy as np
from joblib import Parallel
from sklearn.base import is_classifier, clone
from sklearn.metrics import check_scoring
from sklearn.model_selection._split import check_cv
from sklearn.utils import indexable, check_random_state
from sklearn.utils.fixes import delayed
from sklearn.utils.metaestimators import _safe_split
from sklearn.utils.validation import _check_fit_params
from sklearn.utils.validation import check_array
from tqdm import tqdm

from skperm.permutations.quickperms import quickperms


class PermutationTest:
    def __init__(self, estimator,
                 n_permutations=100, n_jobs=None, random_state=0,
                 verbose=0, fit_params=None, exchangeable_errors=True,
                 is_errors=False, ignore_repeat_rows=False, ignore_repeat_perms=False, scoring=None):
        """
        Evaluate the significance of a cross-validated score with permutations
        Permutes targets to generate 'randomized data' and compute the empirical
        p-value against the null hypothesis that features and targets are
        independent.
        The p-value represents the fraction of randomized data sets where the
        estimator performed as well or better than in the original data. A small
        p-value suggests that there is a real dependency between features and
        targets which has been used by the estimator to give good predictions.
        A large p-value may be due to lack of real dependency between features
        and targets or the estimator was not able to use the dependency to
        give good predictions.

        Parameters
        ----------
        estimator
        n_permutations :
            number of permutations
        n_jobs :
            number of processors to use (permutations are computed in parallel)
        random_state :
            random seed for reproducibility
        verbose :
            whether to print progress
        fit_params :
            parameters used to fit estimator
        exchangeable_errors :
            True/False indicating whether to assume exchangeable errors,
            which allow permutations.
        is_errors :
            True/False indicating whether to assume independent and
            symmetric errors, which allow sign-flippings.
        ignore_repeat_rows :
            True/False indicating whether repeated rows in the design
            should be be ignored. Default is false.
        ignore_repeat_perms :
            True/False indicating whether repeated permutations should
            be ignored. Default is false.
        scoring
        """
        self.estimator = estimator
        self.random_state = check_random_state(random_state)
        self.fit_params = fit_params
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.n_permutations = n_permutations
        self.exchangeable_errors = exchangeable_errors
        self.is_errors = is_errors
        self.ignore_repeat_rows = ignore_repeat_rows
        self.ignore_repeat_perms = ignore_repeat_perms
        self.scoring = scoring

    def run(self, X, y, *, exchangeability_blocks=None, groups=None, cv=None):
        X = check_array(X)
        X, y, groups = indexable(X, y, groups)

        cv = check_cv(cv, y, classifier=is_classifier(self.estimator))
        scorer = check_scoring(self.estimator, scoring=self.scoring)

        #+1 as 1st permutation from quickperms is unpermuted
        permutations = quickperms(y[:, None], exchangeability_blocks=exchangeability_blocks,
                                  perms=self.n_permutations+1, exchangeable_errors=self.exchangeable_errors,
                                  is_errors=self.is_errors, ignore_repeat_rows=self.ignore_repeat_rows,
                                  ignore_repeat_perms=self.ignore_repeat_perms)[0]

        # We clone the estimator to make sure that all the folds are
        # independent, and that it is pickle-able.
        score = PermutationTest._permutation_test_score(clone(self.estimator), X, y, groups, cv, scorer,
                                                        fit_params=self.fit_params)
        permutation_scores = Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(
            delayed(self._permutation_test_score)(
                clone(self.estimator), X,
                np.diag(np.sign(permutations[:, 0])) @ y[np.abs(permutations[:, p]) - 1],
                groups, cv, scorer, fit_params=self.fit_params)
            for p in range(1,self.n_permutations+1))
        permutation_scores = np.array(permutation_scores)
        self.get_metrics(score, permutation_scores)
        return score, permutation_scores, self.metrics

    def get_metrics(self, score, permutation_scores):
        self.metrics = {}
        self.metrics['pvalue'] = (np.sum(permutation_scores >= score) + 1.0) / (self.n_permutations + 1)

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
        return np.mean(avg_score, axis=0)
