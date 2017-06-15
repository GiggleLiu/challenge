import numpy as np
import pdb,xlrd
from climin import RmsProp,GradientDescent

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
        #self.route_table=route_table
        self.p0=np.asarray(p0)

        #table
        self._table=table
        self.table=table.copy()
        #self._table=np.zeros([self.num_node,self.num_path],dtype='float64')
        #for i in xrange(self.num_path):
        #    self._table[self.route_table[i],i]=1

        interval=self.node_max-self.node_min
        self._offset=(self.node_max+self.node_min-2*self._table.dot(p0))/interval
        pdb.set_trace()
        self._table/=interval[:,np.newaxis]/2.

    @property
    def num_node(self):
        '''Number of nodes'''
        return len(self.node_min)

    @property
    def num_path(self):
        '''Number of paths'''
        return self._table.shape[1]

    def get_overflow(self, path_weights):
        '''
        Get the weight distribution matrix over nodes and paths.

        Parameters:
            :path_weights: 1darray, weight for each path.
        '''
        return self._table.dot(path_weights)-self._offset

    def compute_gradient(self,x,xmask=None,mask_y=True):
        '''Compute the gradient.'''
        p=np.zeros(self.num_path)
        if xmask is not None:
            p[xmask]=x
        overflow=self.get_overflow(p)
        if mask_y:
            #mask y version
            overflow[abs(overflow)<1]=0
        if xmask is None:
            grad=self._table.T.dot(overflow)
        else:
            grad=self._table.T[xmask].dot(overflow)
        return grad

    def compute_cost(self,x,xmask=None):
        '''Compute the cost function.'''
        p=np.zeros(self.num_path)
        if xmask is not None:
            p[xmask]=x
        overflow=abs(self.get_overflow(p))-1
        return np.linalg.norm(overflow[overflow>0])**2

    def optimize(self,xmask,x0,niter=1000):
        #rms=RmsProp(wrt=x0,fprime=lambda x:self.compute_gradient(x,xmask),step_rate=1e-1)
        rms=GradientDescent(wrt=x0,fprime=lambda x:self.compute_gradient(x,xmask),step_rate=0.1)
        el=[]
        for i in xrange(niter):
            info=rms.minimize_until(lambda x:rms.n_iter>i)
            cost=self.compute_cost(rms.wrt,xmask)
            el.append(cost)
        return cost,x0

    def check_result(self,x):
        '''Check the correctness of result.'''
        #table=np.zeros([self.num_node,self.num_path],dtype='float64')
        #for i in xrange(self.num_path):
        #    table[self.route_table[i],i]=(self.p0+x)[i]
        table=self.table*(self.p0+x)
        occ=table.sum(axis=1)
        if all(occ>=self.node_min) and all(occ<=self.node_max):
            print 'Pass'
            return True
        else:
            print 'Not Pass'
            return False

def get_testcase(which=0):
    if which==1:
        return _load_test_data(1)
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
    wb = xlrd.open_workbook("data.xlsx")
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


def method1():
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

def method2():
    '''
    random choice.
    '''
    num_change=3
    num_try=100
    case=get_testcase()
    #cope the index with maximum gradient
    for ix in xrange(num_try):
        x0=np.zeros(case.num_path)
        xmask=np.random.choice(range(case.num_path),num_change)
        print xmask
        #optimize corresponding axis
        print 'x0=%s'%x0[xmask]
        opt_cost,opt_x=case.optimize(xmask,x0=x0[xmask])
        x0[xmask]=opt_x
        print x0

        if case.check_result(x0):
            print 'Find Result! x=%s, cost=%s, num_change = %s.'%(opt_x,opt_cost,len(xmask))
            break
        else:
            print 'Need more changes, cost=%s, x=%s'%(opt_cost,opt_x)
    pdb.set_trace()

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

if __name__=='__main__':
    #case=get_testcase()
    #occ=case.get_overflow(np.zeros(8))
    #print np.linalg.svd(case._table,full_matrices=False)[1]
    #print occ
    #load_test_data(1)

    method1(sheet=1)
    #method2()
