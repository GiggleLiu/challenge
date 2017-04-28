import scipy.sparse as sps
import numpy as np
import pdb

__all__=['MyGraph','random_graph']

class MyGraph(object):
    '''
    Attributes:
        :connections: list, i,j,weight.
        :node_positions: 2darray, the positions of graph nodes.
        :must_nodes: list, nodes must be passed.
    '''
    def __init__(self,connections,node_positions,must_nodes=None,must_connections=None):
        self.connections=connections
        self.node_positions=np.asarray(node_positions)
        self.must_nodes=must_nodes if must_nodes is not None else []
        self.must_connections=must_connections if must_connections is not None else []
        il,jl,wl=zip(*self.connections)
        num_nodes=int(max(max(il),max(jl))+1)
        if num_nodes!=self.node_positions.shape[0] or self.node_positions.shape[1]!=2:
            raise ValueError()

        #initialize matrices.
        il,jl,weights=zip(*self.connections)
        il,jl=np.concatenate([il,jl]),np.concatenate([jl,il])
        weights=np.concatenate([weights,weights])
        self.sparse_matrix=sps.coo_matrix((weights,(il,jl)),dtype='float64')
        self.dense_matrix=np.zeros([num_nodes]*2)
        self.dense_matrix[il,jl]=weights

    def __str__(self):
        return 'Graph(%s nodes, %s legs)\n %s'%(self.num_nodes,self.num_paths,'\n '.join(str(con) for con in self.connections))

    @property
    def num_nodes(self):
        '''Number of nodes'''
        return self.dense_matrix.shape[0]

    @property
    def num_paths(self):
        '''Number of paths'''
        return len(self.connections)

    def get_cost(self,path):
        '''Calculate the cost for given path.'''
        il,jl=path[:-1],path[1:]
        diss=self.dense_matrix[il,jl]
        if any(diss==0): raise ValueError('Invalid Path!')
        return sum(diss)

def random_graph(num_nodes,density=1):
    m=np.random.random([num_nodes]*2)*3
    m[np.random.random([num_nodes]*2)>density]=0
    np.fill_diagonal(m,0)
    il,jl=np.where(m)
    weights=m[il,jl]
    return MyGraph(zip(il,jl,weights),node_positions=(np.random.random([num_nodes,2])-0.5)*num_nodes)
