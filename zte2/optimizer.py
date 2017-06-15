import numpy as np
from numpy.linalg import norm
from abc import ABCMeta, abstractmethod

__all__=['Optimizer','RMSProp','DefaultOpt']


class Optimizer(object):
    '''
    Compute the change of paramter according to the gradient.
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self,key,g):
        '''
        Parameters:
            :key: object, key for indexing.
            :g: ndarray, the gradient.

        Return:
            ndarray, the change of data.
        '''
        pass

class DefaultOpt(Optimizer):
    '''Default optimizer.'''
    def __init__(self,rate,momentum=0):
        self.rate=rate
        self.momentum=momentum
        self.cum_gradient=0

    def __call__(self,g):
        if self.momentum!=0:
            gradient=self.cum_gradient*self.momentum+g
            self.cum_gradient=gradient
        else:
            gradient=g
        return -gradient*self.rate

class RMSProp(Optimizer):
    '''
    RMSProp adaptive optimizer.

    Parameters:
        :rate: float, learning rate.
        :delta: float, constant to assure numerical stability.
        :rho: float, decay rate.
        :r: array, the learning rate.
    '''
    def __init__(self,rate,rho,delta=1e-6):
        self.rate=rate
        self.rho=rho
        self.delta=delta
        self.r=0

    def __call__(self,g): #g is the gradient
        g_norm=norm(g)
        gv=g/g_norm
        self.r=self.r*self.rho/g_norm**2+(1-self.rho)*gv**2
        res=-self.rate/np.sqrt(self.r+self.delta)*gv
        return res


