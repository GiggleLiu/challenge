import numpy as np

from antcolony import AntGraph,AntColony
from setting import num_ants,num_ant_repetitions,num_ant_iterations,constraint_bisect_xtol,constrain_maxeval

def djfunc_tqk(mat,must_nodes,must_connections):
    '''Interfacing TQK's Dijkstra function.'''
    nt=len(must_nodes)+2*len(must_connections)+2
    tsp_mat=np.random.random([nt,nt])
    tsp_mat[1,2]=-2
    tsp_mat+=tsp_mat.T
    np.fill_diagonal(tsp_mat,0)
    predecesor=np.random.random([nt,len(mat)])
    return tsp_mat,predecesor

def tsp2path_tqk(best_path_vec,predecesor):
    '''Interfacing TQK's path recover function.'''
    nodes=range(predecesor.shape[1])
    best_path_vec_real=np.random.choice(nodes,np.random.randint(0,2*predecesor.shape[1]))
    return best_path_vec_real

def find_shortest_path(g,max_num_nodes=np.Inf):
    '''
    Parameters:
        :g: <Graph>,
        :max_num_nodes: int, the maximum number of allowed nodes.
    '''
    bias,res=bisect(lambda bias:_find_shortest_path1(g,bias,max_num_nodes=max_num_nodes),0,1,max_eval=constrain_maxeval,xtol=constraint_bisect_xtol)
    best_path_vec,best_path_cost=res
    if bias is None:
        print 'Can not find path within %s nodes.'%max_num_nodes
        print 'The reference path is %s, with cost %s.'%(best_path_vec,best_path_cost)
    else:
        print 'Find solution!'
        print 'The reference path is %s, with cost %s.'%(best_path_vec,best_path_cost)
    return res

def _find_shortest_path1(g,bias,max_num_nodes):
    '''
    Parameters:
        :g: <Graph>,
        :bias: float, in 0-1, 0 is the shortest path limit, 1 is the least node limit.
        :max_num_nodes: int, the maximum number of allowed nodes.

    Return:
        (is qualified,(best solution, cost of best solution)),
        qualified means the number of nodes do not exceed max_num_nodes.
    '''
    mm=np.zeros_like(g.dense_matrix)
    nzmask=g.dense_matrix!=0
    mm[nzmask]=g.dense_matrix[nzmask].mean()
    mat=g.dense_matrix*(1-bias)+bias*mm
    must_connections=[g.connections[ic][:2] for ic in g.must_connections]
    tsp_mat,predecesor=djfunc_tqk(mat,g.must_nodes,must_connections)

    #solve tsp using ant colony
    best_path_vecs,best_path_costs=solve_tsp_mat(tsp_mat)
    indmin=np.argmin(best_path_costs)
    best_path_vec=best_path_vecs[indmin]
    best_path_cost=best_path_costs[indmin]
    best_path_vec_real=tsp2path_tqk(best_path_vec,predecesor)
    qualified=len(best_path_vec_real)<=max_num_nodes
    return 1 if qualified else -1,(best_path_vec_real,best_path_cost)

def bisect(func, low, high, max_eval, xtol):
    '''find lowest qualified root of func'''
    flow,lres=func(low)
    if flow==1 or max_eval==1: return low,lres
    fhigh,hres=func(high)
    if flow==fhigh: return None,lres
    for i in range(max_eval-2):
        midpoint=(low+high)/2.
        fmid,mres=func(midpoint)
        if flow*fmid>0:
            low = midpoint
            flow=fmid
            lres=mres
        else:
            high = midpoint
            fhigh=fmid
        if abs(high-low)/2.<=xtol:
            break
    return low,lres

def solve_tsp_mat(tsp_mat):
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
        ant_colony = AntColony(graph, num_ants)
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


