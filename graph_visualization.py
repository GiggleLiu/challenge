'''
Visualization tools.
'''

from numpy import *
from numpy.linalg import norm
import scipy.sparse as sps
import matplotlib.pyplot as plt
import pdb

__all__=['visualize_graph']

radius=0.3

def plot_single_node(pos,color,text):
    ax=plt.gca()
    cir=plt.Circle(pos,radius=radius,facecolor=color,edgecolor='k')
    ax.add_patch(cir)
    plt.text(pos[0],pos[1],text,ha='center',va='center',fontsize=16)

def plot_single_connection(pos1,pos2,weight,color='k'):
    r=pos2-pos1
    norm_r=norm(r)
    dr=r/norm_r*0.3
    pos1=pos1+dr
    pos2=pos2-dr
    plt.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],lw=2*weight,color=color)

def visualize_graph(g):
    '''
    Parameters:
        :g: matrix, the graph.
    '''
    ng=g.num_nodes
    poss=g.node_positions
    il,jl,weights=zip(*g.connections)
    #gm=g.construct_graph_matrix()
    #if isinstance(gm,ndarray):
    #    il,jl=where(gm!=0)
    #    weights=gm[il,jl]
    #elif sps.issparse(gm):
    #    gm=gm.tocoo()
    #    il,jl,weights=gm.row,gm.col,gm.data
    #else:
    #    raise ValueError()
    colors=array(['w']*ng)
    colors[g.must_nodes]='g'

    for i in xrange(ng):
        plot_single_node(poss[i],color=colors[i],text='%s'%i)
    for ii,(i,j,weight) in enumerate(g.connections):
        plot_single_connection(poss[i],poss[j],weight=weight,color='g' if ii in g.must_connections else 'k')

