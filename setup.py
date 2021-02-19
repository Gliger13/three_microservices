#!/usr/bin/env python

from distutils.core import setup
from os.path import join, dirname

from setuptools import find_packages

VERSION = '0.0.0'

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='three_microservices',
    version=VERSION,
    description='Networking of three microservices',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Andrei Zaneuski',
    author_email='zanevskiyandrey@gmail.com',
    url='https://github.com/Gliger13/three_microservices',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=requirements,
)
