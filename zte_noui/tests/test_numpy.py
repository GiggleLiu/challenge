from ..poor_mans_numpy import *
if __name__=='__main__':
    m=[[1,2,3],[2,2.5,4],[3,4,5]]
    savetxt('test.dat',m)
    m2=int32(loadtxt('test.dat'))
    print m2
    print isinf(m2)
