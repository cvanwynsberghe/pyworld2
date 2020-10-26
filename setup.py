#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import pyworld2

setup(
    name='pyworld2',
    version=pyworld2.__version__,
    packages=["pyworld2"],
    description="A Python implementation of the model World2",
    long_description=open('README.md').read(),

    author="Charles Vanwynsberghe",
    url='http://github.com/cvanwynsberghe/pyworld2',
    download_url="https://github.com/cvanwynsberghe/pyworld2/archive/v1.0.tar.gz",

    install_requires=["numpy", "scipy", "matplotlib"],

    include_package_data=True,  # files declared in MANIFEST.in

    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Science",
        "Topic :: Education",
    ],

    license="MIT",
    )
