PYTEST_AVAILABLE=$( shell which py.test 2>/dev/null; echo $? )

.PHONY: test oldtest clean

test:
ifeq ($(PYTEST_AVAILABLE), 0)
	py.test
else
	@$(MAKE) --quiet oldtest
endif

oldtest:
	python test_wrapper.py

clean:
	-rm -fr __pycache__ *.pyc

