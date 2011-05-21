#!/usr/bin/env python

import os, sys, time

import numpy as np

import matplotlib
if sys.platform == 'linux2': # for headless plot generation
    matplotlib.use('Cairo')

import pylab as pl
# import scipy.optimize
import scipy.misc
from PIL import Image

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

global vs
vs = []

def eval_func(x, grad):
    if grad.size > 0:
        print grad, grad.size
    # print np.mean(x), np.max(x), np.min(x)
    v = float(np.squeeze(n.run(x.reshape((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])),channel,layer)))
    # print v
    global vs
    vs.append(v)
    return v

print "Entering test repetition loop"
times = []
for I in xrange(NReps):
    print "Test: %i" % I 
    # ====== Setup
    ND = cfg.layerTestSizes[layer]*cfg.layerTestSizes[layer]
    x0 = np.random.rand(ND)
    
    # global opts require bounds
    # GN_MLSL GN_MLSL_LDS
    # try: LN_COBYLA LN_BOBYQA LN_NEWUOA [and _BOUND]
    # LN_PRAXIS : slow, stopped
    # LN_NELDERMEAD : slow, stopped
    # LN_SBPLX : fast, bad result: 0.8-1.0
    # GN_ISRES : slow, stopped
    # GN_MLSL : 
    algorithm = nlopt.GN_ISRES
    opt = nlopt.opt(algorithm, ND)
    opt.set_max_objective(eval_func)
    opt.set_lower_bounds(np.ones(ND) * -1000000)
    opt.set_upper_bounds(np.ones(ND) * 1000000)
    opt.set_maxeval(100000)
    opt.set_ftol_rel(0.001)
    opt.set_xtol_rel(0.1)
    opt.set_maxtime(240)
    
    # ======

    startTime = time.time()
    # =================== -> optimize (eval_func, x0)
    
    xOpt = opt.optimize(x0)
    
    # ===================
    endTime = time.time()
    
    maxResp = opt.last_optimum_value()
    nIter = 0 
    
    print "  N: %i V: %.3f Time: %.3f" % (nIter, maxResp, endTime-startTime)
    #im = Image.fromarray(xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer]))
    #im.resize((300,300))
    #fn = '%s/resized.png' % outDir
    #print "  Saving %s" % fn
    #im.save(fn)
    #imA = np.array(im)
    imA = xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
    imA = scipy.misc.imresize(imA,(300,300),interp='nearest')
    pl.imsave('%s/nlopt_%i_%.3f_%i.png' % (outDir, I, maxResp, nIter), imA, cmap=pl.cm.gray)
    times.append(endTime-startTime)
    
    pl.plot(vs)
    pl.savefig('%s/nlopt_%i_%.3f_prog.png' % (outDir, I, maxResp))
    pl.close()
    vs = []

if len(times) > 1:
    print "Timing info"
    print " Mean: %f" % np.mean(times)
    print " Max : %f" % np.max(times)
    print " Min : %f" % np.min(times)
    print " Std : %f" % np.std(times)
