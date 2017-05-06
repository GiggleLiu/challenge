from configobj import ConfigObj
from validate import Validator
import matplotlib.pyplot as plt
import os,sys
import numpy as np

from graph_visualization import animate_path,visualize_graph,visualize_path
from graph import load_graph
from solvepath import find_shortest_path

def run_config(config_file):
    '''
    TODO: start == end? start, end at random position?
    '''
    #read config
    specfile=os.path.join(os.path.dirname(__file__),'config-spec.ini')
    config=ConfigObj(config_file,configspec=specfile,stringify=True)
    validator = Validator()
    result = config.validate(validator,preserve_errors=True)
    if result!=True:
        raise ValueError('Configuration Error! %s'%result)
    max_num_nodes=config['problem']['max_num_nodes']
    graph_spec=config['problem']['graph_specify']
    np.random.seed(config['program']['random_seed'])

    from testcases import Gs  #import testcase here to make random_seed take effect
    if graph_spec<0:
        graph_prefix=config['problem']['graph_file_prefix']
        g=load_graph(graph_prefix)
    else:
        g=Gs[graph_spec]

    solution,cost=find_shortest_path(g,max_num_nodes=max_num_nodes,djmethod=config['program']['shortest_path_algorithm'],\
            ant_config=config['ant_colony'],max_eval=config['problem']['constraint_maxeval'])

    vconfig=config['visualization']
    visualize_method=vconfig['visualize_method']
    if visualize_method=='no':
        return
    fig=plt.figure(figsize=(8,6),facecolor='w')
    visualize_graph(g)
    plt.axis('equal')
    plt.axis('off')
    fig.tight_layout()
    if visualize_method=='red-line':
        visualize_path(g,solution)
        plt.show()
    elif visualize_method=='animate':
        animate_path(g,solution,ant_speed=vconfig['ant_speed'])
        plt.show()
    elif visualize_method=='save-gif':
        fname=vconfig['gif_filename']
        print 'Generating Gif file (may take a while)...'
        animate_path(g,solution,ant_speed=vconfig['ant_speed'],filename=fname)
        print 'Saved to file %s'%fname

if __name__=='__main__':
    if len(sys.argv)>1:
        config_file=sys.argv[1]
    else:
        config_file='config-sample.ini'
    run_config(config_file)
