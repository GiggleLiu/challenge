module problem
    integer :: num_path, num_node
    integer,allocatable :: table(:,:), node_min(:), node_max(:), p0(:), dp(:), occ0(:)
    !f2py num_node, num_path, table
    !f2py node_min, node_max, p0, dp

    contains
    subroutine init_problem(table_, node_min_, node_max_, p0_)
        implicit none
        integer,intent(in) :: table_(:,:), node_min_(:), node_max_(:), p0_(:)
        num_path=size(p0_)
        num_node=size(node_min_)
        allocate(table(num_node,num_path),node_min(num_node),node_max(num_node),&
        p0(num_path),dp(num_path),occ0(num_node))
        table=table_
        node_min=node_min_
        node_max=node_max_
        p0=p0_
        dp=0
        occ0=matmul(table,p0)
    end subroutine init_problem

    subroutine get_cost(cost)
        implicit none
        integer,intent(out) :: cost
        integer :: i,y(num_node)
        !f2py integer,intent(aux) :: num_path
        y=occ0
        do i=1,num_path
            if(dp(i)/=0) then
                y=y+table(:,i)*dp(i)
            endif
        enddo
        cost=0
        do i=1,num_node
            if(y(i)<node_min(i)) then
                cost=cost+(node_min(i)-y(i))**2
            else if(y(i)>node_max(i)) then
                cost=cost+(node_max(i)-y(i))**2
            endif
        enddo
    end subroutine get_cost

    subroutine get_num_overflow(overflow)
        implicit none
        integer,intent(out) :: overflow
        integer :: i,y(num_node)
        !f2py integer,intent(aux) :: num_path

        y=matmul(table,dp)+occ0
        overflow=0
        do i=1,num_node
            if(y(i)<node_min(i)) then
                overflow=overflow+abs(node_min(i)-y(i))
            else if(y(i)>node_max(i)) then
                overflow=overflow+abs(node_max(i)-y(i))
            endif
        enddo
    end subroutine get_num_overflow

    subroutine compute_gradient(num_path_,gradient)
        implicit none
        integer,intent(in) :: num_path_
        integer,intent(out) :: gradient(num_path_)
        integer :: i,dy(num_node),y(num_node)
        !f2py integer,intent(aux) :: num_path
        !f2py depend(num_path_) :: gradient

        !y=matmul(table,dp)+occ0
        y=occ0
        do i=1,num_path
            if(dp(i)/=0) then
                y=y+table(:,i)*dp(i)
            endif
        enddo
        dy=0
        do i=1,num_node
            if(y(i)<node_min(i)) then
                dy(i)=y(i)-node_min(i)
            else if(y(i)>node_max(i)) then
                dy(i)=y(i)-node_max(i)
            endif
        enddo
        !gradient=matmul(dy,table)
        gradient=0
        do i=1,num_node
            if(dy(i)/=0) then
                gradient=gradient+dy(i)*table(i,:)
            endif
        enddo
    end subroutine compute_gradient

    subroutine chdp(i_node,delta)
        implicit none
        integer,intent(in) :: i_node, delta

        dp(i_node+1)=dp(i_node+1)+delta
    end subroutine chdp

    subroutine fin_problem()
        implicit none
        deallocate (table, node_max, node_min,p0,dp,occ0)
    end subroutine fin_problem

end module problem
