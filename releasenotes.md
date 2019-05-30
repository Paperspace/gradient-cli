# Paperspace Python Release Notes

# Release Notes for 0.2.0a5
### Fixes
* removed command group aliases
* streaming logs for `experiments createAndStart` by default

# Release Notes for 0.2.0a4
### New features
* new params for `job create` and `hyperparameters create`
### Fixes
* fixed missing `--experimentType` when creating new single node experiment
* deployments can be of `TFSERVING` type only
* fixed autocomplete instructions

# Release Notes for 0.2.0a3
### New features
* autocomplete for bash (GNU/Linux and iOS)
* aliases in singular form for command groups
* showing logs for experiments and jobs
* restored and deprecated `run` command
* workspace uploading for experiments
* workspace upload progress bar

# Release Notes for 0.2.0a2
### New features
* partial support for hyperparameter tuning
* prompt for apiKey if not provided
* deprecate `login` command
* `--ignoreFiles` option for `experiments create`
* `--ignoreFiles` and `--workspace none` options for `jobs create`
### Fixes
* restore apiKey command

# Release Notes for 0.2.0a1
### New features
* colorful error and help messages
* removed `paperspace-python run` command

# Release Notes for 0.2.0a0
### New features
* partial support for managing jobs, models and projects
* filtering deployments list by project ID and model ID
* reading logs of experiments and jobs
### Fixes
* handling error response when listing experiments

## Release Notes for 0.1.0
### New features
* experiments and deployments management
* --apiKey for all commands for one-time api key overwrite
* help messages for all commands and parameters

## Release Notes for v0.0.19
### New features
* filtering experiments list with `--projectHandle` 
* paginating experiments list when does not fit the terminal width
* added `--modelType` and `--modelPath` to `experiments create`
### Fixes
* some minor bug fixes

## Release Notes for v0.0.19a
### New features
* support for experiments API - creating, starting, listing, etc.

## Release Notes for v0.0.18
### Fixes 
* Fix missing import

## Release Notes for v0.0.16

### New features
* Add statsd agent support with StatsdClient

### Fixes
* Fix crashing on converting to bytes in python < 3

## Release Notes for v0.0.15

### New features
* Run gradient jobs from custom Dockerfile built containers (see: https://docs.paperspace.com/gradient/jobs/create-a-job#new-run-jobs-from-dockerfiles)

* Push GPU-enabled container images to a registry of your choice 

### Fixes
* Add custom headers to requests 

## Release Notes for v0.0.14

#### New features
* Allow user to select preemptible machine types

#### Fixes
* Fix package.egg-info issue affecting Windows users downloading paperspace from PyPI

## Release Notes for v0.0.13

#### New features
* Allow user to select custom port mappings between container and host

#### Fixes
* Fix circular import bug causing problems for python2 users on v0.0.12

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
