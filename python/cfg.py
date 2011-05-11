#!/usr/bin/env python

import numpy as np

# this would be faster as an object
class O:
    pass

cfg = { 0 : {'filt': {'size': 0, 'number': 1},
                'actv': {'min': -np.Inf, 'max': np.Inf},
                'pool': {'size': 0, 'order': 0, 'stride': 0},
                'norm': {'size': 9, 'centering': 0, 'gain': 1.0, 'threshold': 1.0}},
        1 : {'filt': {'size': 3, 'number': 16},
                'actv': {'min': 0., 'max': np.Inf},
                'pool': {'size': 5, 'order': 2, 'stride': 2},
                'norm': {'size': 9, 'centering': 0, 'gain': 0.1, 'threshold': 10.0}},
        2 : {'filt': {'size': 3, 'number': 32},
                'actv': {'min': 0., 'max': np.Inf},
                'pool': {'size': 5, 'order': 10, 'stride': 2},
                'norm': {'size': 5, 'centering': 1, 'gain': 0.1, 'threshold': 10.0}},
        3 : {'filt': {'size': 3, 'number': 128},
                'actv': {'min': -np.Inf, 'max': 1.},
                'pool': {'size': 9, 'order': 2, 'stride': 2},
                'norm': {'size': 3, 'centering': 0, 'gain': 0.1, 'threshold': 1.0}}}