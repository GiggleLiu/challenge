.PHONY: all clean

.DEFAULT: all


TARGETS=fsa.so

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

$(TARGETS) : %: problem.f90 fsa.f90
	f2py -m fsa -c problem.f90 fsa.f90
