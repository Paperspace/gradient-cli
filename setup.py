import io
import re
from codecs import open
from os import path
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

with io.open("gradient/version.py", "rt", encoding="utf8") as f:
    version = re.search(r"version = \"(.*?)\"", f.read()).group(1)

here = path.abspath(path.dirname(__file__))


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version
            )
            sys.exit(info)


# Get the long description from the README file
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='gradient',
    version=version,
    description='Gradient CLI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/paperspace/gradient-cli',
    author='Paperspace Co.',
    author_email='info@paperspace.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='The command line interface for Gradient - https://gradient.paperspace.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'old_tests']),
    install_requires=[
        'requests[security]',
        'six',
        'gradient-statsd',
        'click',
        'gradient-sdk',
        'terminaltables',
        'click-didyoumean',
        'click-help-colors',
        'click-completion',
        'colorama',
        'requests-toolbelt',
        'progressbar2',
    ],
    entry_points={'console_scripts': [
        'gradient = gradient:main',
    ]},
    extras_require={
        "dev": [
            'tox',
            'pytest',
            'mock',
            'twine',
        ],
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
