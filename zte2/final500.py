import numpy as np
import pdb,time
from fproblem import problem
from utils import get_testcase
#from profilehooks import profile
from optimizer import RMSProp,DefaultOpt

DEBUG=False

#@profile
def help_ant(sheet=2,num_iter=10000,momentum=0.9,learning_rate=0.79e-3):
    '''
    A method to help ants sheduling routes.

    Parameters:
        :sheet: int, specify the sheet number.

            * 0 -> run functionality test case with 9 nodes.
            * 1 -> run the bad case with 500 nodes.
            * 2 -> run performace test case with 1000 nodes.
        
        :num_iter: int, maximum number of iteration.
        :momentum: float, a number in 0-1.
        :learning_rate: float, learning rate.
    '''
    t0=time.time()
    #load and initialize problem
    node_min,node_max,table,p0=get_testcase(sheet)
    problem.init_problem(table,node_min,node_max,p0)

    #using optimizer with momentum=0.9
    optimizer=DefaultOpt(rate=learning_rate,momentum=momentum)

    t1=time.time()
    min_num_overflow=problem.get_num_overflow()
    for i in xrange(num_iter):
        #compute the gradient
        gradient_i=problem.compute_gradient(problem.num_path)
        if all(gradient_i==0):
            print 'Find Result!'
            break
        #modify the gradient accoding to optimizer
        gradient=optimizer(gradient_i)

        #choose the principle axis to change.
        ind_pivot=np.argmax(abs(gradient))
        g=gradient[ind_pivot]
        dx=round(g)
        if abs(dx)<1:
            dx=1 if g>0 else -1
        problem.chdp(ind_pivot,dx)
        
        #display information
        num_overflow=problem.get_num_overflow()
        min_num_overflow=min(num_overflow,min_num_overflow)
        if i%100==0:
            print 'i=%s, minimum number of overflow = %s.'%(i,min_num_overflow)
            print 'num_bins=',np.sum(abs(problem.dp)>0)

    t2=time.time()
    #save data to files
    np.savetxt('deletaC_%s.dat'%sheet,np.array([problem.p0,problem.p0+problem.dp]).T,fmt='%d')
    np.savetxt('deletaNC_%s.dat'%sheet,np.array([problem.table.dot(problem.p0),problem.table.dot(problem.p0+problem.dp)]).T,fmt='%d')
    t3=time.time()

    print 'num_bins=',np.sum(abs(problem.dp)>0)
    print 'time elapse: main block: %s, save & load %s.'%(t2-t1,t1-t0+t3-t2)

if __name__=='__main__':
    #run functionality test case with 9 nodes.
    #help_ant(0)

    #run the bad case with 500 nodes.
    help_ant(1,learning_rate=1e-3,num_iter=100000)

    #run performace test case with 1000 nodes.
    #help_ant(2)
