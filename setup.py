# -*- coding: utf-8 -*-
from setuptools import setup

modules = ["sample_prep"]
install_requires = [
    "SoundFile>=0.10.3,<0.11.0",
    "click>=8.0.4,<9.0.0",
    "librosa>=0.9.1,<0.10.0",
    "llvmlite>=0.38.0,<0.39.0",
]

entry_points = {"console_scripts": ["sample-prep = sample_prep:cli"]}

setup_kwargs = {
    "name": "sample-prep",
    "version": "0.1.0",
    "description": "Remove silence from percussive samples, normalize and write norm/high/low versions",
    "long_description": None,
    "author": "Stream Punk",
    "author_email": "glad.car1474@fastmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "py_modules": modules,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.9,<3.11",
}


setup(**setup_kwargs)
