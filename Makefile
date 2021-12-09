PREFIX ?= /usr/local

cbin = gcc gfortran g++ c++ icc ifort icpc icx ifx icpx pgcc pgf77 pgf90 pgf95 pgfortran pgc++ nvc nvc++ nvfortran
mbin = mpicc mpiCC mpigcc mpiicc mpiifort mpifort mpif77 mpif90 mpif08 mpic++ mpicxx ortecc orteCC

.PHONY: wrapper install clean

wrapper:
	mkdir -p bin/mpi
	cp wrapper.sh bin
	./install.sh bin $(cbin)
	./install.sh bin/mpi $(mbin)

install:
	mkdir -p $(PREFIX)
	cp -r bin $(PREFIX)

clean:
	rm -r bin
