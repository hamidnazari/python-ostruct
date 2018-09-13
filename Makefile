.PHONY: deps codedev test
default: test

deps:
	pip install -r requirements-dev.txt

codedev:
	pip install codecov
	codecov

test: deps
	flake8
	tox --recreate
