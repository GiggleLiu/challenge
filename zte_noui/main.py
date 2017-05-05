import os,sys,pdb
import ConfigParser
from graph import load_graph
from solvepath import find_shortest_path
from testcases import Gs
import random

def run_config(config_file):
    '''
    TODO: start == end? start, end at random position?
    '''
    #read config
    config=ConfigParser.RawConfigParser()
    config.read(config_file)
    random.seed(config.getint('program','random_seed'))
    max_num_nodes=config.getint('problem','max_num_nodes')
    graph_spec=config.getint('problem','graph_specify')
    if graph_spec<0:
        graph_prefix=config.get('problem','graph_file_prefix')
        g=load_graph(graph_prefix)
    else:
        g=Gs[graph_spec]

    ant_config={
            'num_ants':config.getint('ant_colony','num_ants'),
            'num_ant_repetitions':config.getint('ant_colony','num_ant_repetitions'),
            'num_ant_iterations':config.getint('ant_colony','num_ant_iterations')}

    solution,cost=find_shortest_path(g,max_num_nodes=max_num_nodes,djmethod=config.get('program','shortest_path_algorithm'),\
            ant_config=ant_config,max_eval=config.getint('problem','constraint_maxeval'))

if __name__=='__main__':
    if len(sys.argv)>1:
        config_file=sys.argv[1]
    else:
        config_file='config-sample.ini'
    run_config(config_file)
