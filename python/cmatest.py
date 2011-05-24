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

import cma

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

outDir = '%s/%i/%i' % ('cma', layer, channel)
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

def eval_func(x):
    # print np.mean(x), np.max(x), np.min(x)
    v = -float(np.squeeze(n.run(x.reshape((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])),channel,layer)))
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
    sigma0 = 1.
    # ======

    startTime = time.time()
    # =================== -> optimize (eval_func, x0)
    
    xOpt, maxResp, nIter, outDict = cma.fmin(eval_func, x0, sigma0, maxiter=ND*100, verb_log=0)
    
    # ===================
    endTime = time.time()
    
    maxResp = -maxResp
    print "  N: %i V: %.3f Time: %.3f" % (nIter, maxResp, endTime-startTime)
    #im = Image.fromarray(xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer]))
    #im.resize((300,300))
    #fn = '%s/resized.png' % outDir
    #print "  Saving %s" % fn
    #im.save(fn)
    #imA = np.array(im)
    imA = xOpt.reshape(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
    imA = scipy.misc.imresize(imA,(300,300),interp='nearest')
    pl.imsave('%s/cma_%i_%.3f_%i.png' % (outDir, I, maxResp, nIter), imA, cmap=pl.cm.gray)
    times.append(endTime-startTime)
    
    pl.plot(vs)
    pl.savefig('%s/cma_%i_%.3f_prog.png' % (outDir, I, maxResp))
    pl.close()
    # cma.plotdata()
    # cma.show()
    vs = []

if len(times) > 1:
    print "Timing info"
    print " Mean: %f" % np.mean(times)
    print " Max : %f" % np.max(times)
    print " Min : %f" % np.min(times)
    print " Std : %f" % np.std(times)
