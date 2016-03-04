PYTEST_AVAILABLE=$(shell which py.test > /dev/null 2>&1 ; echo $$? )

.PHONY: test exectest unittest oldunittest clean

test: unittest exectest

exectest:
	./gcc --show
	@echo
	./gcc --version
	@echo "========================================"
	PATH=`pwd`:$(PATH) gcc --show
	@echo
	PATH=`pwd`:$(PATH) gcc --version
	@echo "========================================"
	PATH=./:$(PATH) gcc --show
	@echo
	PATH=./:$(PATH) gcc --version

unittest:
ifeq ($(PYTEST_AVAILABLE), 0)
	py.test
else
	@$(MAKE) --quiet oldunittest
endif

oldunittest:
	python test_wrapper.py

clean:
	-rm -fr __pycache__ *.pyc

