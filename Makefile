.PHONY: deps codedev test clean package
default: test

deps:
	pip install -r requirements-dev.txt

codedev:
	pip install codecov
	codecov

test: deps
	flake8
	tox --recreate

clean:
	find . -name __pycache__ -type d
	rm -rf ./.cache ./.pytest_cache ./.tox ./build ./dist ./ostruct.egg-info

package: clean
	pip3 install twine==1.11.0 setuptools==28.8.0 wheel==0.31.1
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
