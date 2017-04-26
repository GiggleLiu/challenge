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
        ng=self.num_nodes
        if ng!=self.node_positions.shape[0] or self.node_positions.shape[1]!=2:
            raise ValueError()

    @property
    def num_nodes(self):
        '''Number of nodes'''
        il,jl,wl=zip(*self.connections)
        return int(max(max(il),max(jl))+1)

    def construct_graph_matrix(self,mtype='sparse'):
        '''
        Parameters:
            :mtype: 'sparse'/'dense'.
        '''
        il,jl,weights=zip(*self.connections)
        il,jl=np.concatenate([il,jl]),np.concatenate([jl,il])
        weights=np.concatenate([weights,weights])
        if mtype=='sparse':
            mat=sps.coo_matrix((weights,(il,jl)),dtype='float64')
        elif mtype=='dense':
            mat=zeros([self.num_nodes]*2)
            mat[il,jl]=weights
        else:
            raise ValueError('Wrong type of matrix.')
        return mat

def random_graph(num_nodes,density=1):
    m=np.random.random([num_nodes]*2)*3
    m[np.random.random([num_nodes]*2)>density]=0
    np.fill_diagonal(m,0)
    il,jl=np.where(m)
    weights=m[il,jl]
    return MyGraph(zip(il,jl,weights),node_positions=(np.random.random([num_nodes,2])-0.5)*num_nodes)
