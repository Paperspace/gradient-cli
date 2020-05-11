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

prepare-docs-source:
	@sphinx-apidoc -f -o source gradient
	@cp source/cli_docs/gradient.cli.rst source/gradient.cli.rst

gh-pages: prepare-docs-source
	@make html
	@cp -a build/html/. docs


# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
