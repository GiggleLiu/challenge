from numpy import *
import matplotlib.pyplot as plt
import pdb,sys
sys.path.insert(0,'../')

from graph import *
from graph_visualization import *

#challenge graph
G0=MyGraph(connections=[(0,1,3),(0,2,1),(0,3,1),
        (1,2,1),(1,4,1),(1,9,4),
        (2,3,1),(2,4,2),(2,5,1),
        (3,5,2),(3,6,2),(3,7,1),
        (4,5,1),(4,9,1),
        (5,6,1),(5,9,3),(5,10,1),(5,12,3),
        (6,7,1),(6,8,2),(6,12,2),(6,13,4),(6,14,3),
        (7,8,1),
        (8,14,1),(8,15,3),
        (9,10,1),(9,11,1),
        (10,11,1),(10,12,2),
        (11,16,1),
        (12,13,2),(12,16,1),
        (13,14,1),(13,15,2),(13,16,2),(13,17,1),
        (14,15,1),(15,17,4),
        (16,17,1)],
        node_positions=1.5*array([(0,0),(0.7,1.5),(0.9,0.5),(1,-0.5),
            (2,1.2),(2.4,0.3),(3,-0.5),(2,-1.2),
            (4,-1.7),(3,2.3),(3.5,1.5),(4.5,1.8),
            (4.7,0.5),(5.5,0),(4.7,-1.1),(5.4,-1.7),
            (5.4,1.5),(6.6,0.7)]),must_nodes=[7,12],
        must_connections=[7,33])
G0.solution=[0,2,4,5,6,8,14,13,12,16,17]

#double bridge model, typical case pure Simulated Annealing will fail.
G1=MyGraph(connections=[(0,1,0.3),(0,2,0.5),(1,3,0.5),(2,4,2),(3,5,0.8),\
        (4,6,0.1),(5,7,1.2),(6,7,0.4)],\
        node_positions=array([(0,0),(1,1),(1,-1),(2,1),(2,-1),(3,1),(3,-1),(4,0)]),\
        must_nodes=[],must_connections=[])
G1.solution=[0,1,3,5,7]

#sun model, typical case Dijkstra will fail.
sq05=sqrt(0.5)
G2=MyGraph(connections=[(0,1,0.3),(1,2,0.5),(1,3,0.5),(1,4,2),(1,5,0.8),\
        (1,6,0.1),(1,7,1.2),(1,8,0.7)],\
        node_positions=array([(-1,0),(0,0),(-sq05,sq05),(-sq05,-sq05),(0,1),(0,-1),(sq05,sq05),(sq05,-sq05),(1,0)]),\
        must_nodes=arange(2,8),must_connections=[])
G2.solution=[0,1,2,1,3,1,4,1,5,1,6,1,7,1,8]

#travaling salesman model
G3=MyGraph(connections=[(0,1,0.5),(0,2,1.5),(0,3,0.5),(0,4,2),(0,5,0.3),\
        (1,2,0.8),(1,3,1),(1,4,3),(1,5,5),(2,3,1.3),(2,4,0.4),(2,5,1),\
        (3,4,2.1),(3,5,0.2),(4,5,2)],
        node_positions=array([(cos(theta),sin(theta)) for theta in arange(0,2*pi,pi/3)]),\
        must_nodes=arange(1,6),must_connections=[])
G3.solution=[0,3,0,1,2,4,0,5]

#disconnected graph
G4=MyGraph(connections=[(0,1,1.),(0,2,0.5),(1,2,1.3),\
        (3,4,0.7),(3,5,3.),(4,5,1.),(4,6,0.8),(5,6,0.1)],\
        node_positions=[(0,0),(1,0),(0,-1),(2,0),(2,-1),(3.,0),(3.5,-0.5)],\
        must_connections=[7])
G4.solution=[] #no solusion

#pass the must connection twice
G5=MyGraph(connections=[(0,1,0.3),(1,2,0.5),(2,3,0.5),(1,4,2)],\
        node_positions=array([(0,0),(1,0.3),(1,1.3),(0,1),(2,0)]),\
        must_nodes=[3],must_connections=[1])
G5.solution=[0,1,2,3,2,1,4]

#must connection very high, pass one of must-connection-node twice
G6=MyGraph(connections=[(0,1,0.3),(1,2,10),(1,3,1),(2,3,0.5),(2,4,2)],\
        node_positions=array([(0,0),(1,0.3),(1,1.3),(0,1),(2,0)]),\
        must_nodes=[3],must_connections=[1])
G6.solution=[0,1,2,3,2,4]

#pass the must connection twice, soft cut 1,3
G7=MyGraph(connections=[(0,1,0.3),(1,2,0.5),(1,3,10),(2,3,0.5),(1,4,2)],\
        node_positions=array([(0,0),(1,0.3),(1,1.3),(0,1),(2,0)]),\
        must_nodes=[3],must_connections=[1])
G7.solution=[0,1,2,3,2,1,4]

#disconnected graph
G8=MyGraph(connections=[(3,1,1.),(3,2,0.5),(1,2,1.3),\
        (0,4,0.7),(0,5,3.),(4,5,1.),(4,6,0.8),(5,6,0.1)],\
        node_positions=[(2,0),(1,0),(0,-1),(0,0),(2,-1),(3.,0),(3.5,-0.5)],\
        must_connections=[7])
G8.solution=[0,4,5,6] #no solusion

#big lattice.
N=10
x,y=arange(10),arange(10)
X,Y=meshgrid(x,y,indexing='ij')
node_positions=zip(X.ravel(),Y.ravel())
Atom=arange(N**2).reshape([N,N])
connections=zip(Atom.ravel(),roll(Atom,1,axis=0).ravel(),ones(N**2))+zip(Atom.ravel(),roll(Atom,1,axis=1).ravel(),ones(N**2))
G9=MyGraph(connections=connections,node_positions=node_positions,must_nodes=unique(random.randint(0,N**2,N)),must_connections=unique(random.randint(0,2*N**2,N)))
G9.solution=[]

#start == end

Gs=[G0,G1,G2,G3,G4,G5,G6,G7,G8]
