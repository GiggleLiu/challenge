! initialize a random seed from the system clock at every run (fortran 95 code)
subroutine init_random_seed()
    INTEGER :: i, n, clock
    INTEGER, DIMENSION(:), ALLOCATABLE :: seed

    CALL RANDOM_SEED(size = n)
    ALLOCATE(seed(n))
    CALL SYSTEM_CLOCK(COUNT=clock)
    seed = clock + 37 * (/ (i - 1, i = 1, n) /)
    CALL RANDOM_SEED(PUT = seed)
    DEALLOCATE(seed)
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
subroutine anneal_singlerun(config,bin_filling,num_bin,opt_cost,opt_config)
    use bpp1d
    implicit none
    integer,intent(in) :: num_bin
    integer,intent(inout) :: config(num_items)
    real,intent(inout) :: bin_filling(num_bin)
    integer,intent(out) :: opt_config(num_items)
    real,intent(out) :: opt_cost
    integer :: it,items_exchange(2),m
    real :: cost,delta
    real :: uni01(nms),beta
    !f2py integer,intent(aux) :: num_items

    opt_config=config
    call get_cost(bin_filling,num_bin,cost)
    opt_cost=cost

    do it=1,num_tempscales
        beta=1/tempscales(it)
        call random_number(uni01)
        do m=1,nms
            call propose(config,bin_filling,num_bin,items_exchange,delta)
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
end subroutine anneal_singlerun
 
!Perform Simulated Annealing with multiple runs.
subroutine anneal(nrun,initial_config,num_bin)
    use bpp1d
    implicit none
    integer,intent(in) :: nrun,num_bin
    integer,intent(inout) :: initial_config(num_items)
    real :: cost,opt_cost
    integer :: config(num_items),opt_config(num_items)
    real :: initial_filling(num_bin)
    integer :: r,i
    interface
        subroutine anneal_singlerun(config,bin_filling,num_bin,opt_cost,opt_config)
            use bpp1d
            implicit none
            integer,intent(in) :: num_bin
            integer,intent(inout) :: config(num_items)
            real,intent(inout) :: bin_filling(num_bin)
            integer,intent(out) :: opt_config(num_items)
            real,intent(out) :: opt_cost
        end subroutine anneal_singlerun
    end interface
    !f2py integer,intent(aux) :: num_items

    opt_cost=999999
    initial_filling=0
    do i=1,num_items
        initial_filling(initial_config(i))=initial_filling(initial_config(i))+weight(i)
    enddo
    do r=1,nrun
        call anneal_singlerun(initial_config,initial_filling,num_bin,cost,config)
        if(cost<opt_cost) then
            opt_cost=cost
            opt_config=config
        endif
        print*,r,'-th run, cost=',cost
    enddo
end subroutine anneal

subroutine test()
    use bpp1d
    implicit none
    integer :: i
    interface
        subroutine anneal(nrun,initial_config,num_bin)
            use bpp1d
            implicit none
            integer,intent(in) :: nrun,num_bin
            integer,intent(in) :: initial_config(num_items)
        end subroutine anneal
    end interface
    call init_problem((/2,5,4,7,1,3,8/)*1.0,10,(/(10-i*0.2,i=1,48)/),4000)
    call init_random_seed()
    call anneal(1,(/1,1,2,3,3,4,5/),5)
end subroutine test

program main
    call test()
end program main
