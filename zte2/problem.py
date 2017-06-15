import numpy as np
from numpy.linalg import pinv
import pdb,xlrd
#from climin import RmsProp,GradientDescent
from scipy.optimize import fmin_cg

class BinPath(object):
    '''
    The Bin Path problem, ZTE challenge, second round.

    Attributes:
        :node_min: 1darray, minimum capacity increment of node.
        :node_max: 1darray, maximum capacity increment of node.
        :table: 2darray, maximum capacity increment of node.
    '''
    def __init__(self, node_min, node_max, table, p0):
        self.node_min=np.asarray(node_min)
        self.node_max=np.asarray(node_max)
        self.p0=np.asarray(p0)

        #table
        self.table=table
        self._center=(self.node_max+self.node_min)/2.
        self._interval=(self.node_max-self.node_min)/2.

    @property
    def num_node(self):
        '''Number of nodes'''
        return len(self.node_min)

    @property
    def num_path(self):
        '''Number of paths'''
        return self.table.shape[1]

    def get_occ(self, path_weights):
        '''
        Get the weight distribution matrix over nodes and paths.

        Parameters:
            :path_weights: 1darray, weight for each path.
        '''
        return self.table.dot(path_weights+self.p0)

    def compute_gradient(self,x,xmask=None,mask_y=True):
        '''Compute the gradient.'''
        p=np.zeros(self.num_path)
        if xmask is not None:
            p[xmask]=x
        occ=self.get_occ(p)-self._center
        if mask_y:
            #mask y version
            #occ[abs(occ)<=self._interval]=0
            occ[abs(occ)<=self._interval]=0
            mask_pos=occ>self._interval
            mask_neg=occ<-self._interval
            occ[mask_pos]-=self._interval[mask_pos]
            occ[mask_neg]+=self._interval[mask_neg]
        if xmask is None:
            grad=self.table.T.dot(occ)
        else:
            grad=self.table.T[xmask].dot(occ)
        return grad

    def compute_cost(self,x,xmask=None):
        '''Compute the cost function.'''
        if xmask is not None:
            p=np.zeros(self.num_path)
            p[xmask]=x
        else:
            p=x
        overflow=abs(self.get_occ(p)-self._center)
        #the part out of bound
        overmask=overflow>self._interval
        return np.linalg.norm(overflow[overmask]-self._interval[overmask])**2
        #return np.linalg.norm(overflow[overmask])**2

    def optimize(self,xmask,x0,niter=100):
        #rms=RmsProp(wrt=x0,fprime=lambda x:self.compute_gradient(x,xmask),step_rate=1e-1)
        rms=GradientDescent(wrt=x0,fprime=lambda x:self.compute_gradient(x,xmask),step_rate=0.1)
        el=[]
        for i in xrange(niter):
            info=rms.minimize_until(lambda x:rms.n_iter>i)
            cost=self.compute_cost(rms.wrt,xmask)
            el.append(cost)
        pdb.set_trace()
        return cost,x0

    def optimize(self,xmask,x0):
        res=fmin_cg(f=self.compute_cost,fprime=self.compute_gradient,args=(xmask,),gtol=0.01,maxiter=10000,x0=x0,full_output=True)
        return res[1],res[0]

    def check_result(self,x):
        '''Check the correctness of result.'''
        occ=self.table.dot(self.p0+x)
        if all(occ>=self.node_min-0.5) and all(occ<=self.node_max+0.5):
            print 'Pass'
            return True
        else:
            print 'Not Pass'
            return False

