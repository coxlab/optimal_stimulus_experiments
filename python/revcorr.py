#!/usr/bin/env python

import os, sys

import numpy as np

import matplotlib
matplotlib.use('Cairo')   # generate postscript output by default

import pylab as pl

from ht import Network
import cfg

channel = 15
layer = 1
N = 100000

if sys.argv > 1:
    channel = int(sys.argv[1])
if sys.argv > 2:
    layer = int(sys.argv[2])
if sys.argv > 3:
    N = int(sys.argv[3])

outDir = '%s/%i/%i' % ('revcorr', layer, channel)
try:
    os.makedirs(outDir)
except OSError:
    pass

n = Network(cfg.cfg)
n.load_mat_file('../network.mat')

# i = np.random.randn(1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
# print n.run(i,channel,layer)
# cv = float(np.squeeze(n.run(i,channel,layer)))
# ab = i[:] * cv
# av = cv
cvs = []
# cvs.append(cv)
testVals = []
ab = np.zeros((1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer]), dtype=np.float64)

testInterval = N / 100
plotInterval = N / 10

for t in xrange(N):
    i = np.random.randn(1,cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
    cv = float(np.squeeze(n.run(i,channel,layer)))
    # av += cv
    # r = cv / av
    ab += i[:] * cv #/ N #ab * (1-r) + i * r
    cvs.append(float(cv))
    if (not t % testInterval):
        testVals.append(float(np.squeeze(n.run(ab[:],channel,layer))))
    if t and (not (t % plotInterval)):
        pl.figure()
        pl.imshow(ab[0])
        pl.title("t = %i" % t)
        pl.colorbar()
        pl.savefig('%s/stim_%i.png' % (outDir, t))
        pl.close()
        
        pl.figure()
        pl.plot(testVals)
        pl.savefig('%s/progress_%i.png' % (outDir, t))
        pl.close()
        # pl.show()
        
        pl.imsave('%s/optimal_%i.png' % (outDir, t), ab[0], cmap=pl.cm.gray)

pl.figure()
pl.imshow(ab[0])
pl.title("t = %i" % t)
pl.colorbar()
pl.savefig('%s/stim_%i.png' % (outDir, t))
pl.close()

pl.figure()
pl.plot(testVals)
pl.savefig('%s/progress_%i.png' % (outDir, t))
pl.close()

pl.imsave('%s/optimal_%i.png' % (outDir, t), ab[0], cmap=pl.cm.gray)
