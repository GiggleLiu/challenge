.PHONY: all clean

.DEFAULT: all


TARGETS=fproblem.so
F90=gfortran

all: $(TARGETS)

clean:
	rm -f *.o *.mod *.so

fproblem.so: %: problem.f90
	f2py -m fproblem -c problem.f90

bintree.o binary_tree.mod: bintree.f90
	$(F90) -c bintree.f90
quicksort.o quicksort.mod: quicksort.f90
	$(F90) -c quicksort.f90
binpacking.o binpacking.mod: binpacking.f90
	$(F90) -c binpacking.f90
bpp_sa.o bpp1d.mod:bpp_sa.f90
	$(F90) -c bpp_sa.f90
ftest: fsa.f90 quicksort.mod bpp1d.mod binpacking.mod binary_tree.mod quicksort.o bpp_sa.o binpacking.o bintree.o
	$(F90) fsa.f90 -fcheck=all -fbounds-check quicksort.o bpp_sa.o binpacking.o bintree.o -o ftest
