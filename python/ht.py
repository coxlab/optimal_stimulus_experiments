#!/usr/bin/env python

import logging, stopwatch, sys

import numpy as np
from scipy.ndimage import convolve
from scipy.signal import convolve2d
from scipy.io import loadmat

import cfg

# dimensions should be as follows:
#  2d:  x   y  (correspond to x and y like inputs)
#  3d:  c   x   y (correspond to filter channel and x and y like inputs)
#  4d:  
# convolution flips the buffer:
#   a1 a2 a3... an
#   b1 b2 b3
#   c1 = a1 * b3 + a2 * b2 + a3 * b1

def valid_bounds(n):
    """
    if len(b) = 3:
        c = convolve(a,b)[1:-1]
    if len(c) = 4:
        c = convolve(a,b)[1:-2]
    if lne(c) = 5:
        c = convolve(a,b)[2:-2]
    
    so...
    
    3 -> 1, -1
    4 -> 1, -2
    5 -> 2, -2
    """
    if n == 1:
        return 0, 1
    d, m = divmod(n-1,2)
    return d, -(d+m)

# def valid_1d_convolve(a, b):
#     l, r = valid_bounds(b.shape[0])
#     return convolve(a,b)[l:-r]
# 
# def valid_2d_convolve(a, b):
#     l0, r0 = valid_bounds(b.shape[0])
#     l1, r1 = valid_bounds(b.shape[1])
#     return convolve(a,b)[l0:-r0,l1:-r1]
# 
# def valid_3d_convolve(a, b):
#     l0, r0 = valid_bounds(b.shape[0])
#     l1, r1 = valid_bounds(b.shape[1])
#     l2, r2 = valid_bounds(b.shape[2])
#     return convolve(a,b)[l0:-r0,l1:-r1,l2:-r2]
# 
# def valid_4d_convolve(a, b):
#     l0, r0 = valid_bounds(b.shape[0])
#     l1, r1 = valid_bounds(b.shape[1])
#     l2, r2 = valid_bounds(b.shape[2])
#     l3, r3 = valid_bounds(b.shape[3])
#     return convolve(a,b)[l0:-r0,l1:-r1,l2:-r2,l3:-r3]
# 
# def valid_convolve(a,b):
#     return [None, valid_1d_convolve, valid_2d_convolve, valid_3d_convolve, valid_4d_convolve][len(b.shape)](a,b)

def pad(x,n):
    y = np.zeros((n,n))
    d = (n - x.shape[0])/2
    y[d:x.shape[0] + d,d:x.shape[0] + d] = x
    return y

def full_to_valid_bounds(n):
    """
    2 -> 1, :
    
    3 -> 1, -1
    4 -> 1, -2
    5 -> 2, -2
    """
    if n == 1:
        return 0, None
    if n == 2:
        return 1, None
    
    d, m = divmod(n-1,2)
    return d, -(d+m)

def fft_to_valid_bounds(a,b):
    """
    106, 9 -> 8,-8
    106, 8 -> 7,-7
    105, 9 -> 8,-8
    105, 8 -> 7,-7
    """
    lfv, rfv = full_to_valid_bounds(b.shape[0])
    l = b.shape[0] + lfv
    r = -b.shape[0] - rfv
    # l = b.shape[0] / 2
    # r = l + (b.shape[0] % 2)
    return l, -r

def convolve_fft(a,b):
    n = a.shape[0] + b.shape[0]
    apad = pad(a,n)
    bpad = pad(b,n)
    z = np.fft.ifftn(np.fft.fftn(apad) * np.fft.fftn(bpad))
    # print a.shape, b.shape, z.shape, fft_to_valid_bounds(a,b)
    return z[[slice(*fft_to_valid_bounds(a,b)) for n in b.shape]]

def valid_2_2_convolve(a,b):
    return convolve2d(a,b,'valid')
    # return convolve_fft(a,b)

def valid_3_2_convolve(a,b):
    o = a[[slice(None)]+[slice(*valid_bounds(n)) for n in b.shape]]
    for i in xrange(a.shape[0]):
        o[i] = valid_2_2_convolve(a[-i],b)
    return o

