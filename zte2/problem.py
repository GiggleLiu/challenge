import numpy as np

class BinPath(object):
    '''
    The Bin Path problem, ZTE challenge, second round.

    Attributes:
        :node_min: 1darray, minimum capacity increment of node.
        :node_max: 1darray, maximum capacity increment of node.
        :route_table: 2darray, maximum capacity increment of node.
    '''
    def __init__(self, node_min, node_max, route_table, p0):
        self.node_min=np.asarray(node_min)
        self.node_max=np.asarray(node_max)
        self.route_table=route_table
        self.p0=np.asarray(p0)

        #table
        self._table=np.zeros([self.num_node,self.num_path],dtype='float64')
        for i in xrange(self.num_path):
            self._table[self.route_table[i],i]=1

        interval=self.node_max-self.node_min
        self._offset=(self.node_max+self.node_min-2*self._table.dot(p0))/interval
        self._table/=interval[:,np.newaxis]/2.

    @property
    def num_node(self):
        '''Number of nodes'''
        return len(self.node_min)

    @property
    def num_path(self):
        '''Number of paths'''
        return len(self.route_table)

    def get_overflow(self, path_weights):
        '''
        Get the weight distribution matrix over nodes and paths.

        Parameters:
            :path_weights: 1darray, weight for each path.
        '''
        return self._table.dot(path_weights)-self._offset

    def compute_gradient(self,x):
        '''Compute the gradient.'''
        overflow=abs(self.get_overflow(x))-1
        overmask=overflow>1
        return self._table.T.dot((self._table.dot(x)-x))[overmask]

    def compute_cost(self,x):
        '''Compute the cost function.'''
        overflow=abs(self.get_overflow(x))-1
        return np.linalg.norm(overflow[overflow>0])**2

def get_testcase():
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

    testcase=BinPath(node_min,node_max,route_table,p0=p0)
    return testcase

def method1():
    case=get_testcase()

if __name__=='__main__':
    case=get_testcase()
    occ=case.get_overflow(np.zeros(8))
    #print np.linalg.svd(case._table,full_matrices=False)[1]
    print occ
