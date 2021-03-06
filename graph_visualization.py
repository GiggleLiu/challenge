'''
Visualization tools.
'''

from numpy import *
from numpy.linalg import norm,eigh
import scipy.sparse as sps
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import os

from graph import MyGraph

__all__=['visualize_graph','visualize_path','animate_path','distance2pos','visualize_tsp_mat']

radius=0.3

def distance2pos(dist_mat):
    '''
    Get "distance" from position matrix.

    https://math.stackexchange.com/questions/156161/finding-the-coordinates-of-points-from-distance-matrix
    '''
    M=dist_mat[:1,:]**2+dist_mat[:,:1]**2-dist_mat**2
    E,U=eigh(M); E[E<0]=0
    X=U*sqrt(E)
    major_columns=argsort(sum(abs(X),axis=0))[-2:]
    pos=X[:,major_columns]
    return pos

def plot_single_node(pos,color,text):
    ax=plt.gca()
    cir=plt.Circle(pos,radius=radius,facecolor=color,edgecolor='k',zorder=0)
    ax.add_patch(cir)
    plt.text(pos[0],pos[1],text,ha='center',va='center',fontsize=16)

def plot_single_connection(pos1,pos2,weight=1,text='',arrow_direction=0,color='k',textoffset=0.1,shrink=False):
    #fix position
    pos1,pos2=asarray(pos1),asarray(pos2)
    r=pos2-pos1
    norm_r=norm(r)
    dr=r/norm_r*0.3
    if shrink:
        pos1=pos1+dr
        pos2=pos2-dr

    fontsize=12
    ax=plt.gca()
    ax.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],lw=2,color=color,zorder=-1)
    #add a text.
    midpos=pos1*0.4+pos2*0.6
    midpos_text=pos1*0.3+pos2*0.7
    xy=midpos_text+textoffset*array([-r[1],r[0]])/norm_r  #move towards the vertical direction.
    ax.annotate(text,xytext=xy,xy=xy,va='center',ha='center',fontsize=fontsize,color='k',zorder=101)
    #add arrow
    if arrow_direction>0:
        ax.arrow(midpos[0],midpos[1],1e-5*dr[0],1e-5*dr[1],color=color,head_width=0.08,head_length=0.12,length_includes_head=False,zorder=99)
    elif arrow_direction<0:
        ax.arrow(midpos[0],midpos[1],-1e-5*dr[0],-1e-5*dr[1],color=color,head_width=0.08,head_length=0.12,length_includes_head=False,zorder=99)

def plot_single_connection_old(pos1,pos2,weight,color='k'):
    r=pos2-pos1
    norm_r=norm(r)
    dr=r/norm_r*0.3
    pos1=pos1+dr
    pos2=pos2-dr
    plt.plot([pos1[0],pos2[0]],[pos1[1],pos2[1]],lw=2,color=color)

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
    colors[0]='y'; colors[-1]='y'

    for i in xrange(ng):
        plot_single_node(poss[i],color=colors[i],text='%s'%i)
    for ii,(i,j,weight) in enumerate(g.connections):
        must_con=ii in g.must_connections
        plot_single_connection(poss[i],poss[j],weight=weight if not must_con else 3,text='%s'%weight,color='g' if must_con else 'k',shrink=True)


def visualize_path(g,path):
    if len(path)<1: pass
    node_color='r'
    edge_color='r'
    poss=g.node_positions[path]
    plt.scatter(poss[:,0],poss[:,1],facecolor=node_color,s=200,edgecolor='k',zorder=100)
    for i,(pos1,pos2) in enumerate(zip(poss[:-1],poss[1:])):
        plot_single_connection(pos1,pos2,text='%s'%i,arrow_direction=1,color='r',weight=2,textoffset=0,shrink=False)

def get_ant(pos):
    image_path=os.path.join(os.path.dirname(__file__),'static/ant.png')
    image=plt.imread(image_path)
    im=OffsetImage(image,zoom=0.1,zorder=200)
    ab=AnnotationBbox(im,(pos[0],pos[1]),xycoords='data',frameon=False)
    plt.gca().add_artist(ab)
    return ab

def ant_march(ant,pos):
    ant.xybox=pos
    return ant

def animate_path(g,path,ant_speed=1,filename=None):
    '''
    Ant March!
    '''
    if len(path)<1: return
    node_color='r'
    edge_color='r'
    poss=g.node_positions[path]
    walk_step=0.04*ant_speed
    ant=get_ant(poss[0])
    route=[]
    for i,(pos1,pos2) in enumerate(zip(poss[:-1],poss[1:])):
        r=pos2-pos1
        absr=norm(r)
        r=r/absr
        for ri in arange(0,absr,walk_step):
            pos_ant=pos1+r*ri
            #ant_march(ant,pos_ant)
            #plt.draw()
            #plt.pause(time_step)
            route.append(pos_ant)

    def update(i):
        return ant_march(ant,route[i]),

    anim = animation.FuncAnimation(plt.gcf(), update,  
                                   frames=len(route), 
                                   interval=100,repeat=False,
                                   blit=True)
    if filename is None:
        plt.show()
    else:
        anim.save(filename,dpi=80,writer='imagemagick')

def visualize_tsp_mat(tsp_mat,pos,nodes):
    N=len(tsp_mat)
    connections=reduce(lambda x,y:x+y,[[(nodes[i],nodes[j],tsp_mat[i,j]) for j in xrange(i)] for i in xrange(N)])
    g=MyGraph(connections=connections,
            node_positions=pos,
            must_nodes=nodes,
            must_connections=[i for i,con in enumerate(connections) if con[-1]==-0.1])
    ng=g.num_nodes
    poss=g.node_positions
    il,jl,weights=zip(*g.connections)

    colors=array(['w']*ng)
    colors[g.must_nodes]='g'
    colors[0]='y'; colors[-1]='y'

    for i in nodes:
        plot_single_node(poss[i],color=colors[i],text='%s'%i)
    for ii,(i,j,weight) in enumerate(g.connections):
        must_con=ii in g.must_connections
        plot_single_connection(poss[i],poss[j],weight=weight if not must_con else 3,text='%s'%weight,color='g' if must_con else 'k',shrink=True)


