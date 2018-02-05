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

    `paperspace-logout logout`

5. Execute the sample Python script hello.py:

    `python hello.py`

   The script will be run on the Paperspace job cluster node, and its output will be
   logged locally.


A slightly more complex example
===============================
    # test/test_remote.py

    import os

    import paperspace

    paperspace.run({'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

    print(os.getcwd())

    print('something useful')


Other examples
==============
See the scripts in the test folder for other examples.


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


Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
