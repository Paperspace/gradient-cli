clean-tests:
	rm -rf .tox paperspace.egg-info

run-tests: clean-tests
	tox
