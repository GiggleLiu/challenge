'''trying to solve M*v=b'''

from numpy import *
from numpy.testing import dec,assert_,assert_raises,assert_almost_equal,assert_allclose
from matplotlib.pyplot import *
from scipy.linalg import inv,norm
import sys,pdb,time
from os import path

from climin import RmsProp,Rprop,GradientDescent,Adadelta,Adam,Lbfgs,Bfgs,Sbfgs,NonlinearConjugateGradient
from optimizer import *

random.seed(2)

class LinEq(object):
    def __init__(self,M,b):
        self.M=M
        self.b=b

    def compute_gradient(self,v):
        M,b=self.M,self.b
        return M.T.conj().dot((M.dot(v)-b))

    def compute_cost(self,v):
        M,b=self.M,self.b
        return norm(M.dot(v)-b)**2

def random_lineq(N):
    M=random.random([N,N])+1j*random.random([N,N])
    M=(M+M.T.conj())/N
    b=random.random(N)+1j*random.random(N)
    return LinEq(M,b)

def test_all():
    N=10
    niter=1000
    prob=random_lineq(N)
    v0=random.random(N)+1j*random.random(N)
    v_true=inv(prob.M).dot(prob.b)

    rms=RmsProp(wrt=v0.copy(),fprime=prob.compute_gradient,step_rate=1e-2)
    gd=GradientDescent(wrt=v0.copy(),fprime=prob.compute_gradient,step_rate=2)
    adadelta=Adadelta(wrt=v0.copy(),fprime=prob.compute_gradient,step_rate=0.5)
    adam=Adam(wrt=v0.copy(),fprime=prob.compute_gradient,step_rate=5e-2)
    rprop=Rprop(wrt=v0.copy(),fprime=prob.compute_gradient)
    bfgs=Bfgs(wrt=v0.copy(),f=prob.compute_cost,fprime=prob.compute_gradient)
    ncg=NonlinearConjugateGradient(wrt=v0.copy(),f=prob.compute_cost,fprime=prob.compute_gradient)

    print 'initial error = ',prob.compute_cost(rms.wrt)
    opts=[rms,gd,adadelta,adam,rprop,bfgs,ncg]
    ion()
    for opt in opts:
        el=[]
        for i in xrange(niter):
            info=opt.minimize_until(lambda x:rms.n_iter>i)
            cost=prob.compute_cost(opt.wrt)
            el.append(cost)
        plot(el)
    legends=['%s(%s)'%(opt.__class__.__name__,opt.step_rate if hasattr(opt,'step_rate') else '') for opt in opts]
    default=DefaultOpt(rate=2)
    myrms=RMSProp(rho=0.9,rate=1e-2)
    opts=[myrms,default]
    for opt in opts:
        print 'Optimizing using %s'%opt
        err=[]
        v=v0.copy()
        for i in xrange(niter):
            distance=prob.compute_cost(v)
            g=prob.compute_gradient(v)
            dv=opt(distance,g,i)
            v+=dv
            #print 'Iter %s, Error = %s'%(i,distance)
            err.append(distance)
        plot(err)
        print 'Iter %s, Error = %s'%(i,distance)
    legends+=['%s(%s)'%(opt.__class__.__name__,opt.rate) for opt in opts]
    legend(legends)
    pdb.set_trace()
    pdb.set_trace()

if __name__=='__main__':
    test_all()
