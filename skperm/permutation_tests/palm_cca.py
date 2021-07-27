import numpy as np
from typing import Tuple
from .permutation_test import _BasePermutationTest


class CCAPermutationTest(_BasePermutationTest):
    def __init__(self, model, scoring=None, cv=None, permuter=None, permutations=100, random_state=0, verbose=0,
                 n_jobs=None, fit_params=None):
        super().__init__(model, scoring, cv, permuter, permutations, random_state, verbose, n_jobs, fit_params)

    def _process(self, wilks=True, lawley_hotelling=True, pillai=True, roy_ii=True, roy_iii=True):
        metrics = {}
        if wilks:
            metrics['wilks'] = self._wilks()
        if lawley_hotelling:
            metrics['lawley_hotelling'] = self._lawley_hotelling()
        if pillai:
            metrics['pillai'] = self._pillai()
        if roy_ii:
            metrics['roy_ii'] = self._roy_ii()
        if roy_iii:
            metrics['roy_iii'] = self._roy_iii()

    def _wilks(self, E, H):
        return np.linalg.det(E) / np.linalg.det(E + H)

    def _lawley_hotelling(self):
        pass

    def _pillai(self):
        pass

    def _roy_ii(self):
        pass

    def _roy_iii(self):
        pass


def _get_correlations(model, X: Tuple[np.ndarray]) -> np.ndarray:
    Z = model.transform(X)
    correlations = np.corr
    return correlations


def cca_perm(model, X: Tuple[np.ndarray], get_correlations=None):
    if get_correlations is None:
        get_correlations = _get_correlations
    model.fit(X)
    correlations = get_correlations()
    wilks_lambda = -np.fliplr(np.cumsum(np.log(1 - correlations ** 2)))
