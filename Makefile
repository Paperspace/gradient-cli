PIP=pip3


clean-tests:
	rm -rf .tox paperspace.egg-info

run-tests: clean-tests
	tox

pip-update:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools

pip-install-dev: pip-update
	$(PIP) install --upgrade -e .[dev]
