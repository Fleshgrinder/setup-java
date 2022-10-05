COV_FORMAT ?= xml

PHONY: test
test: MAKEFLAGS += --keep-going
test: install
	coverage run -m pytest
	coverage report
	coverage $(COV_FORMAT)

install:
	pip3 install -r requirements.txt
	touch install

clean:
	rm -fr .pytest_cache/ htmlcov/ coverage coverage.xml install