def get_testcase(which=0):
    if which==1:
        return _load_test_data(which)
    elif which==2:
        maxmin=np.loadtxt('maxmin1000.dat')
        p0=np.loadtxt('p01000.dat')
        table=np.loadtxt('table1000.dat')
        testcase=BinPath(node_min=maxmin[:,0],node_max=maxmin[:,1],table=table,p0=p0)
        return testcase
    node_min=[10,5,-5,15,5,5,-5,-5,-5]
    node_max=[20,20,10,25,20,20,20,10,15]
    route_table=[[0,4,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [2,4,6],
            [0,1,2],
            [3,4,5],
            [6,7,8]]
    p0=[5,6,15,5,-15,8,4,-10]

    table=np.zeros([len(node_min),len(route_table)],dtype='float64')
    for i in xrange(len(route_table)):
        table[route_table[i],i]=1
    testcase=BinPath(node_min,node_max,table,p0=p0)
    return testcase

def _load_test_data(sheet=1):
    wb = xlrd.open_workbook("data2.xlsx")
    ws = wb.sheet_by_index(sheet)
    #pl=np.array([cell.value for cell in ws.row(1)[3:]])
    minmax=[cell.value.strip('[]').split(',') for cell in ws.col(1)[2:]]
    minval=np.array([int(val[0]) for val in minmax],dtype='int32')
    maxval=np.array([int(val[1]) for val in minmax],dtype='int32')
    data=np.array([[1 if col.value else 0 for col in ws.row(irow)[3:]] for irow in xrange(2,ws.nrows)],dtype='float64')
    data_val=np.array([[col.value if col.value else 0 for col in ws.row(irow)[3:]] for irow in xrange(2,ws.nrows)],dtype='int32')
    max_row=np.argmax(abs(data_val),axis=0)
    pl=data_val[max_row,np.arange(data_val.shape[1])]
    return BinPath(node_min=minval,node_max=maxval,table=data,p0=pl)


def method3():
    '''
    max gradient method.
    '''
    case=get_testcase()
    xmask=[]
    x0=np.zeros(case.num_path)
    #cope the index with maximum gradient
    for ix in xrange(case.num_path):
        dx=case.compute_gradient(x0)
        dx[xmask]=0
        xmask.append(np.argmax(abs(dx)))
        xmask=list(set(xmask))
        print xmask
        #optimize corresponding axis
        print 'x0=%s'%x0[xmask]
        opt_cost,opt_x=case.optimize(xmask,x0=x0[xmask])
        x0[xmask]=opt_x
        print opt_cost

        if case.check_result(x0):
            print 'Find Result! x=%s, num_change = %s.'%(opt_x,len(xmask))
            break
        else:
            print 'Need more changes, cost=%s, x=%s'%(opt_cost,opt_x)
        pdb.set_trace()
    pdb.set_trace()

def method2(sheet=0):
    '''
    random choice.
    '''
    num_try=1000
    case=get_testcase(sheet)
    num_change=case.num_path
    #cope the index with maximum gradient
    xmask=np.zeros(case.num_path,dtype='bool')
    for ix in xrange(num_try):
        x0=np.zeros(case.num_path)
        xmask=np.random.choice(range(case.num_path),num_change)
        #random_mask1(xmask)
        #optimize corresponding axis
        print 'x0=%s'%x0[xmask]
        cost0=case.compute_cost(x0[xmask])
        opt_cost,opt_x=case.optimize(xmask,x0=x0[xmask])
        x0[xmask]=opt_x
        print cost0,opt_cost
        print opt_cost-cost0
        pdb.set_trace()

        if case.check_result(x0):
            print 'Find Result! x=%s, cost=%s, num_change = %s.'%(opt_x,opt_cost,len(xmask))
            break
        else:
            print 'Need more changes, cost=%s, x=%s'%(opt_cost,opt_x)
    pdb.set_trace()

def random_mask1(mask):
    indices=np.where(~mask)[0]
    rint=np.random.randint(0,len(indices))
    mask[rint]=True
    return mask

def method1(sheet=0):
    '''
    max gradient method.
    '''
    case=get_testcase(sheet)
    xmask=[]
    x0=np.zeros(case.num_path)
    #cope the index with maximum gradient
    for ix in xrange(case.num_path):
        dx=case.compute_gradient(x0,mask_y=False)
        dx[xmask]=0
        xmask.append(np.argmax(abs(dx)))
        xmask=list(set(xmask))
        print xmask
        #optimize corresponding axis
        print 'x0=%s'%x0[xmask]
        old_cost=case.compute_cost(x0[xmask])
        opt_cost,opt_x=case.optimize(xmask,x0=x0[xmask])
        x0[xmask]=opt_x
        if old_cost-opt_cost<1e-5:
            pass

        if case.check_result(x0):
            print 'Find Result! x=%s, num_change = %s.'%(opt_x,len(xmask))
            break
        else:
            print 'Need more changes, cost=%s, x=%s'%(opt_cost,opt_x)
        #pdb.set_trace()
    pdb.set_trace()

def method4(sheet):
    case=get_testcase(sheet)
    pdb.set_trace()
    dp=pinv(case.table).dot(case._center)-case.p0
    print case.compute_cost(dp)
    print case.compute_cost(np.zeros(case.num_path))
    print case.check_result(dp)

if __name__=='__main__':
    #case=get_testcase()
    #occ=case.get_occ(np.zeros(8))
    #print np.linalg.svd(case._table,full_matrices=False)[1]
    #print occ
    #pdb.set_trace()
    #load_test_data(1)

    #method1(sheet=1)
    #method2(sheet=1)
    method4(sheet=2)
