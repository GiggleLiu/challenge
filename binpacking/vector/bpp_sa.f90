module bpp1d
    integer :: num_items, num_tempscales, nms, dim_vector
    real,allocatable :: tempscales(:),weight(:,:)
    real,allocatable :: size_bin(:)
    !f2py num_items,size_bin,num_tempscales,nms,timescale,weight

    contains
    subroutine init_problem(weight_,size_bin_,tempscales_,nms_)
        implicit none
        integer,intent(in) :: size_bin_(:), nms_
        real,intent(in) :: tempscales_(:),weight_(:,:)
        num_items=size(weight_,1)
        dim_vector=size(weight_,2)
        num_tempscales=size(tempscales_)
        if (.not. allocated(weight)) allocate (weight(num_items,dim_vector))
        if (.not. allocated(tempscales)) allocate (tempscales(num_tempscales))
        if (.not. allocated(size_bin)) allocate (size_bin(dim_vector))
        weight=weight_
        size_bin=size_bin_
        tempscales=tempscales_
        nms=nms_
    end subroutine init_problem

    subroutine get_cost(bin_filling,num_bin,cost)
        implicit none
        integer,intent(in) :: num_bin
        real,intent(in) :: bin_filling(num_bin,dim_vector)
        real,intent(out) :: cost
        !f2py integer,intent(aux) :: dim_vector
        !cost=-sum(sum(spread(size_bin,1,num_bin)-bin_filling,2)**2)
        cost=-sum(product(bin_filling,2)**2)
    end subroutine get_cost

    subroutine propose(config,bin_filling,num_bin,items_exchange,delta)
        implicit none
        integer,intent(in) :: num_bin,config(num_bin)
        real,intent(in) :: bin_filling(num_bin,dim_vector)
        integer,intent(out) :: items_exchange(2)
        real,intent(out) :: delta
        real :: rn(2)
        real,dimension(dim_vector) :: filling_1,filling_2,filling_1_new,filling_2_new,weight_diff
        integer :: i,item1,item2,bin1,bin2,j
        logical :: found
        !f2py integer,intent(aux) :: dim_vector

        found=.false.
        loop1:do i=1,num_items**2
            call random_number(rn)
            items_exchange = floor(num_items*rn)+1
            item1=items_exchange(1)
            item2=items_exchange(2)
            bin1=config(item1)
            bin2=config(item2)
            filling_1 = bin_filling(bin1,:)
            filling_2 = bin_filling(bin2,:)
            weight_diff=weight(item2,:)-weight(item1,:)
            filling_1_new = filling_1+weight_diff
            filling_2_new = filling_2-weight_diff
            if(bin1/=bin2) then
                do j=1,dim_vector
                    if(filling_1_new(j)>size_bin(j)) then
                        cycle loop1
                    else if(filling_2_new(j)>size_bin(j)) then
                        cycle loop1
                    endif
                enddo
                if(any(abs(filling_1_new-filling_1)>1D-8)) then
                    !find valid update
                    found=.true.
                    delta=-product(filling_1_new,1)**2-product(filling_2_new)**2 &
                        +product(filling_1)**2+product(filling_2)**2
                    exit loop1
                endif
            endif
            !if(bin1/=bin2 .and. any(abs(filling_1_new-filling_1)>1D-8) &
            !    .and. all(filling_1_new<=size_bin) .and. all(filling_2_new<=size_bin)) then
            !    !find valid update
            !    found=.true.
            !    delta=-product(filling_1_new,1)**2-product(filling_2_new)**2 &
            !        +product(filling_1)**2+product(filling_2)**2
            !    exit
            !endif
        enddo loop1
        if(.not. found) then
            items_exchange=0
        endif
    end subroutine propose

    subroutine accept(items_exchange,config,bin_filling,num_bin)
        implicit none
        integer,intent(inout) :: config(num_items)
        real,intent(inout) :: bin_filling(num_bin,dim_vector)
        integer,intent(in) :: items_exchange(2),num_bin
        integer :: atom1,atom2,bin1,bin2
        !f2py integer,intent(aux) :: num_items
        !f2py integer,intent(aux) :: dim_vector

        atom1=items_exchange(1)
        atom2=items_exchange(2)
        bin1=config(atom1)
        bin2=config(atom2)

        !exchange config
        config(atom1)=bin2
        config(atom2)=bin1

        !update filling
        bin_filling(bin1,:)=bin_filling(bin1,:)-weight(atom1,:)+weight(atom2,:)
        bin_filling(bin2,:)=bin_filling(bin2,:)-weight(atom2,:)+weight(atom1,:)
    end subroutine accept
end module bpp1d
