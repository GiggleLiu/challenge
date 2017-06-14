import numpy as np

class BinPath(object):
    '''
    The Bin Path problem, ZTE challenge, second round.

    Attributes:
        :node_min: 1darray, minimum capacity increment of node.
        :node_max: 1darray, maximum capacity increment of node.
        :route_table: 2darray, maximum capacity increment of node.
    '''
    def __init__(self, node_min, node_max, route_table):
        self.node_min=np.asarray(node_min)
        self.node_max=np.asarray(node_max)
        self.route_table=route_table

    @property
    def num_node(self):
        '''Number of nodes'''
        return len(self.node_min)

    @property
    def num_path(self):
        '''Number of paths'''
        return len(self.route_table)

    def get_table(self, path_weights):
        '''
        Get the weight distribution matrix over nodes and paths.

        Parameters:
            :path_weights: 1darray, weight for each path.
        '''
        table=np.zeros([self.num_node,self.num_path],dtype='int32')
        for i in xrange(self.num_path):
            table[self.route_table[i],i]=path_weights[i]
        return table

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

    testcase=BinPath(node_min,node_max,route_table)
    return testcase

def method1():
    case=get_testcase()

if __name__=='__main__':
    case=get_testcase()
    table=case.get_table([5,6,15,5,-15,8,4,-10])
    print table