def valid_3_3_convolve(a,b):
    o = a[[slice(None)]+[slice(*valid_bounds(n)) for n in b.shape[1:]]]
    for i in xrange(a.shape[0]):
        o[i] = valid_2_2_convolve(a[-i],b[i])
    return sum(o,0)[np.newaxis,:,:]

def valid_convolve_signal(a,b):
    if a.ndim == 2:
        return valid_2_2_convolve(a,b)
    if b.ndim == 2:
        return valid_3_2_convolve(a,b)
    return valid_3_3_convolve(a,b)

def valid_convolve_ndimage(a,b):
    """
    If b.ndim < a.ndim will convolve(a[i],b) for i in a.shape[0]
    # cases:
    # a.ndim = 3, b.ndim = 2
    # a.ndim = 3, b.ndim = 3
    # a.ndim = 2, b.ndim = 2
    """
    # if a.ndim != b.ndim:
    #     print "Diff:", a.ndim, b.ndim
    # else:
    #     print "Same:", a.ndim
    if a.ndim > b.ndim: # corner case for lower-dimensional kernels
        o = a[[slice(None)]+[slice(*valid_bounds(n)) for n in b.shape]]
        for i in xrange(a.shape[0]):
            o[i] = valid_convolve(a[-i],b)
        return o
    return convolve(a,b)[[slice(*valid_bounds(n)) for n in b.shape]]

# def valid_convolve_fft(a,b):
#     if a.ndim > b.ndim: # corner case for lower-dimensional kernels
#         o = a[[slice(None)]+[slice(*valid_bounds(n)) for n in b.shape]]
#         for i in xrange(a.shape[0]):
#             o[i] = valid_convolve(a[-i],b)
#         return o
#     return np.fft.ifftn(np.fft.fftn(a) * np.fft.fftn(b))[[slice(*valid_bounds(n)) for n in b.shape]]
    
valid_convolve = valid_convolve_signal # ~.405 per run (with signal), ~1.636 per run (with fft)
# valid_convolve = valid_convolve_ndimage # ~.646 per run
# valid_convolve = valid_convolve_fft # does not work

