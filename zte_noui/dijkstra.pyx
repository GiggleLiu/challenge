from libc.stdlib cimport malloc, free

Inf=99999999
NULL_IDX=-9999

def dijkstra(csgraph, indices=None,
             return_predecessors=False,
             limit=Inf):
    """
    dijkstra(csgraph, indices=None, return_predecessors=False,
             unweighted=False, limit=np.inf)
    Dijkstra algorithm using Fibonacci Heaps
    Parameters
    ----------
    csgraph : array, matrix, or sparse matrix, 2 dimensions
        The N x N array of non-negative distances representing the input graph.
    indices : array_like or int, optional
        if specified, only compute the paths for the points at the given
        indices.
    return_predecessors : bool, optional
        If True, return the size (N, N) predecesor matrix
    unweighted : bool, optional
        If True, then find unweighted distances.  That is, rather than finding
        the path between each point such that the sum of weights is minimized,
        find the path such that the number of edges is minimized.
    limit : float, optional
        The maximum distance to calculate, must be >= 0. Using a smaller limit
        will decrease computation time by aborting calculations between pairs
        that are separated by a distance > limit. For such pairs, the distance
        will be equal to np.inf (i.e., not connected).
        .. versionadded:: 0.14.0
    Returns
    -------
    dist_matrix : ndarray
        The matrix of distances between graph nodes. dist_matrix[i,j]
        gives the shortest distance from point i to point j along the graph.
    predecessors : ndarray
        Returned only if return_predecessors == True.
        The matrix of predecessors, which can be used to reconstruct
        the shortest paths.  Row i of the predecessor matrix contains
        information on the shortest paths from point i: each entry
        predecessors[i, j] gives the index of the previous node in the
        path from point i to point j.  If no path exists between point
        i and j, then predecessors[i, j] = -9999
    Notes
    -----
    As currently implemented, Dijkstra's algorithm does not work for
    graphs with direction-dependent distances when directed == False.
    i.e., if csgraph[i,j] and csgraph[j,i] are not equal and
    both are nonzero, setting directed=False will not yield the correct
    result.
    Also, this routine does not work for graphs with negative
    distances.  Negative distances can lead to infinite cycles that must
    be handled by specialized algorithms such as Bellman-Ford's algorithm
    or Johnson's algorithm.
    """
    #------------------------------
    # validate csgraph and convert to csr matrix
    N = len(csgraph)
    ptr_=0
    cdef int *csr_indptr = <int *>malloc((N+1) * sizeof(int))
    csr_indices_,csr_data_=[],[]
    csr_indptr[0]=ptr_
    for i in xrange(N):
        for j in xrange(N):
            data=csgraph[i][j]
            if data!=0:
                csr_indices_.append(j)
                csr_data_.append(data)
                ptr_+=1
        csr_indptr[i+1]=ptr_
    ndata=len(csr_indices_)
    cdef int *csr_indices = <int *>malloc(ndata * sizeof(int))
    cdef double *csr_data = <double *>malloc(ndata * sizeof(double))
    for i in xrange(ndata):
        csr_data[i] = csr_data_[i]
        csr_indices[i] = csr_indices_[i]


    #------------------------------
    # intitialize/validate indices
    if indices is None:
        indices=range(N)
    nind=len(indices)
    return_shape = (nind,N)
    cdef int *indices_c = <int *>malloc(nind * sizeof(int))
    for i in xrange(nind):
        indices_c[i]=indices[i]

    #------------------------------
    # initialize dist_matrix for output
    dist_matrix=[]
    for i in xrange(nind):
        dist_matrix.append([Inf if j!=indices[i] else 0 for j in xrange(N)])
        #for j in xrange(N):
        #    dist_matrix[i][j]=Inf if j!=indices[i] else 0

    #------------------------------
    # initialize predecessors for output
    #cdef int[ind][N] predecessor_matrix
    #predecessor_matrix=NULL_IDX
    predecessor_matrix=[[NULL_IDX for j in xrange(N)] for i in xrange(nind)]

    _dijkstra_directed(indices_c,
                       csr_data, csr_indices, csr_indptr,
                       dist_matrix, predecessor_matrix, limit)

    return dist_matrix,predecessor_matrix

