import numpy as np
import pdb,time
from fproblem import problem
from utils import get_testcase
#from profilehooks import profile

from optimizer import RMSProp,DefaultOpt

DEBUG=False
np.random.seed(2)

#@profile
def help_ant(sheet,num_iter=50000,momentum=0.9,learning_rate=0.79e-3,max_path=None):
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
    if max_path is None:
        max_path=problem.num_path
    t1=time.time()

    #using optimizer with momentum=0.9
    optimizer=DefaultOpt(rate=learning_rate,momentum=momentum)

    _fix_path=False
    for i in xrange(num_iter):
        if i%100==0:
            cost0=problem.get_cost()

        #compute the gradient
        gradient_i=problem.compute_gradient(problem.num_path)
        if all(gradient_i==0):
            print 'Find Result!'
            break
        #modify the gradient accoding to optimizer
        gradient=optimizer(gradient_i)

        #choose the principle axis to change.
        if _fix_path or np.count_nonzero(problem)>=max_path:
            _fix_path=True
            allowed_indices=np.where(problem.dp)[0]
            ind_pivot=allowed_indices[np.argmax(abs(gradient[allowed_indices]))]
        else:
            ind_pivot=np.argmax(abs(gradient))
        g=gradient[ind_pivot]
        dx=round(g)
        if abs(dx)<1:
            dx=1 if g>0 else -1
        problem.chdp(ind_pivot,dx)
        
        #display information
        if i%100==0:
            opt_cost=problem.get_cost()
            print 'i=%s, opt_cost = %s, diff = %s.'%(i,opt_cost,opt_cost-cost0)
            print 'num_path=',np.sum(abs(problem.dp)>0)

    t2=time.time()
    num_path=np.sum(abs(problem.dp)>0)
    #save data to files
    np.savetxt('deletaC_%s.%s.dat'%(sheet,num_path),np.array([problem.p0,problem.p0+problem.dp]).T,fmt='%d')
    np.savetxt('deletaNC_%s.%s.dat'%(sheet,num_path),np.array([problem.table.dot(problem.p0),problem.table.dot(problem.p0+problem.dp)]).T,fmt='%d')
    t3=time.time()

    print 'number of path changed = %s'%num_path
    print 'time elapse: main block: %s, save & load %s.'%(t2-t1,t1-t0+t3-t2)

def surviving_game(sheet,num_iter=50000,momentum=0.9,learning_rate=0.79e-3,max_path=None,die_rate=0.01):
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
    if max_path is None:
        max_path=problem.num_path
    t1=time.time()

    #using optimizer with momentum=0.9
    optimizer=DefaultOpt(rate=learning_rate,momentum=momentum)

    for i in xrange(num_iter):
        if i%100==0:
            cost0=problem.get_cost()

        #compute the gradient
        gradient_i=problem.compute_gradient(problem.num_path)
        if all(gradient_i==0):
            print 'Find Result!'
            break
        #modify the gradient accoding to optimizer
        gradient=optimizer(gradient_i)

        #choose the principle axis to change.
        if np.random.random()<die_rate:
            #choose one to die!
            allowed_indices=np.where(problem.dp)[0]
            ind_die=allowed_indices[np.argmax(gradient_i[allowed_indices]/problem.dp[allowed_indices])]
            problem.dp[ind_die]=0
        if np.count_nonzero(problem.dp)>=max_path:
            allowed_indices=np.where(problem.dp)[0]
            ind_pivot=allowed_indices[np.argmax(abs(gradient[allowed_indices]))]
        else:
            ind_pivot=np.argmax(abs(gradient))
        g=gradient[ind_pivot]
        dx=round(g)
        if abs(dx)<1:
            dx=1 if g>0 else -1
        problem.chdp(ind_pivot,dx)
        
        #display information
        if i%100==0:
            opt_cost=problem.get_cost()
            print 'i=%s, opt_cost = %s, diff = %s.'%(i,opt_cost,opt_cost-cost0)
            print 'num_path=',np.sum(abs(problem.dp)>0)

    t2=time.time()
    num_path=np.sum(abs(problem.dp)>0)
    #save data to files
    np.savetxt('deletaC_%s.%s.dat'%(sheet,num_path),np.array([problem.p0,problem.p0+problem.dp]).T,fmt='%d')
    np.savetxt('deletaNC_%s.%s.dat'%(sheet,num_path),np.array([problem.table.dot(problem.p0),problem.table.dot(problem.p0+problem.dp)]).T,fmt='%d')
    t3=time.time()

    print 'number of path changed = %s'%num_path
    print 'time elapse: main block: %s, save & load %s.'%(t2-t1,t1-t0+t3-t2)


