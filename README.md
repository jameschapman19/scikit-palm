[![DOI](https://zenodo.org/badge/303801602.svg)](https://zenodo.org/badge/latestdoi/303801602)
[![Python package](https://github.com/jameschapman19/scikit-perm/actions/workflows/python-package.yml/badge.svg)](https://github.com/jameschapman19/scikit-perm/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/jameschapman19/pypalm/branch/main/graph/badge.svg?token=DUTZX5ZO2L)](https://codecov.io/gh/jameschapman19/pypalm)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jameschapman19/pypalm/badges/quality-score.png?b=main&s=7539a6d0e88e9e24aa80d99830afc7d3486b2165)](https://scrutinizer-ci.com/g/jameschapman19/pypalm/?branch=main)
# scikit-perm
Implementing the PALM — Permutation Analysis of Linear Models toolbox (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/PALM) for
Python. PALM a

## Objectives
The goal is to have a flexible framework for statistically valid permutation testing when using linear models from
https://github.com/scikit-learn/scikit-learn or otherwise. 

The framework should also be adaptable to multiview models such as those in https://github.com/mvlearn/mvlearn

Project is open to contributions. 

I am currently aware of some related repos e.g. https://github.com/danlurie/PyPALM https://github.com/statlab/permute 
but neither appear to contain the functionality for multi-level exchangeability block permuation.

- [ ] quickperms
    - [x] quickperms function and helpers
    - [ ] unit testing for quickperms
- [ ] scikit-learn wrappers
    - [ ] regression/classification
        - [ ] adapt permutation_test_score() using permutations based on quickperms for multiblock exchangeability
    - [ ] canonical correlation analysis
        - [ ] wilks
        - [ ] lawley_hotelling
        - [ ] pillai
        - [ ] roy-ii
        - [ ] roy-iii

## References
 - Winkler AM, Ridgway GR, Webster MA, Smith SM, Nichols TE. Permutation inference for the general linear model. NeuroImage, 2014;92:381-397 (Open Access)
 - Alberton BAV, Nichols TE, Gamba HR, Winkler AM. Multiple testing correction over contrasts for brain imaging. Neuroimage. 2020 Mar 19:116760. (Open Access)
 - Winkler AM, Webster MA, Brooks JC, Tracey I, Smith SM, Nichols TE. Non-Parametric Combination and related permutation tests for neuroimaging. Hum Brain Mapp. 2016 Apr;37(4):1486-511. (Open Access)
 - Winkler AM, Webster MA, Vidaurre D, Nichols TE, Smith SM. Multi-level block permutation. Neuroimage. 2015;123:253-68. (Open Access)
 - Winkler AM, Ridgway GR, Douaud G, Nichols TE, Smith SM. Faster permutation inference in brain imaging. Neuroimage. 2016 Jun 7;141:502-516. (Open Access)
 - Nichols TE, Holmes AP. Nonparametric permutation tests for functional neuroimaging: a primer with examples. Hum Brain Mapp. 2002 Jan;15(1):1-25.
 - Holmes AP, Blair RC, Watson JD, Ford I. Nonparametric analysis of statistic images from functional mapping experiments. J Cereb Blood Flow Metab. 1996 Jan;16(1):7-22.