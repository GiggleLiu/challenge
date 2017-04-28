from testcases import *

def show_cases():
    plt.ion()
    fig=plt.figure(facecolor='w')
    plt.axis('equal')
    for ig,g in enumerate(Gs):
        plt.cla()
        plt.axis('off')
        visualize_graph(g)
        visualize_path(g,g.solution)
        print 'The Cost is %s'%g.get_cost(g.solution)
        #animate_path(g,g.solution)#,filename='Ant-G%s'%ig)
        pdb.set_trace()

def test_shortest_path():
    from scipy.sparse.csgraph import shortest_path
    mat=G1.sparse_matrix
    dist_matrix=shortest_path(mat,method='D',directed=True)
    print 'The shortest distances between nodes are:\n%s'%dist_matrix

if __name__=='__main__':
    test_shortest_path()
    show_cases()
