#import numpy as np
import poor_mans_numpy as np
#from scipy.sparse.csgraph import dijkstra
from dijkstra import dijkstra
import sys,time

from antcolony import AntGraph,AntColony

def find_shortest_path(g,max_num_nodes=np.Inf,ant_config={},max_eval=5,bias_neg=-0.1):
    '''
    Parameters:
        :g: <Graph>,
        :max_num_nodes: int, the maximum number of allowed nodes.
    '''
    bias,res=bisect(lambda bias:_find_shortest_path1(g,bias,max_num_nodes=max_num_nodes,ant_config=ant_config,bias_neg=bias_neg),0,1,max_eval=max_eval)
    best_path_vec,best_path_cost=res
    true_cost=g.get_cost(best_path_vec)
    if bias is None:
        print 'Can not find path within %s nodes.'%max_num_nodes
    else:
        print 'Find solution!'
    return best_path_vec,true_cost

def _find_shortest_path1(g,bias,max_num_nodes,ant_config,bias_neg):
    '''
    Parameters:
        :g: <Graph>,
        :bias: float, in 0-1, 0 is the shortest path limit, 1 is the least node limit.
        :max_num_nodes: int, the maximum number of allowed nodes.
        :ant_config: dict, configurations of ant colony algorithm.

    Return:
        (is qualified,(best solution, cost of best solution)),
        qualified means the number of nodes do not exceed max_num_nodes.
    '''
    mat=np.mix_mat_by_mean(g.dense_matrix,bias,mean_weight=np.mean([con[-1] for con in g.connections]))
    must_connections=[g.connections[ic][:2] for ic in g.must_connections]

    must_nodes=np.int32(np.unique(np.concatenate([g.must_nodes,[0,g.num_nodes-1],np.ravel(np.array(must_connections))])))
    must_nodes.sort()
    t0=time.time()
    print '  Running Dijkstra to convert the graph to TSP problem.'
    tsp_mat,predecesor=djfunc_tqk(mat,must_nodes,must_connections,bias_neg=bias_neg)
    t1=time.time()

    #solve tsp using ant colony
    print '  Running Ant Conlony Optimization.'
    best_path_vecs,best_path_costs=solve_tsp_mat(tsp_mat,**ant_config)
    t2=time.time()
    indmin=np.argmin(best_path_costs)
    best_path_vec=best_path_vecs[indmin]
    best_path_cost=best_path_costs[indmin]
    best_path_vec_real=tsp2path_tqk(best_path_vec,must_nodes,predecesor)
    qualified=len(best_path_vec_real)<=max_num_nodes
    print '  Done! Time Elapse -> Dijkstra = %ss, Ant-Colony = %ss'%(t1-t0,t2-t1)
    return 1 if qualified else -1,(best_path_vec_real,best_path_cost)

def bisect(func, low, high, max_eval):
    '''find lowest qualified root of func'''
    print 'Bisect: 1st iteration for bias lambda = %s (shortest path)'%low
    flow,lres=func(low)
    if flow==1 or max_eval==1: return low,lres
    print 'Bisect: 2nd iteration for bias lambda = %s (minimal number of nodes)'%high
    fhigh,hres=func(high)
    if flow==fhigh: return None,lres
    for i in range(max_eval-2):
        midpoint=(low+high)/2.
        print 'Bisect: %s iteration for bias lambda = %s (minimal number of nodes)'%(str(i+3)+('rd' if i==0 else 'th'),midpoint)
        fmid,mres=func(midpoint)
        if flow*fmid>0:
            low = midpoint
            flow=fmid
        else:
            high = midpoint
            fhigh=fmid
            hres=mres
    return high,hres

def solve_tsp_mat(tsp_mat,num_ants=30,num_ant_repetitions=1,num_ant_iterations=20):
    '''
    Solve TSP problem using Ant Colony Algorithm.

    Return:
        (list, list), best paths and costs in each repetition.
    '''
    graph = AntGraph(tsp_mat)
    best_path_vec = []
    best_path_cost = []
    for i in range(num_ant_repetitions):
        graph.reset_tau()
        ant_colony = AntColony(graph, num_ants, start_node=0,end_node=len(tsp_mat)-1)
        ant_colony.run(num_ant_iterations)
        best_path_vec.append(ant_colony.best_path_vec)
        best_path_cost.append(ant_colony.best_path_cost)
    return best_path_vec,best_path_cost

def analyse_tsp_solutions(best_path_vec,best_path_cost):
    '''
    Analyse solutions.
    '''
    indmin=np.argmin(best_path_cost)
    print "\n------------------------------------------------------------"
    print "                     Results                                "
    print "------------------------------------------------------------"
    print "\nBest path = %s" % (best_path_vec[indmin],)
    print "\nBest path cost = %s\n" % (best_path_cost[indmin],)
    correct_rate=(best_path_cost[indmin]==np.array(best_path_cost)).mean()
    print 'Correct Rate = %s'%correct_rate

def djfunc_tqk(mat,node,line,bias_neg=-0.1):
    '''Interfacing TQK's Dijkstra function.'''
    dist,pred=dijkstra(mat,return_predecessors=True)
    #dist,pred=dijkstra(mat,indices=node,return_predecessors=True)
    if np.any(np.isinf(np.take(dist[0],node))):
        print 'Can not find solution, must_pass nodes disconnected!'
        sys.exit()
    for i in xrange(len(line)):
        pred[line[i][0]][line[i][1]]=line[i][0]
        pred[line[i][1]][line[i][0]]=line[i][1]
        dist[line[i][0]][line[i][1]]=bias_neg
        dist[line[i][1]][line[i][0]]=bias_neg
    d=np.take(np.take(dist,node,axis=0),node,axis=1)
    return d,pred

def tsp2path_tqk(tsp_solution,node,pred):
    '''Interfacing TQK's path recover function.'''
    a=[]
    n=len(node)
    node=np.asarray(node)
    b=np.take(node,tsp_solution)
    b=b[::-1]
    for i in xrange(n-1):
        j=b[i]
        k=b[i+1]
        a.append(b[i])
        while pred[k][j]!=k and pred[k][j]>=0:
            j=pred[k][j]
            a.append(j)
    a.append(b[-1])
    return a[::-1]

