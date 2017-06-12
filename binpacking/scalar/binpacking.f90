module binpacking
    contains
    subroutine select_with_prob(prob,i_prob)
        implicit none
        real,intent(in) :: prob(:)
        integer,intent(out) :: i_prob
        real :: rn,cumprob,normalize_factor
        integer :: num_prob

        normalize_factor=sum(prob)
        num_prob=size(prob)
        call random_number(rn)
        cumprob=0
        do i_prob=1,num_prob
            cumprob=cumprob+prob(i_prob)/normalize_factor
            if(cumprob>=rn) then
                exit
            endif
        enddo
    end subroutine select_with_prob

    ! Returns number of bins required using Dot-Product
    ! online algorithm
    subroutine dotproduct(weight, num_items, size_bin, num_bin, dim_vector, assign_table)
        implicit none
        integer,intent(out) :: num_bin
        integer,intent(in) :: num_items, dim_vector
        real,intent(in) :: size_bin(dim_vector)
        real,intent(in) :: weight(num_items,dim_vector)
        integer,intent(out) :: assign_table(num_items)
        real :: av_demand(dim_vector)
        integer :: i,j,best_i,best_item_i,num_unset_items,item_table(num_items),item_i
        real :: rem_j(dim_vector),avrem(dim_vector),cur_dot,best_dot  ! Create an array to store remaining space in bins! there can be at most n bins

        !initialize variables
        num_unset_items=num_items
        item_table=(/(i,i=1,num_items)/)
        av_demand=sum(weight,1)/num_items
     
        ! Place items one by one
        do j=1,num_items
            rem_j=size_bin
            avrem=rem_j*av_demand
            do while(.true.)
                best_i=-1
                best_item_i=-1
                best_dot=0
                ! Find the best item that can accommodate bin(j)
                do i=1,num_unset_items
                    item_i=item_table(i)
                    if (all(rem_j >= weight(item_i,:))) then
                        cur_dot=sum(avrem*weight(item_i,:))
                        if(cur_dot>best_dot) then
                            best_i=i
                            best_item_i=item_i
                            best_dot=cur_dot
                        endif
                    endif
                enddo
         
                if (best_i/=-1) then
                    !assign best_i
                    assign_table(best_item_i)=j-1
                    rem_j = rem_j - weight(best_item_i,:)
                    avrem=rem_j*av_demand

                    !move last item to current position in item_table.
                    item_table(best_i)=item_table(num_unset_items)
                    num_unset_items=num_unset_items-1
                else
                    exit
                endif
            enddo

            !exit condition
            if(num_unset_items==0) then
                exit
            endif
        enddo
        num_bin=j
    end subroutine dotproduct

    ! Returns number of bins required using first fit 
    ! online algorithm
    subroutine firstfit1d(weight, num_items, size_bin, num_bin, dim_vector, assign_table)
        implicit none
        integer,intent(out) :: num_bin
        integer,intent(in) :: num_items, dim_vector
        real,intent(in) :: size_bin(dim_vector)
        real,intent(in) :: weight(num_items,dim_vector)
        integer,intent(out) :: assign_table(num_items)
        integer :: i,j
        real :: bin_rem(num_items,dim_vector)  ! Create an array to store remaining space in bins! there can be at most n bins
        logical :: found

        !initialize variables
        num_bin=0
     
        ! Place items one by one
        do i=1,num_items
            ! Find the first bin that can accommodate
            ! weight(i)
            found=.false.
            do j=1,num_bin
                if (all(bin_rem(j,:) >= weight(i,:))) then
                    bin_rem(j,:) = bin_rem(j,:) - weight(i,:)
                    assign_table(i)=j-1
                    found=.true.
                    exit
                endif
            enddo
     
            ! If no bin could accommodate weight[i]
            if (.not. found) then
                assign_table(i)=num_bin
                num_bin=num_bin+1
                bin_rem(num_bin,:) = size_bin - weight(i,:)
            endif
        enddo
    end subroutine firstfit1d

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

    ! Returns number of bins required using first fit 
    ! binary tree version
    subroutine firstfit_bt(weight, num_items, size_bin, num_bin, assign_table)
        use binary_tree
        implicit none
        integer,intent(out) :: num_bin
        integer,intent(in) :: num_items
        real,intent(in) :: size_bin
        real,intent(in) :: weight(num_items)
        integer,intent(out) :: assign_table(num_items)
        integer :: i,i_bin

        !initialize variables
        num_bin=0
        call init_tree(num_items)  !to store the bins
     
        ! Place items one by one
        do i=1,num_items
            ! Find the first bin that can accommodate weight(i)
            !search the bin
            call search_node_fit(weight(i),i_bin)

            if (i_bin==0) then
                ! If no bin could accommodate weight[i]
                assign_table(i)=num_bin
                num_bin=num_bin+1
                call insert_node(size_bin - weight(i),num_bin)
            else
                assign_table(i)=i_bin-1
                node_data(i_bin)=node_data(i_bin) - weight(i)  !change position of node
                call delete_node(i_bin)
                call insert_node(node_data(i_bin),i_bin)
            endif
            !pause
        enddo
        call free_tree()
    end subroutine firstfit_bt

    !!!!!!!!!!!!!!!!!!!!! Other Algorithms
    ! Returns number of bins required using next fit 
    ! online algorithm
    subroutine nextfit(weight, num_items, size_bin, num_bin, assign_table)
        implicit none
        integer,intent(out) :: num_bin,assign_table(num_items)
        integer,intent(in) :: num_items
        real,intent(in) :: size_bin
        real,intent(in) :: weight(num_items)
        integer :: i
        real :: bin_rem
        
        !initialize variables
        bin_rem=size_bin
        num_bin=1
     
        ! Place items one by one
        do i=1,num_items
            ! If this item can't fit in current bin
            if (weight(i) > bin_rem) then
                num_bin=num_bin+1  ! Use a new bin
                bin_rem = size_bin - weight(i)
            else
                bin_rem = bin_rem - weight(i)
            endif
            assign_table(i)=num_bin-1
        enddo
    end subroutine nextfit

    subroutine nextfit1d(weight, num_items, dim_vector, size_bin, num_bin, assign_table)
        implicit none
        integer,intent(out) :: num_bin,assign_table(num_items)
        integer,intent(in) :: num_items, dim_vector
        real,intent(in) :: size_bin(dim_vector)
        real,intent(in) :: weight(num_items,dim_vector)
        integer :: i
        real :: bin_rem(dim_vector)
        
        !initialize variables
        bin_rem=size_bin
        num_bin=1
     
        ! Place items one by one
        do i=1,num_items
            ! If this item can't fit in current bin
            if (any(weight(i,:) > bin_rem)) then
                num_bin=num_bin+1  ! Use a new bin
                bin_rem = size_bin - weight(i,:)
            else
                bin_rem = bin_rem - weight(i,:)
            endif
            assign_table(i)=num_bin-1
        enddo
    end subroutine nextfit1d

    ! Returns number of bins required using best fit
    ! online algorithm
    subroutine bestfit(weight, num_items, size_bin, num_bin, assign_table)
        implicit none
        integer,intent(out) :: num_bin
        integer,intent(in) :: num_items
        real,intent(in) :: size_bin
        real,intent(in) :: weight(num_items)
        integer,intent(out) :: assign_table(num_items)
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
                assign_table(i)=num_bin-1
            else ! Assign the item to best bin
                bin_rem(bi) = bin_rem(bi) - weight(i)
                assign_table(i)=bi-1
            endif
        enddo
    end subroutine bestfit

    ! Returns number of bins required using best fit
    ! online algorithm
    subroutine bestfit1d(weight, num_items, dim_vector, size_bin, num_bin, assign_table)
        implicit none
        integer,intent(out) :: num_bin
        integer,intent(in) :: num_items,dim_vector
        real,intent(in) :: size_bin(dim_vector)
        real,intent(in) :: weight(num_items,dim_vector)
        integer,intent(out) :: assign_table(num_items)
        integer :: i,j,bi
        real :: bin_rem(num_items,dim_vector),size_min  ! Create an array to store remaining space in bins! there can be at most n bins
        logical :: found
        ! Initialize result (Count of bins)

        num_bin=0
        bin_rem=0
     
        ! Place items one by one
        do i=1,num_items
            ! Find the best bin that can accomodate  weight(i)
            ! Initialize minimum space left and index of best bin
            size_min = sum(size_bin)
            bi = 1
            found=.false.
     
            do j=1,num_bin
                if (all(bin_rem(j,:) >= weight(i,:)) .and. sum(bin_rem(j,:) - weight(i,:)) <= size_min) then
                    bi = j
                    size_min = sum(bin_rem(j,:) - weight(i,:))
                    found=.true.
                endif
            enddo
     
            ! If no bin could accommodate weight[i],
            ! create a new bin
            if (.not. found) then
                num_bin=num_bin+1
                bin_rem(num_bin,:) = size_bin - weight(i,:)
                assign_table(i)=num_bin-1
            else ! Assign the item to best bin
                bin_rem(bi,:) = bin_rem(bi,:) - weight(i,:)
                assign_table(i)=bi-1
            endif
        enddo
    end subroutine bestfit1d
end module binpacking
