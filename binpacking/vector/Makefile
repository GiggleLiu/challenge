.PHONY: all clean

.DEFAULT: all


TARGETS=fsa.so
F90=gfortran

all: $(TARGETS)

clean:
	rm -f *.o *.mod *.so

$(TARGETS) : %: bpp_sa.f90 bpp1d.mod
	f2py -m bpp_sa -c bpp_sa.f90 quicksort.f90 binpacking.f90 fsa.f90

quicksort.o quicksort.mod: quicksort.f90
	$(F90) -c quicksort.f90
binpacking.o binpacking.mod: binpacking.f90
	$(F90) -c binpacking.f90
bpp_sa.o bpp1d.mod:bpp_sa.f90
	$(F90) -c bpp_sa.f90
ftest: fsa.f90 quicksort.mod bpp1d.mod binpacking.mod quicksort.o bpp_sa.o binpacking.o
	$(F90) fsa.f90 -fcheck=all -fbounds-check quicksort.o bpp_sa.o binpacking.o -o ftest
