from numpy import *

class NNSolver(object):
    '''
    Neural network solver.
    '''
    def __init_(self,W):
        self.W=W

    def forward(self,x):
        '''Forward scan'''
