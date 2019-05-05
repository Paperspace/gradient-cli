clean-tox:
	rm -rf .tox paperspace.egg-info

run-tests: clean-tox
	tox
