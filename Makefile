.PHONY: deps codedev test package
default: test

deps:
	pip install -r requirements-dev.txt

codedev:
	pip install codecov
	codecov

test: deps
	flake8
	tox --recreate

package:
	pip3 install twine==1.11.0 setuptools==28.8.0 wheel==0.31.1
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
