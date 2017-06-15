subroutine solve1000(niter=10000)
    '''
    random choice.
    '''
    node_min,node_max,table,p0=get_testcase(sheet)
    problem.init_problem(table,node_min,node_max,p0)
    #cope the index with maximum gradient
    x0=np.zeros(problem.num_path,dtype='int32')
    for i in xrange(niter):
        cost0=problem.get_cost(x0)
        print x0
        pdb.set_trace()
        gradient=problem.compute_gradient(x0)
        pivot=np.argmax(abs(gradient))
        x0[pivot]-=np.sign(gradient[pivot])
        opt_cost=problem.get_cost(x0)
        print opt_cost,cost0,opt_cost-cost0
        if opt_cost<1e-5:
            print 'Find Result!'
            break
        print sum(abs(x0)>0)

    problem.fin_problem()
    pdb.set_trace()
subroutine solve1000(niter=10000)
