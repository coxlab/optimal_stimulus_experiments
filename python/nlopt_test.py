#!/usr/bin/env python

import os, sys, time

import numpy as np

import matplotlib
if sys.platform == 'linux2': # for headless plot generation
    matplotlib.use('Cairo')

import pylab as pl
# import scipy.optimize
import nlopt

from ht import Network
import cfg

channel = 0
layer = 1
NReps = 1

if len(sys.argv) > 1:
    channel = int(sys.argv[1])
if len(sys.argv) > 2:
    layer = int(sys.argv[2])
if len(sys.argv) > 3:
    N = int(sys.argv[3])
if len(sys.argv) > 4:
    NReps = int(sys.argv[4])

outDir = '%s/%i/%i' % ('nlopt', layer, channel)
try:
    os.makedirs(outDir)
except OSError:
    pass

print "Creating network"
n = Network(cfg.cfg)
print "Loading mat file"
n.load_mat_file('../network.mat')

# v = float(np.squeeze(n.run(x0.reshape((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])),channel,layer)))

# print v

def eval_func(x, grad):
    # print np.mean(x), np.max(x), np.min(x)
    v = float(np.squeeze(n.run(x.reshape((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])),channel,layer)))
    # print v
    return v

print "Entering test repetition loop"
times = []
for I in xrange(NReps):
    print "Test: %i" % I 
    # ====== Setup
    x0 = np.random.rand(1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
    
    # don't work: GN_MLSL GN_MLSL_LDS
    # try: LN_COBYLA LN_BOBYQA LN_NEWUOA [and _BOUND] LN_PRAXIS LN_NELDERMEAD LN_SBPLX
    algorithm = nlopt.LN_SBPLX
    opt = nlopt.opt(algorithm, cfg.layerTestSizes[layer] * cfg.layerTestSizes[layer])
    opt.set_max_objective(eval_func)
    #opt.set_lower_bounds(np.ones((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])) * 0)
    #opt.set_lower_bounds(np.ones((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])) * 1)
    
    # ======

    startTime = time.time()
    # =================== -> optimize (eval_func, x0)
    
    xopt = opt.optimize(x0)
    
    # ===================
    endTime = time.time()
    
    maxResp = opt.last_optimum_value()
    
    
    print "  N: %i V: %.3f Time: %.3f" % (nIter, maxResp, endTime-startTime)
    pl.imsave('%s/nlopt_%i_%.3f_%i.png' % (outDir, I, maxResp, nIter), xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer]), cmap=pl.cm.gray)
    times.append(endTime-startTime)

if len(times) > 1:
    print "Timing info"
    print " Mean: %f" % np.mean(times)
    print " Max : %f" % np.max(times)
    print " Min : %f" % np.min(times)
    print " Std : %f" % np.std(times)
