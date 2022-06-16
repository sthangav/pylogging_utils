#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.0.1'


def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), 'r', 'utf-8').read()

readme = read('README.md')

setup(
    name = 'logging_utils',
    version = __version__,
    description = 'Logging utilities',
    long_description = readme,
    author = 'Michał Bachowski',
    author_email = 'michalbachowski@gmail.com',
    url = 'https://github.com/michalbachowski/pylogging_utils',
    packages = ['logging_utils', 'logging_utils.context', 'logging_utils.context.stack'],
    license = "MIT",
    package_dir = {'logging_utils': 'logging_utils'},
    install_requires = [],
    dependency_links = [],
    zip_safe = True,
    keywords = 'logging_utils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: System :: Logging',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

