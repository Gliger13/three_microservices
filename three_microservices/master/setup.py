#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

VERSION = '0.0.0'

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='master',
    version=VERSION,
    description='control other microservices',
    author='Andrei Zaneuski',
    author_email='zanevskiyandrey@gmail.com',
    url='https://github.com/Gliger13/three_microservices',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=requirements,
)
