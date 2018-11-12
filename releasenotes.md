# Paperspace Python Release Notes

## Release Notes for v0.0.12

#### New features
* New cluster and machineType functionality supported: send jobs to a gradient-node based on the cluster name or clusterId
    * For more information on running gradient-node see the [Gradient Private Cloud](https://docs.paperspace.com/gradient/private-cloud/about) docs
* Send jobs to a specific node by specifying node attributes
* Changed default handling of machineType: cluster preferences come first
* Jobs create automatically records the git commit hash for local workspaces using git

## Release Notes for v0.0.11

#### New features
* New jobs machineTypes method for discovering available job machine types.

#### Fixes
* Minor doc fixes

## Release Notes for v0.0.10

#### New features
* `paperspace-python run` command for running python scripts unmodified on paperspace
* run a python script, module, or command string remotely
* run a executable or shell command remotely
* use pip, pipenv, or a shell script to manage python dependencies
* Improved docs

#### Fixes
* Minor doc fixes

#### Changes
* The default machineType for paperspace-python is now P5000, since GPU+ machines are not yet available for jobs.
* The default container image for paperspace-python is 'docker.io/paperspace/tensorflow-python' which adds python3 support to Google's 'gcr.io/tensorflow/tensorflow:1.5.0-gpu' container.

## Release Notes for v0.0.9

#### New features
* This is the first official release of the Paperspace Python package.
* It provides support for Gradient jobs and running python modules as jobs.
* There are python packages available on PyPI: https://pypi.python.org/pypi/paperspace
* And on Anaconda.org for Conda: https://anaconda.org/paperspace/paperspace