class Layer(object):
    def __init__(self, cfg, nInFilters):
        """
        cfg : dictionary of layer settings
        nInFilters : number of filters in previous later
        """
        self.cfg = cfg
        self.nInFilters = nInFilters
        self.make_filters()
    
    def make_filters(self):
        """
        filters should always have ndim == 3
        """
        self.randomize_filters()
    
    def randomize_filters(self):
        if self.cfg.filt.size != 0:
            self.filters = np.random.rand(self.cfg.filt.number,
                                            self.nInFilters,
                                            self.cfg.filt.size,
                                            self.cfg.filt.size)
    
    def filt(self, inArr, channel=None):
        if self.cfg.filt.size == 0:
            return inArr
        if channel is not None:
            #print inArr.shape, self.filters[channel].shape
            # print "In filt[1] 0 ",; t = stopwatch.Timer()
            # v = valid_convolve(inArr, self.filters[channel])
            # t.stop(); print t.elapsed
            # return v
            return valid_convolve(inArr, self.filters[channel])
        fSize = inArr.shape[1] - self.cfg.filt.size + 1
        o = np.zeros((self.cfg.filt.number, fSize, fSize), dtype=np.float64)
        # print "In filt[2] 0 ",; t = stopwatch.Timer()
        for i in xrange(len(self.filters)):
            # print fSize, inArr.shape, self.filters[i].shape
            o[i,:,:] = valid_convolve(inArr, self.filters[i])
        # t.stop(); print t.elapsed
        return o
        
    
    def actv(self, inArr):
        return np.clip(inArr, self.cfg.actv.min, self.cfg.actv.max)
    
    def pool(self, inArr):
        if self.cfg.pool.size == 0:
            return inArr
        # .^ = power of
        # pool = convn(actv .^ network{l}.pool.order, ones(network{l}.pool.size), 'valid') .^ (1 / network{l}.pool.order);
        # pool = pool(1:network{l}.pool.stride:end, 1:network{l}.pool.stride:end, :);
        # print inArr.shape
        # this line should only compress x and y
        # print "In pool 1 ",; t = stopwatch.Timer()
        pool = valid_convolve(inArr ** self.cfg.pool.order, np.ones((self.cfg.pool.size,self.cfg.pool.size))) ** (1. / self.cfg.pool.order)
        # t.stop(); print t.elapsed
        # next line should compress x and y based on stride
        return pool[:,::self.cfg.pool.stride,::self.cfg.pool.stride]
    
    def norm(self, inArr):
        # print "In norm[1] 2 ",; t = stopwatch.Timer()
        pSum = valid_convolve(inArr.copy(), np.squeeze(np.ones((self.cfg.filt.number,
                                            self.cfg.norm.size,
                                            self.cfg.norm.size))))
        # t.stop(); print t.elapsed
        # print "In norm[2] 2 ",; t = stopwatch.Timer()
        pSSum = valid_convolve(inArr.copy() ** 2., np.squeeze(np.ones((self.cfg.filt.number,
                                                    self.cfg.norm.size,
                                                    self.cfg.norm.size))))
        # t.stop(); print t.elapsed
        pMean = pSum / ((self.cfg.norm.size ** 2.) * self.cfg.filt.number)
        
        #posMin = (self.cfg['norm']['size'] + 1) / 2.
        # posMin, posMax = valid_bounds(self.cfg['norm']['size'])
        posSlice = slice(*valid_bounds(self.cfg.norm.size))
        # posMin = self.cfg['norm']['size'] / 2.
        # posMax = posMin + inArr.shape[0] - self.cfg['norm']['size']
        
        if self.cfg.norm.centering == 1:
            c = inArr[:, posSlice, posSlice] - np.tile(pMean, (self.cfg.filt.number, 1, 1))
            cNorm = pSSum - (pSum ** 2.) / ((self.cfg.norm.size ** 2.) * self.cfg.filt.number)
            cNorm = cNorm ** 0.5
        else:
            # print inArr.shape
            c = inArr[:, posSlice, posSlice]
            cNorm = pSSum ** 0.5
        
        # cNorm = cNorm / self.cfg['norm']['gain']
        cNorm = np.clip(cNorm, 1./self.cfg.norm.gain,np.Inf)
        # print c.shape, cNorm.shape
        if cNorm.ndim < 3:
            cNorm = np.reshape(cNorm, (cNorm.shape[0], cNorm.shape[1], 1))
        if c.ndim < 3:
            c = np.reshape(c, (c.shape[0], c.shape[1], 1))
        return c / np.tile(cNorm, (self.cfg.filt.number,1,1))
    
    def run(self, inArr, channel=None):
        if channel is None:
            return self.norm(self.pool(self.actv(self.filt(inArr))))
        else:
            return self.pool(self.actv(self.filt(inArr, channel)))

