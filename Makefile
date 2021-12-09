PREFIX ?= /usr/local

cbin = gcc gfortran g++ c++ icc ifort icpc icx ifx icpx pgcc pgf77 pgf90 pgf95 pgfortran pgc++ nvc nvc++ nvfortran
mbin = mpicc mpiCC mpigcc mpiicc mpiifort mpifort mpif77 mpif90 mpif08 mpic++ mpicxx ortecc orteCC

wrapper:
	mkdir -p $(PREFIX)/bin/mpi
	cp wrapper.sh $(PREFIX)/bin
	./install.sh $(PREFIX)/bin $(cbin)
	./install.sh $(PREFIX)/bin/mpi $(mbin)
