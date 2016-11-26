.PHONY: standard build clean install-dev lint test test-all

standard: test lint

build:
	python setup.py sdist bdist_wheel

clean:
	find . -type d -name '__pycache__' | xargs rm -r
	find . -type f -name '*.pyc' -delete

install-test:
	pip install -r requirements-test.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	flake8

test:
	py.test

test-all:
	tox
