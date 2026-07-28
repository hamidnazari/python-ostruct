.PHONY: build clean install lint package test

PYTHON ?= python3

default: lint test

install:
	$(PYTHON) -m pip install --editable ".[test,dev]"

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest --cov=ostruct --cov-report=term-missing

clean:
	rm -rf .cache .pytest_cache .tox build dist htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

build: clean
	$(PYTHON) -m build

package: build
	$(PYTHON) -m twine check dist/*
