#!/usr/bin/env python

import os, sys

import numpy as np

import matplotlib
if sys.platform == 'linux2': # for headless plot generation
    matplotlib.use('Cairo')

import pylab as pl

from pyevolve import G2DList, GSimpleGA, Selectors, Crossovers, Mutators, DBAdapters

from ht import Network
import cfg

channel = 15
layer = 1
NGen = 1000000
NPop = 32

if len(sys.argv) > 1:
    channel = int(sys.argv[1])
if len(sys.argv) > 2:
    layer = int(sys.argv[2])
if len(sys.argv) > 3:
    N = int(sys.argv[3])

outDir = '%s/%i/%i' % ('revcorr', layer, channel)
try:
    os.makedirs(outDir)
except OSError:
    pass

n = Network(cfg.cfg)
n.load_mat_file('../network.mat')

def eval_func(chromosome):
    i = np.array(chromosome.genomeList)[np.newaxis,:,:]
    return float(np.squeeze(n.run(i,channel,layer)))

genome = G2DList.G2DList(cfg.layerTestSizes[layer],cfg.layerTestSizes[layer])
genome.setParams(rangemin=0,rangemax=1,gauss_mu=0,gauss_sigma=1)

genome.evaluator.set(eval_func)
genome.crossover.set(Crossovers.G2DListCrossoverUniform)
genome.mutator.set(Mutators.G2DListMutatorRealGaussian)

ga = GSimpleGA.GSimpleGA(genome)
# ga.selector.set(Selectors.GRouletteWheel)
ga.setPopulationSize(NPop)
ga.setGenerations(NGen)

csvfile_adapter = DBAdapters.DBFileCSV(filename="%i_%i.csv" % (layer, channel), frequency=NGen/10)
ga.setDBAdapter(csvfile_adapter)
# sqlite_adapter = DBAdapters.DBSQLite(identify="%i_%i" % (layer, channel),frequency=NGen/10)
# ga.setDBAdapter(sqlite_adapter)

ga.evolve(freq_stats=NGen/10)

bi = ga.bestIndividual()
pl.imsave('%s/ga_%i.png' % (outDir, NGen), np.array(bi.genomeList), cmap=pl.cm.gray)