cdef _dijkstra_directed(int* source_indices,
        double* csr_weights,
        int* csr_indices,
        int* csr_indptr,
        dist_matrix,
        pred,
        double limit):
    cdef unsigned int Nind = len(dist_matrix)
    cdef unsigned int N = len(dist_matrix[0])
    cdef unsigned int i, k, j_source, j_current
    cdef int j

    cdef double next_val


    cdef FibonacciHeap heap
    cdef FibonacciNode *v
    cdef FibonacciNode *current_node
    cdef FibonacciNode* nodes = <FibonacciNode*> malloc(N *
                                                        sizeof(FibonacciNode))

    #print csr_weights[0],csr_indices[0],csr_indptr[0],dist_matrix[0],pred[0]
    for i in range(Nind):
        j_source = source_indices[i]

        for k in range(N):
            initialize_node(&nodes[k], k)

        dist_matrix[i][j_source] = 0
        heap.min_node = NULL
        insert_node(&heap, &nodes[j_source])

        while heap.min_node:
            v = remove_min(&heap)
            v.state = SCANNED

            for j in range(csr_indptr[v.index], csr_indptr[v.index + 1]):
                j_current = csr_indices[j]
                current_node = &nodes[j_current]
                if current_node.state != SCANNED:
                    next_val = v.val + csr_weights[j]
                    if next_val <= limit:
                        if current_node.state == NOT_IN_HEAP:
                            current_node.state = IN_HEAP
                            current_node.val = next_val
                            insert_node(&heap, current_node)
                            pred[i][j_current] = v.index
                        elif current_node.val > next_val:
                            decrease_val(&heap, current_node,
                                         next_val)
                            pred[i][j_current] = v.index

            #v has now been scanned: add the distance to the results
            dist_matrix[i][v.index] = v.val
    free(nodes)

######################################################################
# FibonacciNode structure
#  This structure and the operations on it are the nodes of the
#  Fibonacci heap.
#
cdef enum FibonacciState:
    SCANNED
    NOT_IN_HEAP
    IN_HEAP


cdef struct FibonacciNode:
    unsigned int index
    unsigned int rank
    FibonacciState state
    double val
    FibonacciNode* parent
    FibonacciNode* left_sibling
    FibonacciNode* right_sibling
    FibonacciNode* children


cdef void initialize_node(FibonacciNode* node,
                          unsigned int index,
                          double val=0):
    # Assumptions: - node is a valid pointer
    #              - node is not currently part of a heap
    node.index = index
    node.val = val
    node.rank = 0
    node.state = NOT_IN_HEAP

    node.parent = NULL
    node.left_sibling = NULL
    node.right_sibling = NULL
    node.children = NULL


