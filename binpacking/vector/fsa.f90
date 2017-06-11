! initialize a random seed from the system clock at every run (fortran 95 code)
subroutine init_random_seed(const_seed)
    INTEGER,INTENT(IN) :: const_seed
    INTEGER :: i, n, clock
    INTEGER, DIMENSION(:), ALLOCATABLE :: seed

    CALL RANDOM_SEED(size = n)
    ALLOCATE(seed(n))
    IF(const_seed==-1) then
        CALL SYSTEM_CLOCK(COUNT=clock)
        seed = clock + 37 * (/ (i - 1, i = 1, n) /)
        CALL RANDOM_SEED(PUT = seed)
        DEALLOCATE(seed)
    ELSE
        seed=const_seed
        CALL RANDOM_SEED(PUT = seed)
        DEALLOCATE(seed)
    ENDIF
end subroutine init_random_seed

!Perform Simulated Annealing using Metropolis updates for the single run.
!
!Parameters:
!    :ann: <SAP>, the app.
!    :initial_config: config,
!    :tempscales: 1D array, the time scale from high temperature to low temperature.
!
!Return:
!    (minimum cost, optimal configuration)
subroutine anneal_singlerun(config,num_bin,opt_cost)
    use bpp1d
    implicit none
    integer,intent(in) :: num_bin
    integer,intent(inout) :: config(num_items)
    real,intent(out) :: opt_cost
    real :: bin_filling(num_bin,dim_vector)
    integer :: opt_config(num_items)
    integer :: i,it,items_exchange(2),m
    real :: cost,delta
    real :: uni01(nms),beta
    !f2py integer,intent(aux) :: num_items
    !f2py integer,intent(aux) :: dim_vector

    !initialize filling
    bin_filling=0
    do i=1,num_items
        bin_filling(config(i),:)=bin_filling(config(i),:)+weight(i,:)
    enddo

    opt_config=config
    call get_cost(bin_filling,num_bin,cost)
    print*,'initial cost=',cost
    opt_cost=cost

    do it=1,num_tempscales
        beta=1/tempscales(it)
        call random_number(uni01)
        !print*,'T=',1/beta
        !print*,'cost=',cost
        !print*,'filling=',bin_filling
        do m=1,nms
            call propose(config,bin_filling,num_bin,items_exchange,delta)
            if(items_exchange(1)==0) then
                print*,'Can not Move!'
                return
            endif
            if(exp(-beta*delta)>uni01(m)) then  !accept
                call accept(items_exchange,config,bin_filling,num_bin)
                cost=cost+delta
                if(cost<opt_cost) then
                    opt_cost=cost
                    opt_config=config
                endif
            endif
            !print*,'cost=',cost,' delta=',delta,' prob=',exp(-beta*delta)
            !pause
        enddo
    enddo
    config=opt_config
    print*,'final cost=',cost
end subroutine anneal_singlerun
 
!Perform Simulated Annealing with multiple runs.
subroutine anneal(nrun,config,num_bin)
    use bpp1d
    use binpacking, only: dotproduct_redistribute
    use qsort_c_module, only: quicksort_ii,quicksort_if,quicksort_fi
    implicit none
    integer,intent(in) :: nrun
    integer,intent(inout) :: num_bin
    integer,intent(inout) :: config(num_items)
    real :: cost
    integer :: unset_items(num_items),unset_assign(num_items),num_unset_items
    real :: cost_bins(num_bin),size_rem(num_bin,dim_vector),unset_weight(num_items,dim_vector)
    integer :: r,i,min_bin
    logical :: less_bin
    interface
        subroutine anneal_singlerun(config,num_bin,opt_cost)
            use bpp1d
            implicit none
            integer,intent(in) :: num_bin
            integer,intent(inout) :: config(num_items)
            real,intent(out) :: opt_cost
        end subroutine anneal_singlerun
    end interface
    !f2py integer,intent(aux) :: num_items
    !f2py integer,intent(aux) :: dim_vector
    !f2py intent(in) :: nrun,num_bin,config
    !f2py intent(out) :: num_bin,config

    do r=1,nrun
        call anneal_singlerun(config,num_bin,cost)
        print*,r,'-th run, cost=',cost

        !find the smallest bin, put it to the end.
        size_rem(:num_bin,:)=spread(size_bin,1,num_bin)
        do i=1,num_items
            size_rem(config(i),:)=size_rem(config(i),:)-weight(i,:)
        enddo
        cost_bins(:num_bin)=sum(size_rem(:num_bin,:),2)
        min_bin=maxloc(cost_bins(:num_bin),1)

        !swap min_bin and num_bin in config, and make the smallest num_bin empty
        !initialize num_unset_items, unset_weight, unset_items
        num_unset_items=0
        do i=1,num_items
            if(config(i)==min_bin) then
                config(i)=num_bin
                num_unset_items=num_unset_items+1
                unset_items(num_unset_items)=i
                unset_weight(num_unset_items,:)=weight(i,:)
            else if(config(i)==num_bin) then
                config(i)=min_bin
            endif
        enddo

        !initialize size_rem
        size_rem(min_bin,:)=size_rem(num_bin,:)
        size_rem(num_bin,:)=size_bin

        call dotproduct_redistribute(unset_weight(:num_unset_items,:), num_unset_items, size_rem(:num_bin,:), dim_vector, &
            unset_assign(:num_unset_items))

        !change config
        less_bin=all(unset_assign+1/=num_bin)
        do i=1,num_unset_items
            config(unset_items(i))=unset_assign(i)+1
        enddo

        !delete redundant bins
        if(less_bin) then
            num_bin=num_bin-1
        endif
        print*,'num_bin=',num_bin
    enddo
end subroutine anneal

subroutine test()
    use bpp1d
    implicit none
    integer,parameter :: num_items_=7
    integer :: i,num_bin
    integer :: opt_config(num_items_)
    interface
        subroutine anneal(nrun,config,num_bin)
            use bpp1d
            implicit none
            integer,intent(in) :: nrun
            integer,intent(inout) :: num_bin
            integer,intent(inout) :: config(num_items)
        end subroutine anneal
    end interface
    !f2py integer,intent(aux) :: num_items
    num_bin=5
    call init_problem(reshape((/2,5,4,7,1,3,8/)*1.0,(/7,1/)),(/10/),(/(10.2-i*0.2,i=1,48)/),4000)
    print*,'Initialized problem!'
    print*,'weight=',weight
    print*,'num_items=',num_items
    !print*,'tempscales=',tempscales
    call init_random_seed(2)
    opt_config=(/1,1,2,3,3,4,5/)  !initial_config
    call anneal(5,opt_config,num_bin)
end subroutine test

program main
    call test()
end program main