def test_perturbation(sheet,num_path,num_iter=50000,momentum=0.9,learning_rate=0.79e-3,max_path=None):
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

    #load existing result
    popt=np.loadtxt('deletaC_%s.%s.dat'%(sheet,num_path),dtype='int32')[:,1]

    problem.init_problem(table,node_min,node_max,popt)
    if max_path is None:
        max_path=problem.num_path
    print 'Initial cost = %s'%problem.get_cost()

    #apply perturbation
    num_perturb=5
    offset=-10
    positions=np.random.randint(0,problem.num_node,num_perturb)
    problem.node_min+=offset
    problem.node_max+=offset
    print 'After perturbation, the cost = %s'%problem.get_cost()
    t1=time.time()

    #using optimizer with momentum=0.9
    optimizer=DefaultOpt(rate=learning_rate,momentum=momentum)

    _fix_path=False
    for i in xrange(num_iter):
        if i%100==0:
            cost0=problem.get_cost()

        #compute the gradient
        gradient_i=problem.compute_gradient(problem.num_path)
        if all(gradient_i==0):
            print 'Find Result!'
            break
        #modify the gradient accoding to optimizer
        gradient=optimizer(gradient_i)

        #choose the principle axis to change.
        if _fix_path or np.count_nonzero(problem.dp)>=max_path:
            _fix_path=True
            allowed_indices=np.where(problem.dp)[0]
            ind_pivot=allowed_indices[np.argmax(abs(gradient[allowed_indices]))]
        else:
            ind_pivot=np.argmax(abs(gradient))
        g=gradient[ind_pivot]
        dx=round(g)
        if abs(dx)<1:
            dx=1 if g>0 else -1
        problem.chdp(ind_pivot,dx)
        
        #display information
        if i%100==0:
            opt_cost=problem.get_cost()
            print 'i=%s, opt_cost = %s, diff = %s.'%(i,opt_cost,opt_cost-cost0)
            print 'num_path=',np.sum(abs(problem.dp)>0)

    t2=time.time()
    num_path=np.sum(abs(problem.dp)>0)
    #save data to files
    np.savetxt('deletaC_%s.%s.dat'%(sheet,num_path),np.array([problem.p0,problem.p0+problem.dp]).T,fmt='%d')
    np.savetxt('deletaNC_%s.%s.dat'%(sheet,num_path),np.array([problem.table.dot(problem.p0),problem.table.dot(problem.p0+problem.dp)]).T,fmt='%d')
    t3=time.time()

    print 'Using %s steps, number of path changed = %s'%(i+1,num_path)
    print 'time elapse: main block: %s, save & load %s.'%(t2-t1,t1-t0+t3-t2)
    problem.fin_problem() #deallocate arrays



if __name__=='__main__':
    #run functionality test case with 9 nodes.
    #help_ant(0)

    #run the bad case with 500 nodes.
    #help_ant(1,learning_rate=1e-3,num_iter=100000)

    #run performace test case with 1000 nodes.
    #help_ant(2,max_path=422,learning_rate=0.8e-3,momentum=0.95)
    surviving_game(2,max_path=400,learning_rate=0.8e-3,momentum=0.9,die_rate=0.01)

    #run a perturbation test for case with 1000 nodes.
    #test_perturbation(2,num_path=420,max_path=None,learning_rate=0.8e-3,momentum=0.95)
