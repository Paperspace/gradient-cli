PIP=pip3

clean-tests:	
	rm -rf .tox gradient.egg-info

run-tests: clean-tests
	tox

pip-update:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools

pip-install-dev: pip-update
	$(PIP) install --upgrade -e .[dev]

clean:
	rm -rf dist/*
	rm -rf .tox gradient.egg-info
	
package:
	python setup.py sdist
	python setup.py bdist_wheel
