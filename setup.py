#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='csvgroup',
    version='0.0',
    description=u'Group-by aggregation over CSV files',
    author=u'CEU MicroData',
    url='https://github.com/ceumicrodata/csvgroup',
    packages=['csvgroup'],
    install_requires=[],
    provides=['csvgroup (0.0)'],
    entry_points={
        'console_scripts': [
            'csvaggregate = csvgroup.aggregate:main',
            'csvmap = csvgroup.map:main',
        ],
    }
    )
