PROG=changelogtools

PY:=$(shell which python)
COVERAGE:=$(shell which coverage)
TWINE:=$(shell which twine)

build:
	$(PY) setup.py build

pkg:
	$(PY) setup.py sdist
	$(PY) setup.py bdist_wheel --universal

publish:
	twine upload dist/*

tests:
	$(PY) setup.py test

coverage:
	$(COVERAGE) run setup.py test

test-ci: coverage

clean:
	rm -rf build .eggs changelog_tools.egg-info $(PROG)/__pycache__ .coveragerc .cache .coverage $(PROG)/*.pyc
