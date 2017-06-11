module type_a_def 
   implicit none 
   type type_a 
      real x 
      type(type_a), pointer :: left => null() 
      type(type_a), pointer :: right => null() 
   end type type_a 
end module type_a_def 
module type_a_ops 
   use type_a_def 
   implicit none 
   interface operator(<=) 
      module procedure less_than_or_equals 
   end interface operator(<=) 
   interface assignment(=) 
      module procedure assign 
   end interface assignment(=) 
   contains 
      function less_than_or_equals(x,y) 
         logical less_than_or_equals 
         type(type_a), intent(in) :: x 
         type(type_a), intent(in) :: y 
         less_than_or_equals = x%x <= y%x 
      end function less_than_or_equals 
      subroutine assign(y, x) 
         type(type_a), intent(out) :: y 
         type(type_a), intent(in) :: x 
         y%x = x%x 
         y%left => x%left 
         y%right => x%right 
      end subroutine assign 
end module type_a_ops 
module tree_funcs 
   use type_a_ops 
   implicit none 
   contains 
      recursive subroutine add_node(root, node) 
         type(type_a), pointer :: root 
         type(type_a), target :: node 
         if(.NOT.associated(root)) then 
            root => node 
         else if(node <= root) then 
            call add_node(root%left, node) 
         else 
            call add_node(root%right, node) 
         end if 
      end subroutine add_node 
      recursive subroutine delete_node(root, node) 
         type(type_a), pointer :: root 
         type(type_a), intent(in) :: node 
         type(type_a), pointer :: temp 
         if(.NOT.associated(root)) then 
            write(*,'(a)') ' Node not found' 
            return 
         end if 
         if(node <= root) then 
            if(root <= node) then 
               if(.NOT.associated(root%left)) then 
                  temp => root 
                  root => root%right 
                  nullify(temp%right) 
                  deallocate(temp) 
               else if(.NOT.associated(root%right)) then 
                  temp => root 
                  root => root%left 
                  nullify(temp%left) 
                  deallocate(temp) 
               else 
                  temp => delete_and_return_biggest(root%left) 
                  temp%left => root%left 
                  temp%right => root%right 
                  root%left => temp 
                  temp => root 
                  root => root%left 
                  nullify(temp%left) 
                  nullify(temp%right) 
                  deallocate(temp) 
               end if 
            else 
               call delete_node(root%left, node) 
            end if 
         else 
            call delete_node(root%right, node) 
         end if 
      end subroutine delete_node 
      recursive function delete_and_return_biggest(root) result(temp) 
         type(type_a), pointer :: temp 
         type(type_a), pointer :: root 
         if(.NOT.associated(root%right)) then 
            temp => root 
            root => root%right 
            nullify(temp%left) 
         else 
            temp => delete_and_return_biggest(root%left) 
         end if 
      end function delete_and_return_biggest 
      recursive subroutine get_stats(root, count, small, big, sum) 
         type(type_a), pointer :: root 
         integer count 
         real small 
         real big 
         real sum 
         real dud 
         if(.NOT.associated(root)) then 
            write(*,'(a)') ' No stats for empty tree' 
            return 
         end if 
         if(associated(root%left)) then 
            call get_stats(root%left, count, small, dud, sum) 
         else 
            small = root%x 
         end if 
         count = count+1 
         sum = sum+root%x 
         if(associated(root%right)) then 
            call get_stats(root%right, count, dud, big, sum) 
         else 
            big = root%x 
         end if 
      end subroutine get_stats 
      recursive function find_n(root, n) result(result) 
         real result 
         type(type_a), pointer :: root 
         integer n 
         if(.NOT.associated(root)) then 
            write(*,'(a)') ' Tree too small' 
            return 
         end if 
         if(associated(root%left)) then 
            result = find_n(root%left, n) 
         end if 
         if(n <= 0) return 
         result = root%x 
         n = n-1 
         if(n <= 0) return 
         if(associated(root%right)) then 
            result = find_n(root%right, n) 
         end if 
      end function find_n 
      recursive subroutine print_tree(root) 
         type(type_a), pointer :: root 
         if(.NOT.associated(root)) then 
            write(*,'(a)') ' Empty tree' 
         else 
            if(associated(root%left)) call print_tree(root%left) 
            write(*,*) root%x 
            if(associated(root%right)) call print_tree(root%right) 
         end if 
      end subroutine print_tree 
end module tree_funcs 
program binary_tree 
   use tree_funcs 
   real harvest 
   integer i 
   type(type_a), target :: temp 
   type(type_a), pointer :: root => NULL() 
   type(type_a), pointer :: ptr => NULL() 
   integer many 
   integer count 
   real small 
   real big 
   real sum 
   write(*,'(a)', advance = 'no') ' Enter how many elements you want:> ' 
   read(*,*) many 
   call random_seed() 
   do i = 1, many 
      call random_number(harvest) 
      allocate(ptr) 
      ptr = type_a(harvest, NULL(), NULL()) 
      call add_node(root, ptr) 
   end do 
   write(*,'(a)') ' Printing the tree...' 
   call print_tree(root) 
   count = 0 
   sum = 0 
   call get_stats(root, count, small, big, sum) 
   write(*,'(a,i0)') ' The number of elements is ', count 
   write(*,'(a,f0.6)') ' The smallest element is ', small 
   write(*,'(a,f0.6)') ' The biggest element is ', big 
   write(*,'(a,f0.6)') ' The sum of the elements is ', sum 
   write(*,'(a,f0.6)') ' The average of the elements is ', sum/count 
   write(*,'(a,f0.6)') ' The median element is ', find_n(root, count/2) 
   write(*,'(a,f0.6)') ' Deleting median element...' 
   temp = type_a(find_n(root, count/2), NULL(), NULL()) 
   call delete_node(root, temp) 
   write(*,'(a)') ' Printing the tree...' 
   call print_tree(root) 
end program binary_tree 
