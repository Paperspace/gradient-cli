# Gradient CLI Release Notes

# Release Notes for 0.8.0a0
#### New features
* Added `deployments logs` command for reading depoyment logs

# Release Notes for 0.7.0
##### Note: this list includes all changes made in 0.7.0a* alpha releases
#### Breaking changes
* Removed experimental `projects wizard` command
#### New features
* Added some datetime fields to deployment and experiment models
* `--modelId` is not required to create a deployment anymore
* Added commands for reading and streaming experiment, deployment, notebook and job metrics
#### Fixes
* Fix request field name for `deployment create` command
* Fix cluster ID field again

# Release Notes for 0.7.0a3
#### Fixes
* Fixed a bug in model upload introduced in 0.7.0a3

# Release Notes for 0.7.0a2
#### New features
* Added some datetime fields to deployment and experiment models
* `--modelId` is not required to create a deployment anymore
* Added commands for reading and streaming deployment, notebook and job metrics

# Release Notes for 0.7.0a1
#### Fixes
* Fix cluster ID field again

# Release Notes for 0.7.0a0
#### Breaking changes
* Removed experimental `projects wizard` command
#### New features
* Added commands for reading experiment metrics
#### Fixes
* Fix request field name for `deployment create` command

# Release Notes for 0.6.3
#### Fixes
* Fix request field name for `deployment create` command

# Release Notes for 0.6.2
#### New features
* Added support for uploading 100MB+ models
* Added `command` option/parameter to `depoyments create` command and SDK method

# Release Notes for 0.6.1
##### Note: this list includes all changes made in 0.6.1a* alpha releases
### Breaking changes
* `--workspaceUrl` and `--workspaceArchive` replaced by `--workspace`
### New features
* Added `clusters machineTypes list` command
* Added `--projectId` option to `models upload` command
* Overwriting options provided in YAML file with values passed in terminal
### Fixes
* Fix raising KeyError when listing experiments
* Added `clusters list` command
* Fixed URL to a newly created project

# Release Notes for 0.6.1a1
### New features
* Added `--projectId` option to `models upload` command
* Overwriting options provided in YAML file with values passed in terminal

# Release Notes for 0.6.1a0
### Breaking changes
* `--workspaceUrl` and `--workspaceArchive` replaced by `--workspace`
### Fixes
* Added `clusters list` command
* Fixed URL to a newly created project

# Release Notes for 0.6.0
##### Note: this list includes all changes made in 0.6.0a* alpha releases
### Breaking changes
* Removed the `--vpc` flag
* `--name` is not required to create/run experiment. Parameters in methods for creating/running experiments have changed 
### New features
* Added commands to `add` and `remove` tags
* Added filtering notebooks by tags
* Added showing tags in `details` commands
* Added `projects details` command
* Datasets for experiments in YAML options file can now be defined as list of objects
* Allow string instead of list of strings in YAML for options that take multiple values
### Fixes
* Removed empty lines in logs
* Fixed `ExperimentsClient.list` parameters (not a breaking change)
* Fix showing cluster ID in `deployments details`
* Add filtering entities by tags in `list` commands

# Release Notes for 0.6.0a2
### Breaking changes
* Removed the `--vpc` flag

# Release Notes for 0.6.0a1
### New features
* Added commands to `add` and `remove` tags
* Added filtering notebooks by tags
* Added showing tags in `details` commands
* Added `projects details` command

# Release Notes for 0.6.0a0
### Breaking changes
* `--name` is not required to create/run experiment. Parameters in methods for creating/running experiments have changed 
### New features
* Datasets for experiments in YAML options file can now be defined as list of objects
* Allow string instead of list of strings in YAML for options that take multiple values
### Fixes
* Removed empty lines in logs
* Fixed `ExperimentsClient.list` parameters (not a breaking change)
* Fix showing cluster ID in `deployments details`
* Add filtering entities by tags in `list` commands

# Release Notes for 0.5.2
##### Note: this list includes all changes made in 0.5.2a* alpha releases
### New features
* Update `notebooks list` command accepts `--list` and `--offset` arguments and show more notebooks
* Add `deployments details` command
* registry target options to `run` and `jobs create` commands
* `--workspace` option in `experiments` commands does not default to current working directory anymore and is required for VPC experiments

# Release Notes for 0.5.2a3
### New features
* Add `deployments details` command

# Release Notes for 0.5.2a2
### Fixes
* Update `notebooks list` command accepts `--list` and `--offset` arguments and show more notebooks

