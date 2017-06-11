! Recursive Fortran 95 quicksort routine
! sorts real numbers into ascending numerical order
! Author: Juli Rew, SCD Consulting (juliana@ucar.edu), 9/03
! Based on algorithm from Cormen et al., Introduction to Algorithms,
! 1997 printing

! Made F conformant by Walt Brainerd

module qsort_c_module
    !implicit none
    !public :: quicksort_fi,quicksort_if,quicksort_ii
    !private :: partition_fi,Partition_if,Partition_ii
contains
    recursive subroutine quicksort_fi(A,B)
      real, intent(inout), dimension(:) :: A
      integer, intent(inout), dimension(:) :: B
      integer :: iq

      if(size(A) > 1) then
         call partition_fi(A, B, iq)
         call quicksort_fi(A(:iq-1), B(:iq-1))
         call quicksort_fi(A(iq:), B(iq:))
      endif
    end subroutine quicksort_fi

    subroutine partition_fi(A, B, marker)
      real, intent(in out), dimension(:) :: A
      integer, intent(in out), dimension(:) :: B
      integer, intent(out) :: marker
      integer :: i, j
      real :: temp
      integer :: temp_B
      real :: x      ! pivot point
      x = A(1)
      i= 0
      j= size(A) + 1

      do
         j = j-1
         do
            if (A(j) <= x) exit
            j = j-1
         end do
         i = i+1
         do
            if (A(i) >= x) exit
            i = i+1
         end do
         if (i < j) then
            ! exchange A(i) and A(j)
            temp = A(i)
            temp_B = B(i)
            A(i) = A(j)
            B(i) = B(j)
            A(j) = temp
            B(j) = temp_B
         elseif (i == j) then
            marker = i+1
            return
         else
            marker = i
            return
         endif
      end do
    end subroutine partition_fi

    recursive subroutine quicksort_ii(A,B)
      integer, intent(inout), dimension(:) :: A
      integer, intent(inout), dimension(:) :: B
      integer :: iq

      if(size(A) > 1) then
         call Partition_ii(A, B, iq)
         call quicksort_ii(A(:iq-1), B(:iq-1))
         call quicksort_ii(A(iq:), B(iq:))
      endif
    end subroutine quicksort_ii

    subroutine Partition_ii(A, B, marker)
      integer, intent(in out), dimension(:) :: A
      integer, intent(in out), dimension(:) :: B
      integer, intent(out) :: marker
      integer :: i, j
      integer :: temp
      integer :: temp_B
      integer :: x      ! pivot point
      x = A(1)
      i= 0
      j= size(A) + 1

      do
         j = j-1
         do
            if (A(j) <= x) exit
            j = j-1
         end do
         i = i+1
         do
            if (A(i) >= x) exit
            i = i+1
         end do
         if (i < j) then
            ! exchange A(i) and A(j)
            temp = A(i)
            temp_B = B(i)
            A(i) = A(j)
            B(i) = B(j)
            A(j) = temp
            B(j) = temp_B
         elseif (i == j) then
            marker = i+1
            return
         else
            marker = i
            return
         endif
      end do
    end subroutine Partition_ii

    recursive subroutine quicksort_if(A,B)
      integer, intent(inout), dimension(:) :: A
      real, intent(inout), dimension(:,:) :: B
      integer :: iq

      if(size(A) > 1) then
         call Partition_if(A, B, iq)
         call quicksort_if(A(:iq-1), B(:iq-1,:))
         call quicksort_if(A(iq:), B(iq:,:))
      endif
    end subroutine quicksort_if

    subroutine Partition_if(A, B, marker)
      integer, intent(in out), dimension(:) :: A
      real, intent(in out), dimension(:,:) :: B
      integer, intent(out) :: marker
      integer :: i, j
      integer :: temp
      real :: temp_B(size(B,2))
      integer :: x      ! pivot point
      x = A(1)
      i= 0
      j= size(A) + 1

      do
         j = j-1
         do
            if (A(j) <= x) exit
            j = j-1
         end do
         i = i+1
         do
            if (A(i) >= x) exit
            i = i+1
         end do
         if (i < j) then
            ! exchange A(i) and A(j)
            temp = A(i)
            temp_B = B(i,:)
            A(i) = A(j)
            B(i,:) = B(j,:)
            A(j) = temp
            B(j,:) = temp_B
         elseif (i == j) then
            marker = i+1
            return
         else
            marker = i
            return
         endif
      end do
    end subroutine Partition_if
end module qsort_c_module
