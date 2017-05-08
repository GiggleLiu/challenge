import scipy.sparse as sps
import numpy as np

__all__=['MyGraph','random_graph','save_graph','load_graph']

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
            print self.node_positions,num_nodes
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
        if np.any(diss==0): raise ValueError('Invalid Path!')
        return np.sum(diss)

def save_graph(graph_prefix,graph):
    must_nodes_mask=np.zeros(graph.num_nodes)
    must_nodes_mask[graph.must_nodes]=1
    np.savetxt(graph_prefix+'.nod.dat',np.concatenate([graph.node_positions,must_nodes_mask[:,np.newaxis]],axis=1))
    must_con_mask=np.zeros(len(graph.connections))
    must_con_mask[graph.must_connections]=1
    np.savetxt(graph_prefix+'.con.dat',np.concatenate([graph.connections,must_con_mask[:,np.newaxis]],axis=1))

def load_graph(graph_prefix):
    #load nodes
    pos_data=np.loadtxt(graph_prefix+'.nod.dat')
    must_nodes=np.where(pos_data[:,-1])[0]
    node_positions=pos_data[:,:2]
    #load connections
    con_data=np.loadtxt(graph_prefix+'.con.dat')
    connections=[(int(data[0]),int(data[1]),data[2]) for data in con_data]
    must_connections=np.where(con_data[:,-1])[0]
    g=MyGraph(connections,node_positions,must_nodes=must_nodes,must_connections=must_connections)
    return g

def random_graph(num_nodes,density=1):
    m=np.random.random([num_nodes]*2)*3
    m[np.random.random([num_nodes]*2)>density]=0
    np.fill_diagonal(m,0)
    il,jl=np.where(m)
    weights=m[il,jl]
    return MyGraph(zip(il,jl,weights),node_positions=(np.random.random([num_nodes,2])-0.5)*num_nodes)
