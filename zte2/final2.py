import numpy as np
import pdb
from fproblem import problem
from utils import get_testcase
from profilehooks import profile

DEBUG=False

@profile
def method5(sheet=2,niter=10000,momentum=0.9):
    '''
    random choice.
    '''
    node_min,node_max,table,p0=get_testcase(sheet)
    problem.init_problem(table,node_min,node_max,p0)
    #cope the index with maximum gradient
    gradient=0
    for i in xrange(niter):
        if i%100==0:
            cost0=problem.get_cost()
        gradient_i=problem.compute_gradient(problem.num_path)
        gradient=momentum*gradient+gradient_i
        pivot=np.argmax(abs(gradient))
        g=gradient[pivot]
        if np.all(gradient_i==0):
            print 'Find Result!'
            break
        dx=round(8e-4*gradient[pivot])
        if abs(dx)<1:
            dx=1 if g>0 else -1
        problem.chdp(pivot,-dx)
        #x0[pivot]-=np.sign(gradient[pivot])
        if i%100==0:
            opt_cost=problem.get_cost()
            print 'i=%s, opt_cost = %s, diff = %s.'%(i,opt_cost,opt_cost-cost0)
            print 'num_bins=',np.sum(abs(problem.dp)>0)
    np.savetxt('deletaC.dat',np.array([problem.p0,problem.p0+problem.dp]).T,fmt='%d')
    np.savetxt('deletaNC.dat',np.array([problem.table.dot(problem.p0),problem.table.dot(problem.p0+problem.dp)]).T,fmt='%d')

    print 'num_bins=',np.sum(abs(problem.dp)>0)
    problem.fin_problem()


if __name__=='__main__':
    method5()
