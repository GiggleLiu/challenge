!http://blog.csdn.net/v_july_v/article/details/6105630
module binary_tree
    implicit none
    integer :: num_nodes,space_nodes,i_root=1
    integer,allocatable :: left(:),right(:),parent(:)
    logical,allocatable :: color(:)
    real,allocatable :: node_data(:)
contains
    subroutine init_tree(space_nodes)
        implicit none
        integer,intent(in) :: space_nodes
        allocate(left(space_nodes),right(space_nodes),node_data(space_nodes), &
            parent(space_nodes),color(space_nodes))
        left=0
        right=0
        parent=0
        color=.false. !black
    end subroutine init_tree

    subroutine leftroate(i_x)  !pivot x
        i_y=right(i_x)
        right(i_x)=left(i_y)
        if(left(i_y)/=0) then
            parent(left(i_y))=i_x
        parent(i_y)=parent(i_x)
        if(parent(i_x)==0) then 
            i_root=i_y  
        else if(i_x==left(parent(i_x)) then
            left(parent(i_x))=i_y
        else
            right(parent(i_x))=i_y  
        left(i_y)=i_x
        parent(i_x)=i_y
    subroutine leftroate

    subroutine rightroate(i_x)  !pivot x
        i_y=left(i_x)
        left(i_x)=right(i_y)
        if(right(i_y)/=0) then
            parent(right(i_y))=i_x
        parent(i_y)=parent(i_x)
        if(parent(i_x)==0) then 
            i_root=i_y  
        else if(i_x==left(parent(i_x)) then
            left(parent(i_x))=i_y
        else
            right(parent(i_x))=i_y  
        right(i_y)=i_x
        parent(i_x)=i_y
    subroutine rightroate

    subroutine insert_node(node)
        implicit none
        real,intent(in) :: node
        integer :: i_node,counter
        logical :: find_pos
        num_nodes=num_nodes+1
        node_data(num_nodes)=node

        if(num_nodes==1) then
            node_data(1)=node
            return
        endif

        i_node=1
        find_pos=.false.
        counter=0
        do while(.not. find_pos)
            counter=counter+1
            if(node_data(i_node)>node) then !search left
                if(left(i_node)==0) then !but no left
                    print*,'counter=',counter
                    find_pos=.true.
                    left(i_node)=num_nodes  !make this node its left
                    parent(num_nodes)=i_node
                    color(num_nodes)=.true.
                else
                    i_node=left(i_node)
                endif
            else   !search right
                if(right(i_node)==0) then !but no right
                    print*,'counter=',counter
                    find_pos=.true.
                    right(i_node)=num_nodes  !make this node its left
                    parent(num_nodes)=i_node
                    color(num_nodes)=.true.
                else
                    i_node=right(i_node)
                endif
            endif
        enddo
        !Fix Color
        i_node=num_nodes
        do while(color(parent(i_nodes)))
            if(parent(i_node)==left(parent(parent(i_node)))) then
                i_y=right(parent(parent(i_node)))
                if(color(i_y)) then
                    color(parent(i_node))=.false.
                    color(i_y)=.false.
                    color(parent(parent(i_node)))=.true.
                    i_node=parent(parent(i_node))
                else if(i_node == right(parent(i_node))) then
                    i_node=parent(i_node)
                    leftrotate(i_node)
                endif
                color(parent(i_node))=.false.
                color(parent(parent(i_node)))=.true.
                rightrotate(parent(parent(i_node)))
            else
                i_y=left(parent(parent(i_node)))
                if(color(i_y)) then
                    color(parent(i_node))=.false.
                    color(i_y)=.false.
                    color(parent(parent(i_node)))=.true.
                    i_node=parent(parent(i_node))
                else if(i_node == left(parent(i_node))) then
                    i_node=parent(i_node)
                    rightrotate(i_node)
                endif
                color(parent(i_node))=.false.
                color(parent(parent(i_node)))=.true.
                leftrotate(parent(parent(i_node)))
            endif
        enddo
        color(i_root)=.false.
    end subroutine insert_node

    !find the minimum node_out >= node
    subroutine search_node_fit(node,i_node_out)
        implicit none
        real,intent(in) :: node
        integer,intent(out) :: i_node_out
        real :: data_temp
        integer :: i_node
        logical :: find_pos

        i_node=1
        i_node_out=0
        find_pos=.false.
        do while(.not. find_pos)
            data_temp=node_data(i_node)
            if(data_temp==node) then
                find_pos=.true.
                i_node_out=i_node
            else if(data_temp>node) then !search left
                if(left(i_node)==0) then !but no left
                    find_pos=.true.
                    i_node_out=i_node
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
                    find_pos=.true.
                else
                    i_node=right(i_node)
                endif
            endif
        enddo
    end subroutine search_node_fit
end module binary_tree

program main
    use binary_tree
    implicit none
    integer :: res

    call init_tree(4)
    call insert_node(1.0)
    call insert_node(2.0)
    call insert_node(0.5)
    call insert_node(1.5)

    print*,'Data=',node_data
    print*,'Left=',left
    print*,'Rght=',right

    call search_node_fit(1.5,res)
    print*,'1.5->',res !print 4
    call search_node_fit(1.4,res)
    print*,'1.4->',res !print 4
    call search_node_fit(1.6,res)
    print*,'1.6->',res !print 2
    call search_node_fit(3.6,res)
    print*,'3.6->',res !print 0
end program main
