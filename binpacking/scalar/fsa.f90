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
    real :: bin_filling(num_bin)
    integer :: opt_config(num_items)
    integer :: i,it,items_exchange(2),m
    real :: cost,delta
    real :: uni01(nms),beta
    !f2py integer,intent(aux) :: num_items

    !initialize filling
    bin_filling=0
    do i=1,num_items
        bin_filling(config(i))=bin_filling(config(i))+weight(i)
    enddo

    opt_config=config
    call get_cost(bin_filling,num_bin,cost)
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
        enddo
    enddo
    config=opt_config
end subroutine anneal_singlerun
 
!Perform Simulated Annealing with multiple runs.
subroutine anneal(nrun,config,num_bin)
    use bpp1d
    use binpacking, only: firstfit
    use qsort_c_module, only: quicksort_ii,quicksort_if,quicksort_fi
    implicit none
    integer,intent(in) :: nrun
    integer,intent(inout) :: num_bin
    integer,intent(inout) :: config(num_items)
    real :: cost
    integer :: config_(num_items)
    integer :: bin_order(num_bin),bin_order_(num_bin)
    real :: bin_filling(num_bin)
    integer :: r,i
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
    !f2py intent(in) :: nrun,num_bin,config
    !f2py intent(out) :: num_bin,config

    do r=1,nrun
        call anneal_singlerun(config,num_bin,cost)
        print*,r,'-th run, cost=',cost

        !!!!detect possible bin merges
        bin_order=(/(i,i=1,num_bin)/)
        bin_order_=(/(i,i=1,num_bin)/)  !the inverse procedure

        !sort bins by fillings in reverse order
        bin_filling=0
        do i=1,num_items
            bin_filling(config(i))=bin_filling(config(i))+weight(i)
        enddo
        bin_filling=-bin_filling
        call quicksort_fi(bin_filling(:num_bin),bin_order(:num_bin))
        call quicksort_ii(bin_order(:num_bin),bin_order_(:num_bin))

        !change the order of weight by new bin-number
        config_=config
        do i=1,num_items
            config_(i)=bin_order_(config(i))
        enddo
        call quicksort_if(config_,weight)

        !next fit to group bins to get new assign table
        call firstfit(weight, num_items, size_bin, num_bin, config)
        config=config+1

        bin_filling=0
        do i=1,num_items
            bin_filling(config(i))=bin_filling(config(i))+weight(i)
        enddo

        !delete redundant bins
        num_bin=1
        do i=1,num_items
            num_bin=max(num_bin,config(i))
        enddo
        print*,'num_bin =',num_bin
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
    call init_problem((/2,5,4,7,1,3,8/)*1.0,10,(/(10.2-i*0.2,i=1,48)/),4000)
    print*,'Initialized problem!'
    print*,'weight=',weight
    print*,'num_items=',num_items
    !print*,'tempscales=',tempscales
    call init_random_seed(2)
    opt_config=(/1,1,2,3,3,4,5/)  !initial_config
    call anneal(3,opt_config,num_bin)
end subroutine test
