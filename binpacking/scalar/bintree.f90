module binary_tree
    implicit none
    integer :: space_nodes,i_root=0,num_nodes=0
    integer,allocatable :: left(:),right(:),parent(:)
    real,allocatable :: node_data(:)
    logical,allocatable :: used_mask(:)
contains
    subroutine init_tree(space_nodes_)
        implicit none
        integer,intent(in) :: space_nodes_
        space_nodes=space_nodes_
        allocate(left(space_nodes),right(space_nodes),node_data(space_nodes), &
            parent(space_nodes),used_mask(space_nodes))
        left=0
        right=0
        parent=0
        used_mask=.false.
    end subroutine init_tree

    subroutine free_tree()
        implicit none
        i_root=0
        num_nodes=0
        deallocate(left,right,parent,node_data,used_mask)
    end subroutine free_tree

    subroutine insert_node(node,pos_node)
        implicit none
        real,intent(in) :: node
        integer,intent(in),optional :: pos_node
        integer :: i_node,counter,pos

        !check position
        if(present(pos_node)) then
            pos=pos_node
        else
            pos=num_nodes+1
        endif
        if(pos>space_nodes .or. pos<=0) then
            print*,'Error: insert node at position out of memory.'
            stop
        endif
        if(used_mask(pos)) then
            print*,'Error: insert node at occupied position.'
            stop
        endif
        used_mask(pos)=.true.
        num_nodes=num_nodes+1
        node_data(pos)=node

        if(num_nodes==1) then
            node_data(pos)=node
            i_root=pos
            return
        endif

        i_node=i_root  !i_node -> its parent
        counter=0
        do while(.true.)
            counter=counter+1
            if(node_data(i_node)>node) then !search left
                if(left(i_node)==0) then !but no left
                    left(i_node)=pos  !make this node its left
                    parent(pos)=i_node
                    return
                else
                    i_node=left(i_node)
                endif
            else   !search right
                if(right(i_node)==0) then !but no right
                    right(i_node)=pos  !make this node its left
                    parent(pos)=i_node
                    return
                else
                    i_node=right(i_node)
                endif
            endif
        enddo
    end subroutine insert_node

    !find the minimum node_out >= node
    subroutine search_node_fit(node,i_node_out)
        implicit none
        real,intent(in) :: node
        integer,intent(out) :: i_node_out
        real :: data_temp
        integer :: i_node

        i_node=i_root
        i_node_out=0
        if(num_nodes<1) return
        do while(.true.)
            data_temp=node_data(i_node)
            !find the exact bin
            if(data_temp==node) then
                i_node_out=i_node
                return
            else if(data_temp>node) then !search left
                if(left(i_node)==0) then !but no left
                    i_node_out=i_node
                    return
                else
                    if(i_node_out==0) then
                        i_node_out=i_node
                    else if(data_temp<=node_data(i_node_out)) then
                        i_node_out=i_node
                    endif
                    i_node=left(i_node)
                endif
            else   !search right
                if(right(i_node)==0) then !but no right
                    return
                else
                    i_node=right(i_node)
                endif
            endif
        enddo
    end subroutine search_node_fit

    subroutine delete_node(i_node)
        implicit none
        integer,intent(in) :: i_node
        integer :: i_y,i_p,i_p_y
        logical :: direct_sibling

        if(i_node>space_nodes .or. i_node<=0 .or. .not. used_mask(i_node)) then
            print*,'Error: remove an unused node.'
            stop
        endif

        !find the node i_y that can replace i_node
        direct_sibling=.true.
        if(left(i_node)==0) then
            i_y=right(i_node)
        else if(right(i_node)==0) then
            i_y=left(i_node)
        else
            i_y=left(i_node)
            do while(right(i_y)/=0)
                i_y=right(i_y)
                direct_sibling=.false.
            enddo
        endif

        !change to left/right sibling for parent to y
        i_p=parent(i_node)
        if(i_p==0) then 
            i_root=i_y
        else if(left(i_p)==i_node) then
            left(i_p)=i_y
        else if(right(i_p)==i_node) then
            right(i_p)=i_y
        endif

        !print*,'use',i_y
        if(i_y/=0 .and. .not. direct_sibling) then
            !change left/right sibling for parent of y to those of y
            i_p_y=parent(i_y)
            if(i_p_y/=0) then 
                if(right(i_p_y)==i_y) then
                    if(left(i_y)/=0) then
                        right(i_p_y)=left(i_y)
                        parent(right(i_p_y))=i_p_y
                    else if(right(i_y)/=0) then
                        right(i_p_y)=right(i_y)
                        parent(right(i_p_y))=i_p_y
                    else
                        right(i_p_y)=0
                    endif
                else
                    if(left(i_y)/=0) then
                        left(i_p_y)=left(i_y)
                        parent(left(i_p_y))=i_p_y
                    else if(right(i_y)/=0) then
                        left(i_p_y)=right(i_y)
                        parent(left(i_p_y))=i_p_y
                    else
                        left(i_p_y)=0
                    endif
                endif
            endif
            parent(i_y)=i_p

            !change add the siblings to i_y
            left(i_y)=left(i_node)
            right(i_y)=right(i_node)
            if(left(i_node)/=0) parent(left(i_node))=i_y
            if(right(i_node)/=0) parent(right(i_node))=i_y
        else if(i_y/=0) then
            parent(i_y)=i_p
            if(left(i_node)==i_y .and. right(i_node)/=0) then
                right(i_y)=right(i_node)
                parent(right(i_y))=i_y
            endif
        endif

        num_nodes=num_nodes-1
        !clear data
        used_mask(i_node)=.false.
        parent(i_node)=0
        left(i_node)=0
        right(i_node)=0
    end subroutine delete_node

    subroutine print_tree()
        implicit none
        integer :: i
        !character :: str_node(1000)
        10 format(' ',10F6.3)
        12 format(' ',A6)
        15 format(' ',I6)
        20 format('  ',A)
        print*,'Tree =>',i_root
        write(*,20,advance='no'),'_ID_='
        do i=1,space_nodes
            if(used_mask(i)) write(*,15,advance='no') i
        enddo
        print*,''
        write(*,20,advance='no'),'Data='
        do i=1,space_nodes
            if(used_mask(i)) write(*,10,advance='no') node_data(i)
        enddo
        print*,''
        write(*,20,advance='no'),'Left='
        do i=1,space_nodes
            if(used_mask(i)) then
                if(left(i)>0 .and. used_mask(left(i))) then
                    write(*,15,advance='no') left(i)
                    !write(*,10,advance='no') node_data(left(i))
                else 
                    write(*,12,advance='no') '-'
                endif
            endif
        enddo
        print*,''
        write(*,20,advance='no'),'Rght='
        do i=1,space_nodes
            if(used_mask(i)) then
                if(right(i)>0 .and. used_mask(right(i))) then
                    write(*,15,advance='no') right(i)
                    !write(*,10,advance='no') node_data(right(i))
                else 
                    write(*,12,advance='no') '-'
                endif
            endif
        enddo
        print*,''
        write(*,20,advance='no'),'Prnt='
        do i=1,space_nodes
            if(used_mask(i)) then
                if(parent(i)>0 .and. used_mask(parent(i))) then
                    write(*,15,advance='no') parent(i)
                    !write(*,10,advance='no') node_data(parent(i))
                else 
                    write(*,12,advance='no') '-'
                endif
            endif
        enddo
        print*,''
    end subroutine print_tree

    subroutine check_validity()
        implicit none
        integer :: i,depth(space_nodes)
        do i=1,space_nodes
            if(used_mask(i)) then
                !check left and right
                if(left(i)/=0) then
                    if(left(i)==i) then
                        call print_tree()
                        print*,'Cycle detected!',i
                        read(*,*)
                    else if(.not. used_mask(left(i))) then
                        call print_tree()
                        print*,'Pointing to null space!',i
                        read(*,*)
                    else if(node_data(left(i))>node_data(i)) then
                        call print_tree()
                        print*,'Left branch greater!',i
                        read(*,*)
                    endif
                    !check consistancy
                    if(parent(left(i))/=i) then
                        call print_tree()
                        print*,'Inconsistant left sibling!',i
                        read(*,*)
                    endif
                endif

                if(right(i)/=0) then
                    if(right(i)==i) then
                        call print_tree()
                        print*,'Cycle detected!',i
                        read(*,*)
                    else if(.not. used_mask(right(i))) then
                        call print_tree()
                        print*,'Pointing to null space!',i
                        read(*,*)
                    else if(node_data(right(i))<node_data(i)) then
                        call print_tree()
                        print*,'Right branch smaller!',i
                        read(*,*)
                    endif
                    !check consistancy
                    if(parent(right(i))/=i) then
                        call print_tree()
                        print*,'Inconsistant right sibling!',i
                        read(*,*)
                    endif
                endif
            endif
        enddo

        !check cycles
        depth=0
        call get_depth(depth,i_root,1)
        if(any(depth==0 .and. used_mask)) then
            call print_tree()
            print*,'Disconnected Graph!'
            read(*,*)
        endif
    end subroutine check_validity

    recursive subroutine get_depth(depth,i_node,i_depth)
        implicit none
        integer,intent(inout) :: depth(:)
        integer,intent(in) :: i_node,i_depth
        if((i_node)==0) return
        if(depth(i_node)/=0) then
            call print_tree()
            print*,'Cycle detected!'
            read(*,*)
        else
            depth(i_node)=i_depth
        endif
        call get_depth(depth,left(i_node),i_depth+1)
        call get_depth(depth,right(i_node),i_depth+1)
    end subroutine get_depth
end module binary_tree


program main
    use binary_tree
    implicit none
    integer :: res,i,i_node
    integer,parameter :: space_tree=6
    real :: dat(space_tree)

    call init_tree(space_tree*2)
    open(11,file='sample.dat')
    do i=1,space_tree
        read(11,*) i_node,dat(i)
        call insert_node(dat(i))
    enddo
    close(11)

    call print_tree()

    call search_node_fit(1.5,res)
    print*,'1.5->',res !print 4
    call search_node_fit(1.4,res)
    print*,'1.4->',res !print 4
    call search_node_fit(1.6,res)
    print*,'1.6->',res !print 2
    call search_node_fit(3.6,res)
    print*,'3.6->',res !print 0

    print*,'Test Delete Node 6'
    call delete_node(6)
    call print_tree()
    print*,'Insert Node 6 Back'
    call insert_node(1.25,6)
    call print_tree()

    print*,'Test Delete Node 4'
    call delete_node(4)
    call print_tree()
    print*,'Insert Node 4 Back'
    call insert_node(1.5,4)
    call print_tree()
    print*,'Test Delete Node 2'
    call delete_node(2)
    call print_tree()
    print*,'Insert Node 2 Back to 7'
    call insert_node(2.0,7)
    call print_tree()
end program main
