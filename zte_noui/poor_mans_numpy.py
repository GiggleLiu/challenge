import __builtin__
Inf=99999999

def arange(mini,maxi=None,step=1):
    if maxi is None:
        mini,maxi=0,mini
    vals=[]
    val=mini
    while(maxi-val>1e-12):
        vals.append(val)
        val+=step
    return vals

def argmin(l):
    return min(enumerate(l),key=lambda y:y[1])[0]

def argmax(l):
    return max(enumerate(l),key=lambda y:y[1])[0]

def unique(l):
    return list(set(l))

def concatenate(l,axis=0):
    if axis==0:
        return reduce(lambda x,y:list(x)+list(y),l)
    else:
        return [concatenate([ln[i] for ln in l]) for i in xrange(len(l[0]))]

def repeat(l,n):
    return concatenate([[li]*n for li in l])

def asarray(l):
    return l

def array(l):
    return l

def ravel(m):
    if hasattr(m[0],'__iter__'):
        return reduce(lambda x,y:x+y,[ravel(mi) for mi in m])
    else:
        return list(m)

def where(lm):
    if hasattr(lm[0],'__iter__'):  #2D
        il,jl=[],[]
        for i,l in enumerate(lm):
            for j,item in enumerate(l):
                if item!=0:
                    il.append(i)
                    jl.append(j)
        return il,jl
    else:
        il=[]
        for i,item in enumerate(lm):
            if item !=0:
                il.append(i)
        return il,

def roll(l,n,axis=0):
    if axis==0:
        l=l[-n:]+l[:-n]
        return l
    else:
        return [roll(li,n,axis=axis-1) for li in l]

def zeros(shape,**kwargs):
    if not hasattr(shape,'__iter__'):
        shape=[shape]
    if len(shape)==2:
        return [[0 for j in xrange(shape[1])] for i in xrange(shape[0])]
    else:
        return [0 for i in xrange(shape[0])]

def any(lm):
    if hasattr(lm[0],'__iter__'):
        __builtin__.any([any(l) for l in lm])
    else:
        return __builtin__.any(lm)

def all(lm):
    if hasattr(lm[0],'__iter__'):
        __builtin__.all([all(l) for l in lm])
    else:
        return __builtin__.all(lm)

def ones(shape,**kwargs):
    if not hasattr(shape,'__iter__'):
        shape=[shape]
    if len(shape)==2:
        return [[1 for j in xrange(shape[1])] for i in xrange(shape[0])]
    else:
        return [1 for i in xrange(shape[0])]

def searchsorted(l,num):
    for i,li in enumerate(l):
        if li>num:
            return i

def cumsum(l):
    s=[]
    cum=0
    for li in l:
        cum+=li
        s.append(cum)
    return s

def mean(l):
    return sum(l)*1./len(l)

def fill_diagonal(m,num):
    for i in xrange(len(m)):
        m[i][i]=num

def sum(lm):
    if hasattr(lm[0],'__iter__'):
        return __builtin__.sum([sum(l) for l in lm])
    else:
        return __builtin__.sum(lm)

def savetxt(filename,m):
    with open(filename,'w') as f:
        for l in m:
            f.write(' '.join([str(li) for li in l])+'\n')

def loadtxt(filename):
    m=[]
    with open(filename,'r') as f:
        for line in f:
            sl=line.strip('\n').split(' ')
            l=[float(s) for s in sl]
            m.append(l)
    return m

def multiply(a,b):
    if not hasattr(a,'__iter__'):
        if not hasattr(b,'__iter__'):
            return a*b
        else:
            return [multiply(a,bi) for bi in b]
    else:
        if not hasattr(b,'__iter__'):
            return [multiply(ai,b) for ai in a]
        else:
            return [multiply(ai,bi) for ai,bi in zip(a,b)]

def add(a,b):
    if not hasattr(a,'__iter__'):
        if not hasattr(b,'__iter__'):
            return a+b
        else:
            return [add(a,bi) for bi in b]
    else:
        if not hasattr(b,'__iter__'):
            return [add(ai,b) for ai in a]
        else:
            return [add(ai,bi) for ai,bi in zip(a,b)]


def divide(a,b):
    if not hasattr(a,'__iter__'):
        if not hasattr(b,'__iter__'):
            return a/b
        else:
            return [divide(a,bi) for bi in b]
    else:
        if not hasattr(b,'__iter__'):
            return [divide(ai,b) for ai in a]
        else:
            return [divide(ai,bi) for ai,bi in zip(a,b)]

def shape(lm):
    if hasattr(lm[0],'__iter__'):
        return len(lm),len(lm[0])
    else:
        return len(lm),

def reshape(l,sp):
    if len(sp)==1:
        return l
    size=len(l)/sp[0]
    ll=[]
    for i in xrange(sp[0]):
        ll.append(reshape(l[i*size:i*size+size],sp[1:]))
    return ll

def int32(m):
    if hasattr(m,'__iter__'):
        return [int32(mi) for mi in m]
    else:
        return int(m)

def isinf(l):
    if hasattr(l,'__iter__'):
        return [isinf(li) for li in l]
    else:
        return l==Inf

def take(m,indices,axis=0):
    if axis==0:
        return [m[ind] for ind in indices]
    else:
        return [take(mi,indices,axis=axis-1) for mi in m]

def power(l,x):
    if not hasattr(l,'__iter__'):
        return l**x
    else:
        return [power(li,x) for li in l]

def mix_mat_by_mean(gmat,bias,mean_weight):
    m=zeros(shape(gmat))
    for i,l in enumerate(gmat):
        for j,item in enumerate(l):
            if item!=0:
                m[i][j]=item*(1-bias)+bias*mean_weight
    return m
