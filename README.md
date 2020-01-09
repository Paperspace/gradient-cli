![GitHubSplash](https://user-images.githubusercontent.com/585865/65443342-e630d300-ddfb-11e9-9bcd-de1d2033ea60.png)

Gradient CLI
=================

![PyPI](https://img.shields.io/pypi/v/gradient)
[![codecov](https://codecov.io/gh/Paperspace/gradient-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/Paperspace/gradient-cli)

<br>

**Get started:** [Create Account](https://www.paperspace.com/account/signup?gradient=true) • [Install CLI](https://docs.paperspace.com/gradient/get-started/install-the-cli) • [Tutorials](https://docs.paperspace.com/gradient/tutorials) • [Docs](https://docs.paperspace.com/gradient)

**Resources:** [Website](https://gradient.paperspace.com/) • [Blog](https://blog.paperspace.com/) • [Support](https://support.paperspace.com/hc/en-us) • [Contact Sales](https://use.paperspace.com/contact-sales)

<br>

Gradient is an an end-to-end MLOps platform that enables individuals and organizations to quickly develop, train, and deploy Deep Learning models.  The Gradient software stack runs on any infrastructure e.g. AWS, GCP, on-premise and low-cost [Paperspace GPUs](https://gradient.paperspace.com/instances).  Leverage automatic versioning, distributed training, built-in graphs & metrics, hyperparameter search, GradientCI, 1-click Jupyter Notebooks, our Python SDK, and more. 

Key components:

* [Notebooks](https://gradient.paperspace.com/notebooks): 1-click Jupyter Notebooks.
* [Experiments](https://gradient.paperspace.com/experiments): Run experiments from a web interface, CLI, SDK, or [GradientCI](https://gradient.paperspace.com/gradientci) bot.
* [Models](https://gradient.paperspace.com/models): Store, analyze, and version models.
* [Inference](https://gradient.paperspace.com/inference): Deploy models as API endpoints.

Gradient supports any ML/DL framework (TensorFlow, PyTorch, XGBoost, etc).

<hr>


See [releasenotes.md](https://github.com/Paperspace/gradient-cli/blob/master/releasenotes.md) for details on the current release, as well as release history.


<br>

Getting Started
===============
1. Make sure you have a Paperspace account set up. Go to [http://paperspace.com](https://www.paperspace.com/account/signup?gradient=true)
   to register.

2. Use pip, pipenv, or conda to install the gradient package, e.g.:

    `pip install -U gradient`

    To install/update prerelease (Alpha/Beta) version version of gradient, use:

    `pip install -U --pre gradient`
3. Enable autocomplete:
    
    Add following to your `.bashrc` (or `.zshrc`) to enable autocomplete anytime you activate your shell.
    If gradient was installed in a virtual environment, the following has to be added to the `activate` script:
     
     `eval "$(_GRADIENT_COMPLETE=source gradient)"`
        
    Alternatively, you can create activation script by:
     
     `(_GRADIENT_COMPLETE=source gradient) > ~/paperspace_complete.sh`
    
    and then add `. ~/paperspace_complete.sh` to your `.bashrc`, `.zshrc` or `activate` script.

    More: https://click.palletsprojects.com/en/7.x/bashcomplete/
4. Set your api key by executing the following:

    `gradient apiKey <your-api-key-here>`

   Note: your api key is cached in ~/.paperspace/config.json

   You can remove your cached api key by executing:

    `gradient logout`

5. Use gradient to run a python script remotely:

    `gradient run myscript.py --name <your-new-job-name>`

   The script will be run on the Paperspace job cluster node, and its output will be logged locally.
   Note: this will archive and upload your entire current working directory to our server if `--workspace` was not provided


Create/create and start experiment
=================
To create new experiment use:
```
gradient experiments create [type] [--options]
```
The two available experiment types are `singlenode` and `multinode`.

To create and immediately start new experiment use:
```
gradient experiments run [type] [--options]
```

For a full list of available commands run `gradient experiments --help`. 
Note that some options are required to create new experiment.


Running a python script by name
===============================
You can run a Python script on a Paperspace server from the command line as follows:

    gradient run myscript.py --name my_new_job

You can also provide additional jobs options on the command line:

    gradient run myscript.py --name my_new_job --projectId myproject --machineType P5000 \
     --container paperspace/tensorflow-python`

Note: this functionality is deprecated and will not be available in future releases

See the [Gradient docs](https://docs.paperspace.com/gradient/jobs/about) for the full list of jobs create options that can be specified.


Basic Run Scenarios
===================
1. Run a python script remotely:

    `gradient run <python_script.py> [args]`

   Example:

    `gradient run myscript.py a b c`

2. Run a python module remotely using the `-m` option:

    `gradient run -m <module_path> [args]`

   Example:

    `gradient run -m pip --version`

3. Run a python command remotely using the `-c` option:

    `gradient run -c "python_statement;..."`

   Example:

    `gradient run -c "import os; print(os.getcwd())"`

4. Run an executable or shell command remotely using the `--shell` option:

    `gradient run --shell "<executable or shell command>"`

   Example:

    `gradient run --shell "ls -al"`

Run Options
===========
The `<script>` option is a python script or path to a python module.  The script or module will be uploaded if it exists on the local file system.

Other script`args` can be provided after the python script or module path.  You can use the `-` option to suppress interpretation of the list of script args as `gradient run` options. 

The `-m <module path>` option runs the specified library module as a script.  This is equivalent to the `-m` option of the `python` executable.  Further paperspace run option processing is disabled after the `-m` option.

The `-c "python_statement;..."` option runs the specified python statements.  This is equivalent to the `-c` option of the `python` executable.  Further paperspace run option processing is disabled after the `-c` option.

The `-` option disables further run command option processing and passes the remaining arguments to the script specified.  This allows you to pass arguments to your script that might otherwise conflict with run command options or jobs create options.

The `--command "shell cmd"` option is used to run an arbitrary executable or shell command inside the container.  Note: the executable or shell command must already be available inside the container image, or be copied over using the `--workspace` option.

Job Options
===========
The `--workspace` option allows you to specify a workspace file or directory to upload, or a git repo link to download and merge with the container.  For example, to upload the current directory along with a script file run:

    gradient run myscript.py --name my_new_job --workspace workspace-dir

Note: `--workspace` defaults to `.`

See the Paperspae API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for more details on the `--workspace` option and related options.

The `--ignoreFiles "<file-or-dir>,..."` option can be used specify a simple comma separated list of files and directories to ignore for the workspace upload:

    gradient run myscript.py --name my_new_job --workspace . --ignoreFiles "hello.py,paperspace"

The following files and directories are ignored by default: `.git`, `.gitignore`, `__pycache__`.

Other `jobs create` options can be specified, such as `--machineType <machine-type>`, `--container <container-image-reference>`, and `--projectId <project-id>`.

See the Paperspae API [jobs create](https://paperspace.github.io/paperspace-node/jobs.html#.create) documentation for a complete description of these options.


Default Container
=================
If no `container` option is specified when using `paperspace run <script.py>` or the `paperspace.run()` function the default container image used is `paperspace/tensorflow-python` on Docker Hub.  This container has the tensorflow-gpu libraries installed for both python2 and python3, as well as several other popular packages, including numpy, scipy, scikit-learn, pandas, Pillow and matplotlib.
It is based off the Google docker image `gcr.io/tensorflow/tensorflow:1.5.0-gpu` with the addition of support for python3, pip3, and pipenv.

A Dockerfile for building this container image is [here](https://github.com/Paperspace/tensorflow-python/).

Other examples
==============
See the scripts in the `tests` folder for other examples.


Authentication options
============================
1. Set the package paperspace.config option in your python code:

    `gradient.config.PAPERSPACE_API_KEY = '1qks1hKsU7e1k...'`

2. Set the PAPERSPACE_API_KEY environment variable:

    (on linux/mac:) `export PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

    (on windows:) `set PAPERSPACE_API_KEY=1qks1hKsU7e1k...`

   Note: the above methods take precedence over use of the cached api key in
   `~/.paperspace/config.json`

3. Set the key in the `~/.paperspace/config.json` file from the command line by running:

    `gradient apiKey 1qks1hKsU7e1k...`


Generating documentation from docstrings
========================================
1. Install dev dependencies
    
    When using pipenv:
    
    `pipenv install --dev`
    
    Otherwise:
    
    `pip install ".[dev]"`

2. Automatically extract docstrings with

    `sphinx-apidoc -f -o source gradient`
    
3. [OPTIONAL] To create HTML version from .rst files

    `make html`
    
    The html version with basic search functionality should appear in `build` directory

4. [OPTIONAL] To generate github pages

    `make gh-pages`

Note: Sphinx offers many more documentation formats via external plugins

For more info visit [Sphinx web page](https://www.sphinx-doc.org)

Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
