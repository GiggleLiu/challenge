from numpy import *
from numpy.linalg import norm,svd
from copy import deepcopy
from numpy.testing import dec,assert_,assert_raises,assert_almost_equal,assert_allclose
from matplotlib.pyplot import *
import sys,pdb,time
from os import path
sys.path.insert(0,'../')

from testcases import *
from solvepath import find_shortest_path

random.seed(5)

def show_cases():
    plt.ion()
    fig=plt.figure(facecolor='w')
    plt.axis('equal')
    Gs=[G9]
    for ig,g in enumerate(Gs):
        plt.cla()
        plt.axis('off')
        visualize_graph(g)
        #visualize_path(g,g.solution)
        print 'The Cost is %s'%g.get_cost(g.solution)
        #animate_path(g,g.solution)#,filename='Ant-G%s'%ig)
        pdb.set_trace()

def test_saveload():
    print 'Test save and load of graph.'
    pref='sample'
    save_graph(pref,G0)
    G1=load_graph(pref)
    assert_allclose(G0.must_nodes,G1.must_nodes)
    assert_allclose(G0.node_positions,G1.node_positions)
    assert_allclose(G0.must_connections,G1.must_connections)
    assert_allclose(G0.connections,G1.connections)

    pdb.set_trace()

def test_shortest_path():
    from scipy.sparse.csgraph import shortest_path
    mat=G1.sparse_matrix
    dist_matrix=shortest_path(mat,method='D',directed=True)
    print 'The shortest distances between nodes are:\n%s'%dist_matrix

def test_g(g):
    solution,cost=find_shortest_path(g,max_num_nodes=12)
    print solution,cost
    #ion()
    visualize_graph(g)
    #visualize_path(g,solution)
    animate_path(g,solution)#,filename='Ant-G%s'%ig)
    axis('equal')
    axis('off')
    show()
    #pdb.set_trace()
    assert_allclose(solution,g.solution)

if __name__=='__main__':
    #test_saveload()
    #test_g(G9)
    #test_shortest_path()
    show_cases()
