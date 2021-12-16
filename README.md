![GitHubSplash](https://user-images.githubusercontent.com/585865/65443342-e630d300-ddfb-11e9-9bcd-de1d2033ea60.png)

Gradient CLI
=================

![PyPI](https://img.shields.io/pypi/v/gradient)
[![Downloads](https://pepy.tech/badge/gradient)](https://pepy.tech/project/gradient)

<br>

**Get started:** [Create Account](https://console.paperspace.com/signup?gradient=true) • [Install CLI](https://docs.paperspace.com/gradient/get-started/install-the-cli) • [Tutorials](https://docs.paperspace.com/gradient/tutorials) • [Docs](https://docs.paperspace.com/gradient)

**Resources:** [Website](https://gradient.run/) • [Blog](https://blog.paperspace.com/) • [Support](https://support.paperspace.com/hc/en-us) • [Contact Sales](https://info.paperspace.com/contact-sales-gradient)

<br>

Gradient is an an end-to-end MLOps platform that enables individuals and organizations to quickly develop, train, and deploy Deep Learning models.  The Gradient software stack runs on any infrastructure e.g. AWS, GCP, on-premise and low-cost [Paperspace GPUs](https://gradient.run/instances).  Leverage automatic versioning, distributed training, built-in graphs & metrics, hyperparameter search, GradientCI, 1-click Jupyter Notebooks, our Python SDK, and more. 

Key components:

* [Notebooks](https://gradient.run/notebooks): 1-click Jupyter Notebooks.
* [Workflows](https://gradient.run/workflows): Train models at scale with composable actions. 
* [Inference](https://gradient.run/deployments): Deploy models as API endpoints.

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

For example, to create a new Workflow in a project use:
```
gradient projects list
gradient workflows create --name <name> --projectId <project-id>
```

For a full list of available commands run `gradient workflows --help`. You can also view more info about Workflows in the [docs](https://docs.paperspace.com/gradient/explore-train-deploy/workflows).  

Contributing
============

Want to contribute?  Contact us at hello@paperspace.com


### Pre-Release Testing

Have a Paperspace QA tester install your change directly from the branch to test it.
They can do it with `pip install git+https://github.com/Paperspace/gradient-cli.git@MYBRANCH`.
