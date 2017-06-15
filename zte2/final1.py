import numpy as np
import pdb
from fproblem import problem
from utils import get_testcase
from profilehooks import profile

DEBUG=False

def method5(sheet=2,niter=10000,momentum=0.9):
    '''
    random choice.
    '''
    node_min,node_max,table,p0=get_testcase(sheet)
    problem.init_problem(table,node_min,node_max,p0)
    #cope the index with maximum gradient
    x0=np.zeros(problem.num_path,dtype='int32')
    gradient=0
    for i in xrange(niter):
        if i%100==0:
            cost0=problem.get_cost(x0)
        gradient_i=problem.compute_gradient(x0,problem.num_path)
        gradient=momentum*gradient+gradient_i
        pivot=np.argmax(abs(gradient))
        g=gradient[pivot]
        if np.all(gradient_i==0):
            print 'Find Result!'
            break
        dx=round(8e-4*gradient[pivot])
        if abs(dx)<1:
            dx=1 if g>0 else -1
        x0[pivot]-=dx
        #x0[pivot]-=np.sign(gradient[pivot])
        if i%100==0:
            opt_cost=problem.get_cost(x0)
            print 'i=%s, opt_cost = %s, diff = %s.'%(i,opt_cost,opt_cost-cost0)
            print 'num_bins=',np.sum(abs(x0)>0)

    print 'num_bins=',np.sum(abs(x0)>0)
    problem.fin_problem()
    pdb.set_trace()


if __name__=='__main__':
    method5()