cdef FibonacciNode* rightmost_sibling(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    cdef FibonacciNode* temp = node
    while(temp.right_sibling):
        temp = temp.right_sibling
    return temp


cdef FibonacciNode* leftmost_sibling(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    cdef FibonacciNode* temp = node
    while(temp.left_sibling):
        temp = temp.left_sibling
    return temp


cdef void add_child(FibonacciNode* node, FibonacciNode* new_child):
    # Assumptions: - node is a valid pointer
    #              - new_child is a valid pointer
    #              - new_child is not the sibling or child of another node
    new_child.parent = node

    if node.children:
        add_sibling(node.children, new_child)
    else:
        node.children = new_child
        new_child.right_sibling = NULL
        new_child.left_sibling = NULL
        node.rank = 1


cdef void add_sibling(FibonacciNode* node, FibonacciNode* new_sibling):
    # Assumptions: - node is a valid pointer
    #              - new_sibling is a valid pointer
    #              - new_sibling is not the child or sibling of another node
    cdef FibonacciNode* temp = rightmost_sibling(node)
    temp.right_sibling = new_sibling
    new_sibling.left_sibling = temp
    new_sibling.right_sibling = NULL
    new_sibling.parent = node.parent
    if new_sibling.parent:
        new_sibling.parent.rank += 1


cdef void remove(FibonacciNode* node):
    # Assumptions: - node is a valid pointer
    if node.parent:
        node.parent.rank -= 1
        if node.left_sibling:
            node.parent.children = node.left_sibling
        elif node.right_sibling:
            node.parent.children = node.right_sibling
        else:
            node.parent.children = NULL

    if node.left_sibling:
        node.left_sibling.right_sibling = node.right_sibling
    if node.right_sibling:
        node.right_sibling.left_sibling = node.left_sibling

    node.left_sibling = NULL
    node.right_sibling = NULL
    node.parent = NULL


######################################################################
# FibonacciHeap structure
#  This structure and operations on it use the FibonacciNode
#  routines to implement a Fibonacci heap

ctypedef FibonacciNode* pFibonacciNode


cdef struct FibonacciHeap:
    FibonacciNode* min_node
    pFibonacciNode[100] roots_by_rank  # maximum number of nodes is ~2^100.


cdef void insert_node(FibonacciHeap* heap,
                      FibonacciNode* node):
    # Assumptions: - heap is a valid pointer
    #              - node is a valid pointer
    #              - node is not the child or sibling of another node
    if heap.min_node:
        add_sibling(heap.min_node, node)
        if node.val < heap.min_node.val:
            heap.min_node = node
    else:
        heap.min_node = node


cdef void decrease_val(FibonacciHeap* heap,
                       FibonacciNode* node,
                       double newval):
    # Assumptions: - heap is a valid pointer
    #              - newval <= node.val
    #              - node is a valid pointer
    #              - node is not the child or sibling of another node
    #              - node is in the heap
    node.val = newval
    if node.parent and (node.parent.val >= newval):
        remove(node)
        insert_node(heap, node)
    elif heap.min_node.val > node.val:
        heap.min_node = node


cdef void link(FibonacciHeap* heap, FibonacciNode* node):
    # Assumptions: - heap is a valid pointer
    #              - node is a valid pointer
    #              - node is already within heap

    cdef FibonacciNode *linknode
    cdef FibonacciNode *parent
    cdef FibonacciNode *child

    if heap.roots_by_rank[node.rank] == NULL:
        heap.roots_by_rank[node.rank] = node
    else:
        linknode = heap.roots_by_rank[node.rank]
        heap.roots_by_rank[node.rank] = NULL

        if node.val < linknode.val or node == heap.min_node:
            remove(linknode)
            add_child(node, linknode)
            link(heap, node)
        else:
            remove(node)
            add_child(linknode, node)
            link(heap, linknode)


cdef FibonacciNode* remove_min(FibonacciHeap* heap):
    # Assumptions: - heap is a valid pointer
    #              - heap.min_node is a valid pointer
    cdef FibonacciNode *temp
    cdef FibonacciNode *temp_right
    cdef FibonacciNode *out
    cdef unsigned int i

    # make all min_node children into root nodes
    if heap.min_node.children:
        temp = leftmost_sibling(heap.min_node.children)
        temp_right = NULL

        while temp:
            temp_right = temp.right_sibling
            remove(temp)
            add_sibling(heap.min_node, temp)
            temp = temp_right

        heap.min_node.children = NULL

    # choose a root node other than min_node
    temp = leftmost_sibling(heap.min_node)
    if temp == heap.min_node:
        if heap.min_node.right_sibling:
            temp = heap.min_node.right_sibling
        else:
            out = heap.min_node
            heap.min_node = NULL
            return out

    # remove min_node, and point heap to the new min
    out = heap.min_node
    remove(heap.min_node)
    heap.min_node = temp

    # re-link the heap
    for i in range(100):
        heap.roots_by_rank[i] = NULL

    while temp:
        if temp.val < heap.min_node.val:
            heap.min_node = temp
        temp_right = temp.right_sibling
        link(heap, temp)
        temp = temp_right

    return out

