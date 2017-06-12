import time
import pdb
from numpy import *
from bpp_sa import binpacking

random.seed(2)

def get_num_bin(weight,size_bin,assign_table):
    weight=asarray(weight)
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

def get_filling(weight,assign_table,num_bin):
    if ndim(weight)==1:
        filling=zeros(num_bin)
    else:
        filling=zeros([num_bin,weight.shape[1]])
    for w,ibin in zip(weight,assign_table):
        filling[ibin]+=w
    return filling

def test_small():
    weight=[2,5,4,7,1,3,8]
    size_bin=10
    print 'Next Fit =',binpacking.nextfit(weight=weight, size_bin=size_bin)
    res=binpacking.firstfit(weight=weight, size_bin=size_bin)
    print 'First Fit =',res
    assert(get_num_bin(weight,size_bin,res[1])==res[0])
    res=binpacking.bestfit(weight=weight, size_bin=size_bin)
    print 'Best Fit =',res
    assert(get_num_bin(weight,size_bin,res[1])==res[0])
    res=binpacking.firstfit(weight=sorted(weight,reverse=True), size_bin=size_bin)
    print 'First Fit Dec =',res
    assert(get_num_bin(sorted(weight,reverse=True),size_bin,res[1])==res[0])

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
    print 'overflow =', min(size_bin-get_filling(weight_,res[1],res[0]))

def test_big():
    num_item=50000
    random.seed(2)
    weight=random.random([num_item])
    size_bin=2
    method=[('First Fit',binpacking.firstfit),
            ('First Fit Bin',binpacking.firstfit_bt),
            ('Next Fit',binpacking.nextfit),
            ('Best Fit',binpacking.bestfit),
            ('First Fit Bin Dec',binpacking.firstfit_bt),
            ('Frist Fit Dec',binpacking.firstfit),
            ]
    for name,func in method:
        if name[-3:]=='Dec':
            weight_=sort(weight)[::-1]
        else:
            weight_=weight
        t0=time.time()
        res=func(weight=weight_, size_bin=size_bin)
        t1=time.time()
        print '%-20s num_bin = %s, Elapse = %s.'%(name, res[0] if hasattr(res,'__iter__') else res,t1-t0)
        if hasattr(res,'__iter__'):
            assert(min(size_bin-get_filling(weight_,res[1],res[0]))>-1e-6)

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
    weight=random.random([num_item])
    size_bin=3
    bpp_sa.bpp1d.init_problem(weight,size_bin,linspace(30,0.5,100),40000)
    nbin,table=binpacking.dotproduct(weight=weight, size_bin=size_bin)
    #nbin,table=binpacking.firstfit(weight=weight, size_bin=size_bin)
    bpp_sa.init_random_seed(2)
    print 'num_bin = %s'%nbin
    print sum(weight)/nbin/size_bin
    pdb.set_trace()
    opt_config,nbin=bpp_sa.anneal(3,table+1,nbin)
    opt_config=opt_config-1
    print 'num_bin(after optimization) = %s'%nbin


#test_small_vec()
test_big()
#test_small()
#test_big_vec()
#test_sa()
#test_sa_big()
