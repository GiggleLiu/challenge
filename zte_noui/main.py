import os,sys
import ConfigParser
import random

from graph import load_graph
from solvepath import find_shortest_path

def run_config(config_file):
    '''
    TODO: start == end? start, end at random position?
    '''
    #read config
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    random.seed(config.getint('program','random_seed'))
    from testcases import Gs  #import testcase here to make random_seed take effect

    max_num_nodes=config.getint('problem','max_num_nodes')
    graph_spec=config.getint('problem','graph_specify')
    print '='*15+' LOAD DATA '+'='*15
    if graph_spec<0:
        print 'Loading graph from file ...'
        graph_prefix=config.get('problem','graph_file_prefix')
        g=load_graph(graph_prefix)
    else:
        print 'Loading test case %s.'%graph_spec
        g=Gs[graph_spec]
    print 'The graph your have specified is\n%s'%g
    print '  The maximum allowed number of nodes in a path is %s'%max_num_nodes

    ant_config={
            'num_ants':config.getint('ant_colony','num_ants'),
            'num_ant_repetitions':config.getint('ant_colony','num_ant_repetitions'),
            'num_ant_iterations':config.getint('ant_colony','num_ant_iterations')}

    print '='*15+' FIND SOLUTION '+'='*15
    best_path_vec,true_cost=find_shortest_path(g,max_num_nodes=max_num_nodes,\
            ant_config=ant_config,max_eval=config.getint('problem','constraint_maxeval'),\
            bias_neg=config.getfloat('program','bias_neg'))

    print '='*15+' ANALYSE RESULT '+'='*15
    print 'The reference path is %s, with cost %s.'%(best_path_vec,true_cost)
    print 'must nodes passed %s/%s'%(len([node for node in g.must_nodes if node in best_path_vec]),len(g.must_nodes))
    all_paths=zip(best_path_vec[:-1],best_path_vec[1:])+zip(best_path_vec[1:],best_path_vec[:-1])
    print 'must paths passed %s/%s'%(len([icon for icon in g.must_connections if g.connections[icon][:2] in all_paths]),len(g.must_connections))

if __name__=='__main__':
    if len(sys.argv)>1:
        config_file=sys.argv[1]
    else:
        config_file='config-sample.ini'
    run_config(config_file)
