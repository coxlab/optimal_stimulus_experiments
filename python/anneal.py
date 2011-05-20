#!/usr/bin/env python

import os, sys

import numpy as np

import matplotlib
if sys.platform == 'linux2': # for headless plot generation
    matplotlib.use('Cairo')

import pylab as pl
import scipy.optimize

from ht import Network
import cfg

channel = 15
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

outDir = '%s/%i/%i' % ('anneal', layer, channel)
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
global tick
tick = 0
def eval_func(x, *args):
    global tick
    tick += 1
    # print np.mean(x), np.max(x), np.min(x)
    v = 100-float(np.squeeze(n.run(x.reshape((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])),channel,layer)))
    # print v
    return v

print "Entering test repetition loop"
for I in xrange(NReps):
    print "Test: %i" % I 
    x0 = np.random.rand(1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
    # xOpt, maxResp, nIter, funcCalls, warnFlags = scipy.optimize.fmin(eval_func, x0, maxiter=1000000, full_output=1)
    # from source of anneal: return best_state.x, best_state.cost, schedule.T, schedule.feval, iters, schedule.accepted, retval
    xOpt, maxResp, T, fEval, nIter, accepts, cond = scipy.optimize.anneal(eval_func, x0, maxiter=10000, full_output=1)
    maxResp = 100 - maxResp
    print "  N: %i V: %.3f" % (nIter, maxResp)
    print tick
    pl.imsave('%s/anneal_%i_%.3f_%i.png' % (outDir, I, maxResp, nIter), xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer]), cmap=pl.cm.gray)