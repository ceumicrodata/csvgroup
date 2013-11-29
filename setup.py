#!/usr/bin/env python
# coding: utf8
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='csvgroup',
    version='0.1',
    description='Group-by aggregation over CSV files',
    long_description=read('README.md'),
    author='Gabor Nyeki (CEU MicroData)',
    url='https://github.com/ceumicrodata/csvgroup.git',
    packages=['csvgroup'],
    entry_points={
        'console_scripts': [
            'csvaggregate = csvgroup.aggregate:main',
            'csvmap = csvgroup.map:main',
        ],
    }
)
