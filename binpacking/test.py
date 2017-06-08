import binpacking
from numpy import *

def test_small():
    weight=[2,5,4,7,1,3,8]
    size_bin=10
    print 'First Fit =',binpacking.firstfit(weight=weight, size_bin=size_bin)
    print 'First Fit Dec =',binpacking.firstfit(weight=sorted(weight,reverse=True), size_bin=size_bin)
    print 'Next Fit =',binpacking.nextfit(weight=weight, size_bin=size_bin)
    print 'Best Fit =',binpacking.bestfit(weight=weight, size_bin=size_bin)

def test_small_vec():
    weight=[2,5,4,7,1,3,8]
    size_bin=10
    print 'First Fit =',binpacking.firstfit(weight=weight, size_bin=size_bin)
    print 'First Fit Dec =',binpacking.firstfit(weight=sorted(weight,reverse=True), size_bin=size_bin)
    print 'Next Fit =',binpacking.nextfit(weight=weight, size_bin=size_bin)
    print 'Best Fit =',binpacking.bestfit(weight=weight, size_bin=size_bin)

def test_big():
    weight=random.random()
test_small()
