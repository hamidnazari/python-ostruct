.PHONY: install codedev test
default: test

install:
	pip install -r requirements-dev.txt

codedev:
	pip install codecov
	codecov

test: install
	flake8
	tox --recreate
