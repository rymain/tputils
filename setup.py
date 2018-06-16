#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script managing packaging and more."""


from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
try: # for pip >= 10O
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession


install_reqs = parse_requirements("requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='tpustils',
    version='0.1',
    description='Utils that makes coding easier.',
    author='Tomáš Přinda',
    author_email='tomas.prinda@gmail.com',
    install_requires=reqs,
    # tohle oznaci jako modul kazdou slozku, ktera obsahuje __init__.py
    # proto by testy nemely obsahovat __init__.py
    packages=find_packages(),

)
