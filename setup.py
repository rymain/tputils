#!/usr/bin/env python

import io
import os.path
import sys

from setuptools import setup, find_packages


def _open(fname):
    """Read a file relatively to this setup.py."""
    return io.open(os.path.join(os.path.dirname(__file__), fname), "rt",
                   encoding="utf-8")


requirements = [line.rstrip('\n') for line in _open('requirements.txt')]

PY2 = sys.version_info[0] == 2

if PY2:
    packages = find_packages()
    # separate entry_points as well?
else:
    packages = [
        "tputils",
    ]

setup(
    name="tputils",
    version="0.1",
    url="https://github.com/rymain/tputils",
    author="Tomáš Přinda",
    author_email="tomas.prinda@gmail.com",
    description="Utils that makes coding easier.",
    packages=packages,
    install_requires=requirements,
)
