from numpy import *
import matplotlib.pyplot as plt
import pdb

from graph import *
from graph_visualization import *

#double bridge model
G1=MyGraph(connections=[(0,1,0.3),(0,2,0.5),(1,3,0.5),(2,4,2),(3,5,0.8),\
        (4,6,0.1),(5,7,1.2),(6,7,0.4)],\
        node_positions=array([(0,0),(1,1),(1,-1),(2,1),(2,-1),(3,1),(3,-1),(4,0)]),\
        must_nodes=[],must_connections=[])

#sun model
sq05=sqrt(0.5)
G2=MyGraph(connections=[(1,0,0.3),(1,2,0.5),(1,3,0.5),(1,4,2),(1,5,0.8),\
        (1,6,0.1),(1,7,1.2),(1,8,0.7)],\
        node_positions=array([(-1,0),(0,0),(-sq05,sq05),(-sq05,-sq05),(0,1),(0,-1),(sq05,sq05),(sq05,-sq05),(1,0)]),\
        must_nodes=arange(2,8),must_connections=[])

#travaling salesman model
G3=random_graph(8); G3.must_nodes=arange(1,7)

G4=MyGraph(connections=[(0,1,1.),(0,2,0.5),(1,2,1.3),(1,3,0.2),(2,3,0.5),(2,4,0.5),\
        (3,4,0.7),(3,5,3.),(4,5,1.),(4,6,0.8),(5,6,0.1)],\
        node_positions=[(0,0),(1,0),(0,-1),(2,0),(2,-1),(3.,0),(3.5,-0.5)],\
        must_connections=[7])

Gs=[G1,G2,G3,G4]

def show_cases():
    plt.ion()
    plt.axis('equal')
    for g in Gs:
        plt.cla()
        visualize_graph(g)
        pdb.set_trace()

if __name__=='__main__':
    show_cases()
