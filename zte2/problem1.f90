module problem
    integer :: num_path, num_node
    integer,allocatable :: table(:,:), node_min(:), node_max(:), p0(:)
    logical,allocatable :: change_mask(:)
    !f2py num_node, num_path, table
    !f2py node_min, node_max, change_mask, p0

    contains
    subroutine init_problem(table_, node_min_, node_max_, p0_)
        implicit none
        integer,intent(in) :: table_(:,:), node_min_(:), node_max_(:), p0_(:)
        num_path=size(p0_)
        num_node=size(node_min_)
        allocate(table(num_node,num_path),node_min(num_node),node_max(num_node),&
        p0(num_path),change_mask(num_path))
        table=table_
        node_min=node_min_
        node_max=node_max_
        p0=p0_
        change_mask=.false.
    end subroutine init_problem

    subroutine get_cost(dp,cost)
        implicit none
        integer,intent(in) :: dp(num_path)
        integer,intent(out) :: cost
        integer :: i,y(num_node),x(num_path)
        !f2py integer,intent(aux) :: num_path
        x=p0+dp
        y=matmul(table,x)
        cost=0
        do i=1,num_node
            if(y(i)<node_min(i)) then
                cost=cost+(node_min(i)-y(i))**2
            else if(y(i)>node_max(i)) then
                cost=cost+(node_max(i)-y(i))**2
            endif
        enddo
    end subroutine get_cost

    subroutine compute_gradient(dp,gradient,num_path_)
        implicit none
        integer,intent(in) :: num_path_,dp(num_path_)
        integer,intent(out) :: gradient(num_path_)
        integer :: i,dy(num_node),x(num_path),y(num_node)
        !f2py integer,intent(aux) :: num_path
        !f2py depend(num_path_) :: dp,gradient

        x=p0+dp
        y=matmul(table,x)
        dy=0
        do i=1,num_node
            if(y(i)<node_min(i)) then
                dy(i)=y(i)-node_min(i)
            else if(y(i)>node_max(i)) then
                dy(i)=y(i)-node_max(i)
            endif
        enddo
        gradient=matmul(dy,table)
    end subroutine compute_gradient

    subroutine fin_problem()
        implicit none
        deallocate (table, node_max, node_min,p0,change_mask)
    end subroutine fin_problem

end module problem
