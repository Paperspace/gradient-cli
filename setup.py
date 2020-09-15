import io
import os
import re
import sys
from codecs import open

from setuptools import setup, find_packages
from setuptools.command.install import install

with io.open("gradient/version.py", "w", encoding="utf8") as f:
    tag = os.getenv('CIRCLE_TAG')
    build = os.getenv('CIRCLE_BUILD_NUM')
    pr = os.getenv('CIRCLE_PR_NUMBER')
    if pr:
        version = "0.0.0.post{}.dev{}".format(pr, build)
    else:
        version = tag

    f.write("version = {}".format(version))

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError, OSError):
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()


class VerifyVersionCommand(install):
    """Custom command to verify the version"""
    description = 'verify that version is set'

    def run(self):
        if version == '0.0.0':
            sys.exit("No version set")


setup(
    name='gradient',
    version=version,
    description='Paperspace Python',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='paperspace api development library',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'old_tests']),
    install_requires=[
        'requests[security]',
        'six',
        'click>=7.0',
        'terminaltables',
        'click-didyoumean',
        'click-help-colors',
        'click-completion',
        'colorama==0.4.3',
        'requests-toolbelt',
        'progressbar2',
        'halo',
        'marshmallow<3.0',
        'attrs<=19',
        'PyYAML==5.*',
        'python-dateutil==2.*',
        'websocket-client==0.57.*',
        'gradient-utils>=0.1.2',
    ],
    entry_points={'console_scripts': [
        'gradient = gradient:main.main',
    ]},
    extras_require={
        "dev": [
            'tox',
            'pytest',
            'mock',
            'twine',
            'sphinx',
            'pathlib2;python_version<"3.4"',
            'sphinx-click',
            'recommonmark'
        ],
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
