#!/usr/bin/env python

import numpy as np

l1TestSize = 16
l2TestSize = 46
l3TestSize = 106

layerTestSizes = [None, l1TestSize, l2TestSize, l3TestSize]

# this would be faster as an object
class O:
    pass

class LayerCfg:
    def __init__(self):
        self.filt = O()
        self.actv = O()
        self.pool = O()
        self.norm = O()

cfg = [LayerCfg(),LayerCfg(),LayerCfg(),LayerCfg()]

cfg[0].filt.size = 0
cfg[0].filt.number = 1
cfg[0].actv.min = -np.Inf
cfg[0].actv.max = np.Inf
cfg[0].pool.size = 0
cfg[0].pool.order = 0
cfg[0].pool.stride = 0
cfg[0].norm.size = 9
cfg[0].norm.centering = 0
cfg[0].norm.gain = 1.0
cfg[0].norm.threshold = 1.0
# cfg = { 0 : {'filt': {'size': 0, 'number': 1},
#                 'actv': {'min': -np.Inf, 'max': np.Inf},
#                 'pool': {'size': 0, 'order': 0, 'stride': 0},
#                 'norm': {'size': 9, 'centering': 0, 'gain': 1.0, 'threshold': 1.0}},

cfg[1].filt.size = 3
cfg[1].filt.number = 16
cfg[1].actv.min = 0.
cfg[1].actv.max = np.Inf
cfg[1].pool.size = 5
cfg[1].pool.order = 2
cfg[1].pool.stride = 2
cfg[1].norm.size = 9
cfg[1].norm.centering = 0
cfg[1].norm.gain = 0.1
cfg[1].norm.threshold = 10.0
#         1 : {'filt': {'size': 3, 'number': 16},
#                 'actv': {'min': 0., 'max': np.Inf},
#                 'pool': {'size': 5, 'order': 2, 'stride': 2},
#                 'norm': {'size': 9, 'centering': 0, 'gain': 0.1, 'threshold': 10.0}},

cfg[2].filt.size = 3
cfg[2].filt.number = 32
cfg[2].actv.min = 0.
cfg[2].actv.max = np.Inf
cfg[2].pool.size = 5
cfg[2].pool.order = 10
cfg[2].pool.stride = 2
cfg[2].norm.size = 5
cfg[2].norm.centering = 1
cfg[2].norm.gain = 0.1
cfg[2].norm.threshold = 10.0
#         2 : {'filt': {'size': 3, 'number': 32},
#                 'actv': {'min': 0., 'max': np.Inf},
#                 'pool': {'size': 5, 'order': 10, 'stride': 2},
#                 'norm': {'size': 5, 'centering': 1, 'gain': 0.1, 'threshold': 10.0}},

cfg[3].filt.size = 3
cfg[3].filt.number = 128
cfg[3].actv.min = -np.Inf
cfg[3].actv.max = 1.
cfg[3].pool.size = 9
cfg[3].pool.order = 2
cfg[3].pool.stride = 2
cfg[3].norm.size = 3
cfg[3].norm.centering = 0
cfg[3].norm.gain = 0.1
cfg[3].norm.threshold = 1.0
#         3 : {'filt': {'size': 3, 'number': 128},
#                 'actv': {'min': -np.Inf, 'max': 1.},
#                 'pool': {'size': 9, 'order': 2, 'stride': 2},
#                 'norm': {'size': 3, 'centering': 0, 'gain': 0.1, 'threshold': 1.0}}}