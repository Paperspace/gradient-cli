Paperspace Python
=================

Release 0.2.0a1

See [releasenotes.md](https://github.com/Paperspace/paperspace-python/blob/master/releasenotes.md) for details on the current release, as well as release history.

Getting Started
===============
1. Make sure you have a Paperspace account set up. Go to http://paperspace.com
   to register.

2. Use pip, pipenv, or conda to install the paperspace-python package, e.g.:

    `pip install -U paperspace`

    To install/update prerelease (Alpha/Beta) version version of paperspace-python, use:

    `pip install -U --pre paperspace`

3. Download your api key by executing the following:

    `paperspace-python login`

   Follow the prompts to enter your Paperspace email and password.

   You can also enter your credentials directly on the command line as follows:

    `paperspace-python login <email> <password> [<api_token_name>]`

   Note: your api key is cached in ~/.paperspace/config.json
   You can remove your cached api key by executing:

    `paperspace-python logout`

4. Run the sample script hello.py using Python:

    `python hello.py`

   The source of this sample script shows how a script can automatically run itself on the Paperspace job cluster node:

    ```
    import paperspace

    paperspace.run()

    print('hello paperspace-python!')
    ```

   Note: the source is modified before transfer to the job cluster in order to remove imported `paperspace` references.

5. Use paperspace-python to run a python script remotely:

    `paperspace-python run myscript.py`

   The script will be run on the Paperspace job cluster node, and its output will be logged locally.


Create/create and start experiment
=================
To create new experiment use:
```
paperspace-python experiments create [type] [--options]
```
The two available experiment types are `singlenode` and `multinode`.

To create and immediately start new experiment use:
```
paperspace-python experiments createAndStart [type] [--options]
```

For a full list of available commands run `paperspace experiments --help`. 
Note that some options are required to create new experiment.


Specifying jobs options within a script
=======================================
This example shows how a script can specify paperspace jobs options for itself, such as `project` name, `machineType`, and a `container` reference:

    # tests/test_remote.py - runs itself on paperspace, demonstrates setting jobs create options
    import os
    import paperspace

    paperspace.run({'project': 'myproject', 'machineType': 'P5000',
                    'container': 'paperspace/tensorflow-python'})

    print(os.getcwd())
    print('something useful')


Automatic running of a python script remotely
=============================================
The above example demonstrates running a python script locally and having that script transmit itself to the paperspace jobs cluster for further execution.  To do this a copy of the local script is modified before transmission to the jobs cluster, in order to strip out the `import paperspace` statements and other `paperspace` library references. There are also some limitations on the types of import statements that are supported, and the dependencies that are supported in each environment (local vs. remote):

1. You need to use a bare import statement, `import paperspace`, and not use the `import paperspace as ...` form.
2. The import form `from paperspace import ...` is currently not supported.
3. Everything after the `paperspace.run()` function call is ignored when running locally (when no script name is provided).  The local script execution stops after the `paperspace.run()` call.
4. Dependencies that are included before `paperspace.run()` must be available locally.
5. If you need to reference dependencies that are not available locally but are available remotely, those should be imported after the `paperspace.run()` call.
6. Dependencies that are needed remotely need to either be already installed in the container used for the job, or need to be installed using one of the techniques below in the section [Dependency Options](#dependency-options)

Because of these limitations it may not always be appropriate to run python scripts automatically from within the same script file.  As an alternative you can run your python scripts unmodified using the techniques below.


Running a python script by name
===============================
You can run an python script on paperspace from the command line as follows:

    paperspace-python run myscript.py

You can also provide additional jobs options on the command line:

    paperspace-python run myscript.py --project myproject --machineType P5000 \
     --container paperspace/tensorflow-python`

Alternatively you can use the `paperspace.run()` fuction in code with a script file name as the first argument:

    import paperspace

    paperspace.run('myscript.py') # runs myscript on paperspace

In code you can provide additional paperspace jobs create options in a dict in the second argument to run():

    paperspace.run('myscript.py', {'project': 'myproject', 'machineType': 'P5000',
                                   'container': 'paperspace/tensorflow-python'})

See the Paperspace API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for the full list of jobs create options that can be specified.


Using paperspace-python run
===========================
The `paperspace-python run` command provides a number of options to run python code and other commands remotely, as well as copy files and set up python dependencies:

    paperspace-python run [options] [[-m] <script> [args] | -c "python code" | --command "shell cmd"]
      options:
      [--python 2|3]
      [--init [<init.sh>]]
      [--pipenv]
      [--req [<requirements.txt>]]
      [--workspace .|<workspace_path>]
      [--ignoreFiles "<file-or-dir>,..."]
      [jobs create options]
      [--dryrun]
      [-]

Basic Run Scenarios
===================
1. Run a python script remotely:

    `paperspace-python run <python_script.py> [args]`

   Example:

    `paperspace-python run myscript.py a b c`

2. Run a python module remotely using the `-m` option:

    `paperspace-python run -m <module_path> [args]`

   Example:

    `paperspace-python run -m pip --version`

3. Run a python command remotely using the `-c` option:

    `paperspace-python run -c "python_statement;..."`

   Example:

    `paperspace-python run -c "import os; print(os.getcwd())"`

4. Run an executable or shell command remotely using the `--command` option:

    `paperspace-python run --command "<executable or shell command>"`

   Example:

    `paperspace-python run --command "ls -al"`

Run Options
===========
The `<script>` option is a python script or path to a python module.  The script or module will be uploaded if it exists on the local file system.

Other script`args` can be provided after the python script or module path.  You can use the `-` option to suppress interpretation of the list of script args as `paperspace-python run` options. 

The `-m <module path>` option runs the specified library module as a script.  This is equivalent to the `-m` option of the `python` executable.  Further paperspace run option processing is disabled after the `-m` option.

The `-c "python_statement;..."` option runs the specified python statements.  This is equivalent to the `-c` option of the `python` executable.  Further paperspace run option processing is disabled after the `-c` option.

The `-` option disables further run command option processing and passes the remaining arguments to the script specified.  This allows you to pass arguments to your script that might otherwise conflict with run command options or jobs create options.

The `--command "shell cmd"` option is used to run an arbitrary executable or shell command inside the container.  Note: the executable or shell command must already be available inside the container image, or be copied over using the `--workspace` option.

Job Options
===========
The `--workspace` option allows you to specify a workspace file or directory to upload, or a git repo link to download and merge with the container.  For example, to upload the current directory along with a script file run:

    paperspace-python run myscript.py --workspace .

See the Paperspae API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for more details on the `--workspace` option and related options.

The `--ignoreFiles "<file-or-dir>,..."` option can be used specify a simple comma separated list of files and directories to ignore for the workspace upload:

    paperspace-python run myscript.py --workspace . --ignoreFiles "hello.py,paperspace"

The following files and directories are ignored by default: `.git`, `.gitignore`, `__pycache__`.

Other `jobs create options` can be specified, such as `--machineType <machine type>`, `--container <container image reference>`, and `--project <project name>`.

Here are some of the other jobs create options available:

- `--project "<project name>"`  (defaults to 'paperspace-python')
- `--machineType [GPU+|P4000|P5000|P6000|V100]`  (defaults to P5000)
- `--container <docker image link or paperspace container name>`  (defaults to `docker.io/paperspace/tensorflow-python`)
- `--name "<job name>"` (defaults to 'job for project <project name>')
- `--projectId "<existing paperspace project id>"`
- `--registryUsername "<username>"`  (for access to a private docker registry)
- `--registryPassword "<secretpw>"`  (for access to a private docker registry)
- `--workspaceUsername "<username>"`  (for access to a private git repo)
- `--workspacePassword "<secretpw>"`  (for access to a private git repo)

See the Paperspae API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for a complete description of these options.

Dependency Options
==================
When running python scripts on paperspace you may need to provide additional dependencies to your scripts or specify the python version.
The `paperspace-python run` command has several options to support this: `--python`, `--init`, `--pipenv`, and `--req`. In addition you can use the `--workspace` option above to upload file dependencies.

The `--python 2|3` option allows you specify whether to use `python2` or `python3` when running the script on paperspace.
If ommitted, the script will be run with the same major version as is being used to run `paperspace-python` locally.

The `--init [<init.sh>]` option is used to specify a script to be run on the remote machine, inside the container, before the python script is run.
If the init script name is ommitted, it is assumed to be the script named `init.sh` in the current directory.  The script is run using
`source init.sh` in the container bash shell.  You can use this option to provide a list of commands to run to set up the dependencies for the script, such as running a list of `pip install` commands.  However, if you are using `pipenv` or a `requirements.txt` file we recommend you use one of the options below.  Multiple dependency setup options can be combinded however.

The `--pipenv` option is used to upload and run the `Pipfile` and `Pipfile.lock` files in the current directory, if found.  These files
are used on the paperspace machine to initialize the python environment using the `pipenv` tool, by running `pipenv install` within the container.  Note: `pipenv` must already be installed in the container for this option to work.  The default container used by paperspace-python already has the `pipenv` package installed.

The `--req [<requirements.txt>]` option is used specify that a `requirements.txt` file should be used to install the required python dependencies using `pip`.
By default this option looks for a file named `requirements.txt` in the current directory, but you can override this by specifying a different file name.  Note: `pip` must already be installed in the container for this option to work.  The default container used by paperspace-python already has the `pip` package installed.

The `--dryrun` option allows you to see the resultant script that will be run on the paperspace job runner without actually running it.

All of the above options can be combined in any combination, however, the order of operations is fixed to the following:

1. `source <init.sh>` is run if `--init <init.sh>` is specified
2. `pipenv [--two|--three] install` is run if `--pipenv` is specified
3. `pip[2|3] install -r requirements.txt` is run if `--req <requirements.txt>` is specified
4. `python[2|3] myscript.py` is run

As mentioned above, you can use the `--dryrun` option to see the resultant commands that will be run on the paperspace jobs cluster node for a given set of options, without actually running the commands.


Default Container
=================
If no `container` option is specified when using `paperspace run <script.py>` or the `paperspace.run()` function the default container image used is `paperspace/tensorflow-python` on Docker Hub.  This container has the tensorflow-gpu libraries installed for both python2 and python3, as well as several other popular packages, including numpy, scipy, scikit-learn, pandas, Pillow and matplotlib.
It is based off the Google docker image `gcr.io/tensorflow/tensorflow:1.5.0-gpu` with the addition of support for python3, pip3, and pipenv.

A Dockerfile for building this container image is [here](https://github.com/Paperspace/tensorflow-python/).

Other examples
==============
See the scripts in the `tests` folder for other examples.


Other Authentication options
============================
1. Specify your apiKey explicitly on the paperspace.run() function or any of the paperspace.jobs methods, e.g.:

    ```
    paperspace.jobs.create({'apiKey': '1qks1hKsU7e1k...', 'project': 'myproject',
                            'machineType': 'P5000', 'container': 'paperspace/tensorflow-python'})
    ```

2. Set the package paperspace.config option in your python code:

    `paperspace.config.PAPERSPACE_API_KEY = '1qks1hKsU7e1k...'`

3. Set the PAPERSPACE_API_KEY environment variable:

    (on linux/mac:) `export PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

    (on windows:) `set PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

   Note: the above methods take precedence over use of the cached api key in
   `~/.paperspace/config.json`

4. Set the key in the `~/.paperspace/config.json` file from the command line by running:

    `paperspace-python apikey 1qks1hKsU7e1k...`


Using SAML, AD or GitHub credentials
====================================
Currently only email login is supported in the CLI - if you're using AD, SAML or GitHub to login to Paperspace, you will need an API key to log in with the CLI. 

You can create an API key from within your Paperspace console under the [API](https://www.paperspace.com/console/account/api) section. Login to your [Paperspace console](https://www.paperspace.com/console), scroll to the API section in the left navigation bar, and click [CREATE AN API KEY](https://www.paperspace.com/console/account/api). Follow the instructions there.
You will need to pick and API token name for your API key, and also provide a description.  You can copy the API key value associated with the API token name only at the time of initial creation. If you need to access your API key in the future, you can instead access it by API token name using the 'paperspace-python login' command.

Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
