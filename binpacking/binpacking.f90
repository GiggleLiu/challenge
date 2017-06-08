! Returns number of bins required using first fit 
! online algorithm
subroutine firstfit(weight, num_items, size_bin, num_bin, assign_table)
    implicit none
    integer,intent(out) :: num_bin
    integer,intent(in) :: num_items
    real,intent(in) :: size_bin
    real,intent(in) :: weight(num_items)
    integer,intent(out) :: assign_table(num_items)
    integer :: i,j
    real :: bin_rem(num_items)  ! Create an array to store remaining space in bins! there can be at most n bins
    logical :: found

    !initialize variables
    num_bin=0
 
    ! Place items one by one
    do i=1,num_items
        ! Find the first bin that can accommodate
        ! weight(i)
        found=.false.
        do j=1,num_bin
            if (bin_rem(j) >= weight(i)) then
                bin_rem(j) = bin_rem(j) - weight(i)
                assign_table(i)=j-1
                found=.true.
                exit
            endif
        enddo
 
        ! If no bin could accommodate weight[i]
        if (.not. found) then
            assign_table(i)=num_bin
            num_bin=num_bin+1
            bin_rem(num_bin) = size_bin - weight(i)
        endif
    enddo
end subroutine firstfit

!!!!!!!!!!!!!!!!!!!!! Other Algorithms
! Returns number of bins required using next fit 
! online algorithm
subroutine nextfit(weight, num_items, size_bin, num_bin)
    implicit none
    integer,intent(out) :: num_bin
    integer,intent(in) :: num_items
    real,intent(in) :: size_bin
    real,intent(in) :: weight(num_items)
    integer :: i
    real :: bin_rem
    
    !initialize variables
    bin_rem=size_bin
    num_bin=0
 
    ! Place items one by one
    do i=1,num_items
        ! If this item can't fit in current bin
        if (weight(i) > bin_rem) then
            num_bin=num_bin+1  ! Use a new bin
            bin_rem = size_bin - weight(i)
        else
            bin_rem = bin_rem - weight(i)
        endif
    enddo
end subroutine nextfit

! Returns number of bins required using best fit
! online algorithm
subroutine bestfit(weight, num_items, size_bin, num_bin)
    implicit none
    integer,intent(out) :: num_bin
    integer,intent(in) :: num_items
    real,intent(in) :: size_bin
    real,intent(in) :: weight(num_items)
    integer :: i,j,bi
    real :: bin_rem(num_items),size_min  ! Create an array to store remaining space in bins! there can be at most n bins
    ! Initialize result (Count of bins)

    num_bin=0
    bin_rem=0
 
    ! Place items one by one
    do i=1,num_items
        ! Find the best bin that can accomodate  weight(i)
        ! Initialize minimum space left and index of best bin
        size_min = size_bin
        bi = 1
 
        do j=1,num_bin
            if (bin_rem(j) >= weight(i) .and. bin_rem(j) - weight(i) <= size_min) then
                bi = j
                size_min = bin_rem(j) - weight(i)
            endif
        enddo
 
        ! If no bin could accommodate weight[i],
        ! create a new bin
        if (size_min==size_bin) then
            num_bin=num_bin+1
            bin_rem(num_bin) = size_bin - weight(i)
        else ! Assign the item to best bin
            bin_rem(bi) = bin_rem(bi) - weight(i)
        endif
    enddo
end subroutine bestfit
