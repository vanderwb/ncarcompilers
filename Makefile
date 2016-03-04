PYTEST_AVAILABLE=$(shell which py.test > /dev/null 2>&1 ; echo $$? )

.PHONY: unittest oldunittest clean

unittest:
ifeq ($(PYTEST_AVAILABLE), 0)
	py.test
else
	@$(MAKE) --quiet oldtest
endif

oldunittest:
	python test_wrapper.py

clean:
	-rm -fr __pycache__ *.pyc

