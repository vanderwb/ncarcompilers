
.PHONY: test oldtest

test:
	py.test || $(MAKE) oldtest

oldtest:
	python test_wrapper.py
