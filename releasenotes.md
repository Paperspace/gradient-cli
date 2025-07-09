# Gradient CLI Release Notes

# Release Notes for 0.9.1a0
* Added basic support for autoscaling deployments

# Release Notes for 0.9.0
##### Note: this list includes all changes made in 0.9.0a* alpha releases
#### Breaking changes
* Normalized parameter names in `notebooks` group and `NotebooksClient`
### Fixes
* Fixed NotImplementedError raised when parsing experiment with dataset volume options set
* Fix output of `metrics stream` command
* Fixed experiment status constants and added constants for deployment statuses
* Fixed reading logs with `--follow`. The bug caused all log lines in a loop instead of only the new one
* Fixed `TypeError` occurring when a job was being created without `--workspace`
### New features
* Added whole directory upload to `models upload` command
* Added a command group for managing `secrets`
* Added `notebooks logs` command for reading logs of notebooks

# Release Notes for 0.9.0a2
### Fixes
* Fixed NotImplementedError raised when parsing experiment with dataset volume options set

# Release Notes for 0.8.1
### Fixes
* Fixed NotImplementedError raised when parsing experiment with dataset volume options set

# Release Notes for 0.9.0a1
#### Fixes
* Fix output of `metrics stream` command
* Fixed experiment status constants and added constants for deployment statuses

# Release Notes for 0.9.0a0
#### Fixes
* Fixed reading logs with `--follow`. The bug caused all log lines in a loop instead of only the new one
* Fixed `TypeError` occurring when a job was being created without `--workspace`
### New features
* Added whole directory upload to `models upload` command
* Added a command group for managing `secrets`

# Release Notes for 0.8.0
##### Note: this list includes all changes made in 0.8.0a* alpha releases
#### Breaking changes
* Removed `entity` parameter from tag-related methods in clients 
#### Fixes
* Fix reading logs with `--follow true`
* Fix creating job without workspace
#### New features
* Added `deployments logs` command for reading depoyment logs
* Added `--command` option to `deployments update`
* Added `--projectId` option to `deployments create` and `deployments update`

# Release Notes for 0.8.0a2
#### Fixes
* Fix reading logs with `--follow true`
* Fix creating job without workspace

# Release Notes for 0.7.1
##### Note: this list includes all changes made in 0.7.1a* alpha releases
#### New features
* Added `deployments logs` command
#### Fixes
* Fix reading logs with `--follow true`
* Fix creating job without workspace

# Release Notes for 0.7.1a0
#### New features
* Added `deployments logs` command
#### Fixes
* Fix reading logs with `--follow true`
* Fix creating job without workspace

# Release Notes for 0.8.0a1
#### Breaking changes
* Removed `entity` parameter from tag-related methods in clients 
#### New features
* Added `--command` option to `deployments update`
* Added `--projectId` option to `deployments create` and `deployments update`

# Release Notes for 0.8.0a0
#### New features
* Added `deployments logs` command for reading depoyment logs
* Added `notebooks create` command for creating and starting a new notebook
* Added `notebooks start` command for starting an existing notebook
* Added `notebooks fork` command for forking a new notebook
* Added `notebooks stop` command for stopping a running notebook
* Added `notebooks artifacts list` command for listing the last workspace artifacts uploaded for a notebook.

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
* Added `machines`