# Release Notes for 0.5.0
##### Note: this list includes all changes made in 0.5.0a* alpha releases
### New features
* Added `projects delete` command
* Added `models upload` command for uploading model file from local machine
* Added `--workspaceRef` option to `experiments create/run` for specifying branch, commit hash or tag
* Added new options to `experiments create/run` for creating experiments with datasets
* Added several new options to `deployments create`
* Added `deployments update` command
* Added `models details` command
* Added pagination for `experiments list`
### Fixes
* Fixed constant used to create deployment
* Fix listing experiments when filtering by project ID
* Fixed KeyError when setting dataset options without setting --datasetUri
* Fixed error occurring when not all dataset values were set
### Breaking changes
* Dropped dependencies: gradient-statsd and gradient-sdk
* Changed ID attribute in Job and Deployment models from `id_` to `id`

# Release Notes for 0.5.1a3
### Fixes
* Reverted changes to `--clusterId` and `--vpc` from 0.5.1a2

# Release Notes for 0.5.1a2
### Fixes
* Update model upload to accept path to file or directory
### Breaking changes
* Change `--clusterId` to required parameter for creation and start of deployments and experiments
* Remove `--vpc` flag for creation and start of deployments and experiments

# Release Notes for 0.5.1a1
### New features
* Added `model upload` command with directory upload command

# Release Notes for 0.5.0a7
### Fixes
* Fixed error occurring when not all dataset values were set

# Release Notes for 0.5.0a6
### New features
* Added `models details` command
* Added pagination for `experiments list`

# Release Notes for 0.5.0a5
### New features
* Added `deployments update` command

# Release Notes for 0.5.0a4
### Fixes
* Fixed KeyError when setting dataset options without setting --datasetUri

# Release Notes for 0.5.0a3
### New features
* Added `projects delete` command
* Added `models upload` command for uploading model file from local machine
* Added `--workspaceRef` option to `experiments create/run` for specifying branch, commit hash or tag
* Added new options to `experiments create/run` for creating experiments with datasets
* Added several new options to `deployments create`
### Fixes
* Added filtering deleted projects in `projects list`

# Release Notes for 0.5.0a2
### Breaking changes
* Changed ID attribute in Job and Deployment models from `id_` to `id`

# Release Notes for 0.5.0a1
### Fixes
* Fixed constant used to create deployment
* Fix listing experiments when filtering by project ID
### Breaking changes
* Dropped dependencies: gradient-statsd and gradient-sdk

# Release Notes for 0.4.1
### Fixes
* Fixed constant used to create deployment

# Release Notes for 0.5.0a0
### New features
* New `delete` commands for deployments and experiments
* Printing url to instance web client's view to terminal after creating it
## Fixes
* Fix spinner not disappearing when some commands were executed
* base64-encoded `command` value so it's not blocked by Cloudflare's filter anymore
## Breaking changes
* Moved hyperparameters group to experiments group
* Dropped experiment_type_id parameter from create_mpi_multi_node() in ExperimentsClient
* Moved constants and config modules into api_sdk module

# Release Notes for 0.4.0
##### Note: this list includes all changes made in alpha releases since 0.3.2a
### New features
* Command for deleting a tensorboard
* Optional adding new experiment to tensorboard with new `--tensorboard` option. Available for `experiments create` and `experiments run`
* Add MPI-specific options for creating experiments
### Fixes
* Fixed AttributeError raised when `--ignoreFiles` was used
* Fixed showing help for some commands
* Fixed URL for fetching notebook details
* Fix StopIteration exception in Python 3.7
* Fix `job delete` and `job stop` commands
* Fix how some error messages are printed
* Fix formatting of datetime in `projects list` table
* Fix sending some bash commands using `--*command` options caused Cloudflare's filter to stop request

# Release Notes for 0.4.0a5
### Fixes
* Fix formatting of datetime in `projects list` table
* Fix sending some bash commands using `--*command` options caused Cloudflare's filter to stop request

# Release Notes for 0.4.0a4
### Fixes
* Fix how some error messages are printed

# Release Notes for 0.3.7
### Fixes
* Fix formatting of datetime in `projects list` table
* Fix sending some bash commands using `--*command` options caused Cloudflare's filter to stop request

# Release Notes for 0.4.0a4
### Fixes
* Fix how some error messages are printed

# Release Notes for 0.3.6
### Fixes
* Fix `job delete` and `job stop` commands
* Fix how some error messages are printed

# Release Notes for 0.4.0a3
### New features
* Command for deleting a tensorboard
* Optional adding new experiment to tensorboard with new `--tensorboard` option. Available for `experiments create` and `experiments run`
* Add MPI-specific options for creating experiments
### Fixes
* Fixed AttributeError raised when `--ignoreFiles` was used
* Fixed showing help for some commands
* Fixed URL for fetching notebook details
* Fix StopIteration exception in Python 3.7
* Fix `job delete` and `job stop` commands

