.PHONY: all clean

.DEFAULT: all


TARGETS=fsa.so

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

$(TARGETS) : %: bpp_sa.f90
	f2py -m bpp_sa -c bpp_sa.f90 fsa.f90
