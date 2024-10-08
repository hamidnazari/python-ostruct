.PHONY: deps codecov test clean package upload
default: test

deps:
	pip install -Ur requirements-dev.txt

codecov:
	pip install codecov
	codecov

test: deps
	flake8
	tox --recreate

clean:
	find . -name __pycache__ -type d
	rm -rf ./.cache ./.pytest_cache ./.tox ./build ./dist ./ostruct.egg-info

package: clean
	pip3 install -Ur requirements-build.txt
	python3 setup.py sdist bdist_wheel

upload: package
	twine upload dist/*
