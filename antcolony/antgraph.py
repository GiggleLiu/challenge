from threading import Lock
import numpy as np

class AntGraph:
    def __init__(self, delta_mat, tau_mat=None):
        num_nodes=len(delta_mat)
        self.delta_mat = delta_mat # matrix of node distance deltas

        # tau mat contains the amount of phermone at node x,y
        if tau_mat is None:
            self.tau_mat=np.zeros([num_nodes,num_nodes])
        else:
            self.tau_mat=tau_mat

    @property
    def num_nodes(self): return len(self.delta_mat)

    def reset_tau(self):
        avg = self.delta_mat.mean()

        # initial tau 
        self.tau0=1.0 / (self.num_nodes * 0.5 * avg)
        self.tau_mat[...] = self.tau0
