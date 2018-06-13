#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import energytechnomodels

setup(

    name='energytechnomodels',

    version=energytechnomodels.__version__,

    packages=find_packages(),

    author="Pablo Puerto",

    author_email="pablo.puerto@mines-albi.fr",

    description="Energy linked technologies simulation tool",

    long_description=open('README.md').read(),

    install_requires=["pandas", "numpy", "scipy", "thermo", "fluids"],

    include_package_data=True,

    url='',

    classifiers=[
        "Natural Language :: English",
        "Operating GraphCreator :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Simulation",
    ]

)