class Network(object):
    """
    High-throughput L3 network
    """
    def __init__(self, cfg, matFile=None):
        """
        cfg : dictionary of layer settings
        """
        if matFile is not None:
            self.load_mat_file(matFile)
        else:
            self.cfg = cfg
            self.layers = []
            self.make_layers()
    
    def load_mat_file(self, matFile):
        d = loadmat(matFile)
        # format
        # d['network'][0][<layer>][0][0].<filt/norm/pool/actv>[0][0].<number/size/weights...>[0][0]
        # construct cfg from mat file
        self.cfg = [cfg.LayerCfg(),cfg.LayerCfg(),cfg.LayerCfg(),cfg.LayerCfg()]
        self.layers = []
        for l in xrange(4):
            # self.cfg[l] = {}
            # self.cfg[l]['filt'] = {}
            self.cfg[l].filt.size = d['network'][0][l][0][0].filt[0][0].size[0][0]
            self.cfg[l].filt.number = d['network'][0][l][0][0].filt[0][0].number[0][0]
            # self.cfg[l]['actv'] = {}
            self.cfg[l].actv.min = float(d['network'][0][l][0][0].actv[0][0].min[0][0])
            self.cfg[l].actv.max = float(d['network'][0][l][0][0].actv[0][0].max[0][0])
            # self.cfg[l]['pool'] = {}
            self.cfg[l].pool.size = d['network'][0][l][0][0].pool[0][0].size[0][0]
            self.cfg[l].pool.order = d['network'][0][l][0][0].pool[0][0].order[0][0]
            self.cfg[l].pool.stride = d['network'][0][l][0][0].pool[0][0].stride[0][0]
            # self.cfg[l]['norm'] = {}
            self.cfg[l].norm.size = d['network'][0][l][0][0].norm[0][0].size[0][0]
            self.cfg[l].norm.centering = d['network'][0][l][0][0].norm[0][0].centering[0][0]
            self.cfg[l].norm.gain = float(d['network'][0][l][0][0].norm[0][0].gain[0][0])
            self.cfg[l].norm.threshold = float(d['network'][0][l][0][0].norm[0][0].threshold[0][0])
            
            # load weights 
            if l != 0:
                lay = Layer(self.cfg[l],self.cfg[l-1].filt.number) # make with random weights??
                for (i,f) in enumerate(d['network'][0][l][0][0].filt[0][0].weights[0]):
                    if lay.filters[i].shape == f.shape:
                        lay.filters[i] = f
                    elif lay.filters[i].ndim == f.ndim:
                        #print l, np.squeeze(lay.filters[i]).shape, f.shape
                        for i2 in xrange(lay.filters[i].shape[0]):
                            lay.filters[i][i2] = f[:,:,i2]
                    else:
                        lay.filters[i,0,:,:] = f[:,:]
            else:
                lay = Layer(self.cfg[l],0)
            self.layers.append(lay)
    
    def make_layers(self):
        prevNFilters = 1
        self.layers = []
        for i in xrange(len(self.cfg)):
            self.layers.append(Layer(self.cfg[i],prevNFilters))
            prevNFilters = self.cfg[i].filt.number
    
    def run(self, inArr, channel, lMax):
        """
        lMax : maximum layer to run, this determines the size of the input
        """
        for l in xrange(lMax+1):
            # logging.debug("Running layer: %i" % l)
            # print "Running layer: %i" % l
            # logging.debug(" inArr pre run :")
            # logging.debug("  shape: %s" % repr(inArr.shape))
            # logging.debug("  value: %s" % repr(inArr))
            if lMax == l:
                inArr = self.layers[l].run(inArr,channel)
            else:
                inArr = self.layers[l].run(inArr)
            # logging.debug(" inArr post run: ")
            # logging.debug("  shape: %s" % repr(inArr.shape))
            # logging.debug("  value: %s" % repr(inArr))
        return inArr
        # -- Layer 0 --
        # Filt: set layer 0 filt to inArr
        # Actv: set layer 0 actv to filt
        # Pool: set layer 0 pool to actv
        # Norm: norm layer 0 pool -> norm
        
        # set norm to input for layer 1
        pass

def compare_to_matlab():
    """
    Passed on May 10, 2011
    """
    #logging.basicConfig(level=logging.DEBUG)
    import cfg
    n = Network(cfg.cfg)
    n.load_mat_file('../network.mat')
    a = np.zeros((1,16,16),dtype=np.float64)
    a[0,7,7] = 1.
    m = np.array([-0.7322,-0.5745,-0.7997,-0.6940,-0.7109,-0.6838,-0.5781,-0.6618,-0.7465,-0.7095,-0.7336,-0.7262,-0.7089,-0.7516,-0.8137,-0.7619])
    vs = np.array([np.squeeze(-n.run(a,i,1)) for i in xrange(16)])
    print "Results"
    print " python : ", vs
    print " matlab : ", m
    print " diff   : ", vs - m
    print " sse    : ", np.sum((vs-m)**2)

def run_l3_n(N=1000):
    #logging.basicConfig(level=logging.DEBUG)
    import cfg
    n = Network(cfg.cfg)
    n.load_mat_file('../network.mat')
    a = np.zeros((1,106,106),dtype=np.float64)
    a[0,7,7] - 1.
    print "Running %i times..." % N
    import time
    st = time.time()
    for i in xrange(N):
        r = -n.run(a,0,3)
    et = time.time()
    print " dt: ", et-st
    print " dt/N: ", (et-st)/N

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        compare_to_matlab()
    else:
        N = 100
        try:
            N = int(sys.argv[1])
        except:
            pass
        run_l3_n(N)