# Release Notes for 0.3.5
### Fixes
* Fix StopIteration exception in Python 3.7

# Release Notes for 0.3.4
### Fixes
* Fixed bug causing exception be raised when `--help` option was used with some commands (like `gradient run`)

# Release Notes for 0.3.3
### Fixes
* ~~Fixed bug causing exception be raised when `--help` option was used with some commands (like `gradient run`)~~

# Release Notes for 0.3.2
### Fixes
* Fixed bug raising exception when `experiment create's` `--ignoreFiles` option was used

# Release Notes for 0.3.2a
### New features
* Support for tensorboard
    * Create tensorboard
    * List user tensorboards
    * Details of user tensorboard
    * Add experiments to existing tensorboard
    * Remove experiments from existing tensorboard
* Add support for experiments workspace credentials

# Release Notes for 0.3.1
### Fixes
* Fixed bug preventing showing logs when 'experiments run' was executed

# Release Notes for 0.3.0
##### Note: this list includes all changes made in alpha releases since 0.2.3
### New features
* Introduced Python SDK package
* Added `ClusterID` function to support new VPCs
* Hyperparameter private registry and custom container functions added \
`--hyperparameterServerContainer` \
`--hyperparameterServerRegistryPassword` \
`--hyperparameterServerRegistryUsername`
* Automated documentation generation based on sphinx
* Updated documentation and docstrings for SDK based functions
* Improved `--help` functions
* Added support for reading options from file to all commands
* Renamed `--optionsFileTemplate` to `--createOptionsFile`
* Added `machines` support to the SDK
* Added `notebooks` command group with `create`, `delete` and `list` commands
* Added `--clusterId` option `deployments create`
* Added coloured options tags ([required], etc.)
* Showing deployment state in deployments list
### Fixes
* Added support for missing isPreemptible option to the SDK
* Fixed URL to logs of jobs
* Removed hardcoded choices for `--machineType` option
* Fixed message shown while creating deployment
* Fixed exception when listing job artifacts

# Release Notes for 0.3.0a5
### Fixes
* Fixed exception when listing job artifacts

# Release Notes for 0.3.0a4
### New features
* Added `--clusterId` option `deployments create`
### Fixes
* Fixed message shown while creating deployment

# Release Notes for 0.3.0a3
### New features
* Added `machines` support to the SDK
* Added `notebooks` command group with `create`, `delete` and `list` commands
### Fixes
* Removed hardcoded choices for `--machineType` option

# Release Notes for 0.3.0a2
### New features
* Added support for reading options from file to all commands
* Renamed `--optionsFileTemplate` to `--createOptionsFile`
### Fixes
* Fixed URL to logs of jobs

# Release Notes for 0.3.0a1
### New features
* Added --optionFile to read options from YAML file
* Added --optionFileTemplate to create YAML template
###Fixes
* Added support for missing isPreemptible option to the SDK

# Release Notes for 0.3.0a0
### New features
* Introduced Python SDK package
* Added `ClusterID` function to support new VPCs
* Hyperparameter private registry and custom container functions added \
`--hyperparameterServerContainer` \
`--hyperparameterServerRegistryPassword` \
`--hyperparameterServerRegistryUsername`
* Automated documentation generation based on sphinx
* Updated documentation and docstrings for SDK based functions
* Improved `--help` functions

# Release Notes for 0.2.3
### Fixes
* hardcoded `colorama` version to avoid errors during installation

# Release Notes for 0.2.2
##### Note: this list includes all changes made in alpha releases since 0.2.1
### New features
* deprecated `--workspaceArchive` and `--workspaceUrl` for `experiments create/run`, `run` and `jobs create` commands
* single `--workspace` option for defining git, S3 and local workspaces
* experimental wizard for creating projects
* add looking for new client version
* added `projects create` command
* added spinner for some long running commands
### Fixes
* fix autocomplete executing prompt for password when double-tab on gradient apiKey

# Release Notes for 0.2.2a3
### New features
* deprecated `--workspaceArchive` and `--workspaceUrl` for `experiments create/run`, `run` and `jobs create` commands
* single `--workspace` option for defining git, S3 and local workspaces

# Release Notes for 0.2.2a2
###New features
* experimental wizard for creating projects
### Fixes
* fix autocomplete executing prompt for password when double-tab on gradient apiKey

# Release Notes for 0.2.2a1
### New features
* add looking for new client version

# Release Notes for 0.2.2a0
### New features
* added `projects create` command
* added spinner for some long running commands

# Release Notes for 0.2.1
### Fixes
* renamed `createAndStart` commands to `run` for experiments and hyperparameters

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
