"""
Copyright (C) 2014 Adobe
"""

from setuptools import setup, find_packages

setup(
    name='vcsinfo',
    packages=find_packages(),
    scripts=[
        'bin/vcsinfo',
    ],
    install_requires=[
        'GitPython==0.3.2.RC1',
    ],
)

