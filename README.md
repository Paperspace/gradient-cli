Paperspace Python
=================

Sample usage
============
1. Make sure you have a Paperspace account set up. Go to http://paperspace.com
   to register.

2. Send an email message to support@paperspace.com to request access to the
   Paperspace API Beta program.

   Wait for an email confirmation indicating your account has been approved
   before proceeding.

3. Use pip, pipenv, or conda to install the paperspace-python package, e.g.:

    `pip install paperspace`

4. Download your api key by executing the following:

    `paperspace-python login`

   Follow the prompts to enter your Paperspace email and password.

   You can also enter your credentials directly on the command line as follows:

    `paperspace-python login <email> <password> [<api_token_name>]`

   Note: your api key is cached in ~/.paperspace/config.json
   You can remove your cached api key by executing:

    `paperspace-python logout`

5. Execute the sample Python script hello.py:

    `python hello.py`

 This sample shows how a script can automatically run itself on the Paperspace job cluster node.
 Note: the script is further modified before transfer in order to remove `paperspace` references.

6. Execute an unmodified Python script remotely:

    `paperspace-python myscript.py`

 The script will be run on the Paperspace job cluster node, and its output will be logged locally.


A slightly more complex example
===============================
    # tests/test_remote.py

    import os

    import paperspace

    paperspace.run({'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

    print(os.getcwd())

    print('something useful')


Automatic running of the current python script remotely
=======================================================
The above example demonstrate running a python script locally and having that script transmit itself to the paperspace jobs cluster for further execution.  To do this a copy of the local script is modified before transmission to the jobs cluster, in order to strip out the `import paperspace` statements and other `paperspace` library references. There are also some limitations on the types of import statements that are supported, and the dependencies that are supported in each environment (local vs. remote):

1. You need to use a bare import statement, `import paperspace`, and not use the `import paperspace as ...` form.
2. The import form `from paperspace import ...` is currently not supported.
3. Everything after the `paperspace.run()` function call is ignored when running locally (when no script name is provided).  The local script execution stops after the `paperspace.run()` call.
4. Dependencies that are included before `paperspace.run()` must be available locally.
5. If you need to reference dependencies that are not available locally but are available remotely, those should be imported after the `paperspace.run()` call.
6. Dependencies that are needed remotely need to either be already installed in the container used for the job, or need to be installed using one of the techniques below in the section [Setting up python script dependencies remotely](#setting-up-python-script-dependencies-remotely)

Because of these limitations it may not always be appropriate to run python scripts automatically from within the same script file.  As an alternative you can run your python scripts unmodified using the techniques in the next section.


Running a python script by name
===============================
You can run an python script on paperspace from the command line as follows:

    paperspace-python run myscript.py

You can also provide additional jobs options on the command line:

    paperspace-python run myscript.py --project myproject --machineType P5000 --container Test-Container

Alternatively you can use the `paperspace.run()` fuction in code with, a script file name as the first argument:

    import paperspace

    paperspace.run('myscript.py') # runs myscript on paperspace

In code you can provide additional paperspace jobs create options in a dict in the second argument to run():

    paperspace.run('myscript.py', {'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

See the Paperspace API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for the full list of jobs create options that can be specified.


Setting up python script dependencies remotely
==============================================
When running python scripts on paperspace you may need to provide additional dependencies to your scripts.
The `paperspace-python run` command and `paperspace.run()` function provide several options to support this:

    paperspace-python run [-m] <python_script.py> [--python 2|3] [--init [<init.sh>]] [--pipenv] [--req [<requirements.txt>] [--workspace .|<workspace_path>] [--ignoreFiles "<file-or-dir>,<file-or-dir>,..."] [other jobs create options...] [--dryrun] [script args]

The `-m` option runs the specified library module as a script.  This is equivalent to the `-m` option of the `python` executable.

The `--python 2|3` option allows you specify whether to use `python2` or `python3` when running the script on paperspace.
If ommitted, the script will be run with the same major version as is being used to run `paperspace-python` locally.

The `--init [<init.sh>]` option is used to specify a script to be run on the remote machine, inside the container, before the python script is run.
If the script name is ommitted, it is assumed to be the script named `init.sh` in the current directory.  The script is run using
`source init.sh` in the container bash shell.  You can use this option to provide a list of commands to run to set up the dependencies for the script, such as running a list of `pip install` commands.  However, if you are using `pipenv` or a `requirements.txt` file we recommend you use one of the options below.  Multiple dependency setup options can be combinded however.

The `--pipenv` option is used to upload and run the `Pipfile` and `Pipfile.lock` files in the current directory, if found.  These files
are used on the paperspace machine to initialize the python environment using the `pipenv` tool, by running `pipenv install` within the container.  Note: `pipenv` must already be installed in the container for this option to work.  The default container used by paperspace-python already has the `pipenv` package installed.

The `--req [<requirements.txt>]` option is used specify that a `requirements.txt` file should be used to install the required python dependencies using `pip`.
By default this option looks for a file named `requirements.txt` in the current directory, but you can override this by specifying a different file name.  Note: `pip` must already be installed in the container for this option to work.  The default container used by paperspace-python already has the `pip` package installed.

The jobs create `--workspace` option is also available with any or all of the above options.
With the `--workspace` option you can specify a workspace directory to upload.  For example, to upload the current directory along with the script file run:

    paperspace-python run myscript.py --workspace .

See the Paperspae API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for more details on the `--workspace` option and related options.

The `--ignoreFiles "<file-or-dir>,<file-or-dir>,..."` option can be used specify a simple comma separated list of files and directories to ignore for the workspace upload:

    paperspace-python run myscript.py --workspace . --ignoreFiles "hello.py,paperspace"

The following files and directories are ignored by default: `.git`, `.gitignore`, `__pycache__`.

The `--dryrun` option allows you to see the resultant script that will be run on the paperspace job runner without actually running it.

Finally, you can provide a trailing list of arguments to pass to the script.

All of the above options can be combined in any combination, however, the order of operations is fixed to the following:

1. `source <init.sh>` is run if `--init <init.sh>` is specified
2. `pipenv [--two|--three] install` is run if `--pipenv` is specified
3. `pip[2|3] install -r requirements.txt` is run if `--req <requirements.txt>` is specified
4. `python[2|3] myscript.py` is run


Default Container
=================
If no `container` option is specified when using `paperspace run <script.py>` or the `paperspace.run()` function the default container image used is `paperspace/tensorflow-python` on Docker Hub.  This container has the tensorflow-gpu libraries installed for both python2 and python3, as well as several other popular packages, including scipy, scikit-learn, pandas, Pillow and pysym.
It is based off the Google docker image gcr.io/tensorflow/tensorflow:latest-gpu` with the addition of support for python3, pip3, and pipenv.


Other examples
==============
See the scripts in the `tests` folder for other examples.


Other Authentication options
============================
1. Specify your apiKey explicitly on any of the paperspace.jobs methods, e.g.:

    `paperspace.jobs.create({'apiKey': '1qks1hKsU7e1k...', 'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})`

2. Set the package paperspace.config option in your python code:

    `paperspace.config.PAPERSPACE_API_KEY = '1qks1hKsU7e1k...'`

3. Set the PAPERSPACE_API_KEY environment variable:

    (on linux/mac:) `export PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

    (on windows:) `set PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

   Note: the above methods take precedence over use of the cached api key in
   `~/.paperspace/config.json`

4. Set the key in the `~/.paperspace/config.json` file from the command line by running:

    `paperspace-python apikey 1qks1hKsU7e1k...`


Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
