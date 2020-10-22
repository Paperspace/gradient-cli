![GitHubSplash](https://user-images.githubusercontent.com/585865/65443342-e630d300-ddfb-11e9-9bcd-de1d2033ea60.png)

Gradient CLI
=================

![PyPI](https://img.shields.io/pypi/v/gradient)
[![codecov](https://codecov.io/gh/Paperspace/gradient-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/Paperspace/gradient-cli)

<br>

**Get started:** [Create Account](https://console.paperspace.com/signup?gradient=true) • [Install CLI](https://docs.paperspace.com/gradient/get-started/install-the-cli) • [Tutorials](https://docs.paperspace.com/gradient/tutorials) • [Docs](https://docs.paperspace.com/gradient)

**Resources:** [Website](https://gradient.paperspace.com/) • [Blog](https://blog.paperspace.com/) • [Support](https://support.paperspace.com/hc/en-us) • [Contact Sales](https://info.paperspace.com/contact-sales)

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
1. Make sure you have a Paperspace account set up. Go to [http://paperspace.com](https://console.paperspace.com/signup?gradient=true)
   to register and generate an API key.

2. Use pip, pipenv, or conda to install the gradient package, e.g.:

    `pip install -U gradient`

    To install/update prerelease (Alpha/Beta) version version of gradient, use:

    `pip install -U --pre gradient`

3. Set your api key by executing the following:

    `gradient apiKey <your-api-key-here>`

   Note: your api key is cached in ~/.paperspace/config.json

   You can remove your cached api key by executing:

    `gradient logout`


Executing tasks on Gradient
=================
The Gradient CLI follows a standard [command] [--options] syntax

For example, to create a new experiment use:
```
gradient experiments create [type] [--options]
```
The two available experiment types are `singlenode` and `multinode`. Various command options include setting the instance type, container, project, etc.  Note that some options are required to create new experiment.

For a full list of available commands run `gradient experiments --help`. You can also view more info about Experiments in the [docs](https://docs.paperspace.com/gradient/experiments/using-experiments).  

Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
