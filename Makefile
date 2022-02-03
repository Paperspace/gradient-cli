PIP=pip3


clean-tests:
	rm -rf .tox paperspace.egg-info
	rm -rf tests/.coverage

run-tests: clean-tests
	tox

pip-update:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools

pip-install-dev: pip-update
	$(PIP) install --upgrade -e .[dev]

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf build dist
