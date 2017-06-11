from binpacking import binpacking
import time
import pdb
from numpy import *


def get_num_bin(weight,size_bin,assign_table):
    order=argsort(assign_table)
    #bins=zeros([2000] if weight.ndim==1 else [2000,weight.shape[1]])
    #for w,ind in zip(weight,assign_table):
    #    bins[ind]+=w
    #print bins
    #pdb.set_trace()
    if weight.ndim==1:
        return binpacking.nextfit(weight[order],size_bin=size_bin)[0]
    else:
        return binpacking.nextfit1d(weight[order],size_bin=size_bin)[0]

def test_small():
    weight=[2,5,4,7,1,3,8]
    size_bin=10
    print 'First Fit =',binpacking.firstfit(weight=weight, size_bin=size_bin)
    print 'Next Fit =',binpacking.nextfit(weight=weight, size_bin=size_bin)
    print 'First Fit Dec =',binpacking.firstfit(weight=sorted(weight,reverse=True), size_bin=size_bin)
    print 'Best Fit =',binpacking.bestfit(weight=weight, size_bin=size_bin)

def test_small_vec():
    weight=array([[2,3,4],[5,1,3],[4,4,4],[7,1,0],[2,1,1],[3,9,1],[8,0,0]])
    size_bin=[10,10,10]
    print 'First Fit =',binpacking.firstfit1d(weight=weight, size_bin=size_bin)[0]
    w_weight={'Sum':sum(weight,axis=1),'Prod':prod(weight,axis=1)}
    for w_key,w_value in w_weight.iteritems():
        t0=time.time()
        order=argsort(w_value)[::-1]
        weight=weight[order]
        t1=time.time()
        print 'First Fit Dec (%s) num_bin = %s, Elapse = %s.'%(w_key,
                binpacking.firstfit1d(weight=weight, size_bin=size_bin)[0],t1-t0)

def test_big_vec():
    num_item=1000
    dim_vector=5
    weight=random.random([num_item,dim_vector])
    size_bin=ones(5)*3
    print 'First Fit num_bin =',binpacking.firstfit1d(weight=weight, size_bin=size_bin)[0]
    w_weight={'Sum':sum(weight,axis=1),'Prod':prod(weight,axis=1)}
    for w_key,w_value in w_weight.iteritems():
        order=argsort(w_value)[::-1]
        weight_=weight[order]
        t0=time.time()
        nbin,table=binpacking.firstfit1d(weight=weight_, size_bin=size_bin)
        t1=time.time()
        print 'First Fit Dec (%s) num_bin = %s, Elapse = %s.'%(w_key,
                nbin,t1-t0)
        assert(get_num_bin(weight_,size_bin,table)==nbin)
        t0=time.time()
        nbin,table=binpacking.bestfit1d(weight=weight_, size_bin=size_bin)
        t1=time.time()
        assert(get_num_bin(weight_,size_bin,table)==nbin)
        print 'Best Fit Dec (%s) num_bin = %s, Elapse = %s.'%(w_key,
                nbin,t1-t0)
    t0=time.time()
    nbin,table=binpacking.dotproduct(weight=weight_, size_bin=size_bin)
    t1=time.time()
    assert(get_num_bin(weight_,size_bin,table)==nbin)
    print 'Dot Prod num_bin = %s, Elapse = %s.'%(nbin,t1-t0)

def test_big():
    num_item=75
    random.seed(2)
    weight=random.random([num_item])**2
    print weight
    size_bin=1
    method={'First Fit':binpacking.firstfit,
            'Frist Fit Dec':lambda weight,size_bin:binpacking.firstfit(weight=sort(weight)[::-1], size_bin=size_bin),
            'Next Fit':binpacking.nextfit,
            'Best Fit':binpacking.bestfit
            }
    for name,func in method.iteritems():
        t0=time.time()
        res=func(weight=weight, size_bin=size_bin)
        t1=time.time()
        print '%s num_bin = %s, Elapse = %s.'%(name, res[0] if hasattr(res,'__iter__') else res,t1-t0)

def test_sa():
    from bpp_sa import test
    test()

def test_sa_small():
    import bpp_sa
    weight=[2,5,4,7,1,3,8]
    size_bin=10
    bpp_sa.bpp1d.init_problem(weight,size_bin,linspace(10,0.5,50),400)
    #nbin,table=binpacking.dotproduct(weight=weight, size_bin=size_bin)
    nbin,table=binpacking.firstfit(weight=weight, size_bin=size_bin)
    bpp_sa.init_random_seed(2)
    print 'num_bin = %s'%nbin
    opt_config,nbin=bpp_sa.anneal(3,table+1,nbin)
    opt_config=opt_config-1
    print 'num_bin(after optimization) = %s'%nbin

def test_sa_big():
    import bpp_sa
    num_item=1000
    num_vector=3
    random.seed(2)
    weight=random.random([num_item,num_vector])
    size_bin=3*ones(3)
    bpp_sa.bpp1d.init_problem(weight,size_bin,logspace(1,-1,50),10000)
    #nbin,table=binpacking.dotproduct(weight=weight, size_bin=size_bin)
    nbin,table=binpacking.firstfit(weight=weight, size_bin=size_bin)
    bpp_sa.init_random_seed(2)
    print 'num_bin = %s'%nbin
    print sum(weight)/nbin/size_bin
    opt_config,nbin=bpp_sa.anneal(10,table+1,nbin)
    opt_config=opt_config-1
    print 'num_bin(after optimization) = %s'%nbin


#test_small_vec()
#test_big()
#test_small()
#test_big_vec()
#test_sa()
test_sa_big()
