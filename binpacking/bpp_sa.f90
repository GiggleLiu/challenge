module bpp1d
    integer :: num_items, size_bin, num_tempscales, nms
    real,allocatable :: tempscales(:),weight(:)

    !f2py num_items,size_bin,num_tempscales,nms,timescale,weight

    contains
    subroutine init_problem(weight_,size_bin_,tempscales_,nms_)
        implicit none
        integer,intent(in) :: size_bin_, nms_
        real,intent(in) :: tempscales_(:),weight_(:)
        num_items=size(weight_)
        num_tempscales=size(tempscales_)
        if (.not. allocated(weight)) allocate (weight(num_items))
        if (.not. allocated(tempscales)) allocate (tempscales(num_tempscales))
        weight=weight_
        size_bin=size_bin_
        tempscales=tempscales_
        nms=nms_
    end subroutine init_problem

    subroutine get_cost(bin_filling,num_bin,cost)
        implicit none
        integer,intent(in) :: num_bin
        real,intent(in) :: bin_filling(num_bin)
        real,intent(out) :: cost
        cost=-sum(bin_filling**2)
    end subroutine get_cost

    subroutine propose(config,bin_filling,num_bin,items_exchange,delta)
        implicit none
        integer,parameter :: num_try=100
        integer,intent(in) :: num_bin,config(num_bin)
        real,intent(in) :: bin_filling(num_bin)
        integer,intent(out) :: items_exchange(2)
        real,intent(out) :: delta
        real :: rn(2),filling_1,filling_2,filling_1_new,filling_2_new,weight_diff
        integer :: i,item1,item2
        logical :: found

        found=.false.
        do i=1,num_try
            call random_number(rn)
            items_exchange = floor(num_items*rn)+1
            item1=items_exchange(1)
            item2=items_exchange(2)
            filling_1 = bin_filling(config(item1))
            filling_2 = bin_filling(config(item2))
            weight_diff=weight(item2)-weight(item1)
            filling_1_new = filling_1+weight_diff
            filling_2_new = filling_2-weight_diff
            if(abs(filling_1_new-filling_1)>1D-14 .and. filling_1_new<=size_bin .and. filling_2_new<=size_bin) then
                !find valid update
                found=.true.
                delta=-filling_1_new**2-filling_2_new**2+filling_1**2+filling_2**2
                exit
            endif
        enddo
        if(.not. found) then
            items_exchange=0
        endif
    end subroutine propose

    subroutine accept(items_exchange,config,bin_filling,num_bin)
        implicit none
        integer,intent(inout) :: config(:)
        real,intent(inout) :: bin_filling(num_bin)
        integer,intent(in) :: items_exchange(2),num_bin
        integer :: atom1,atom2,bin1,bin2

        atom1=items_exchange(1)
        atom2=items_exchange(2)
        bin1=config(atom1)
        bin2=config(atom2)

        !exchange config
        config(atom1)=bin2
        config(atom2)=bin1

        !update filling
        bin_filling(bin1)=bin_filling(bin1)-weight(atom1)+weight(atom2)
        bin_filling(bin2)=bin_filling(bin2)-weight(atom2)+weight(atom1)
    end subroutine accept
end module bpp1d
