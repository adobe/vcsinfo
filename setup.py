"""
Copyright (C) 2014 Adobe
"""
from setuptools import setup, find_packages
import vcsinfo

#pylint: disable=C0301
setup(
    name='vcsinfo',
    version='0.1',
    author='***REMOVED***',
    author_email="***REMOVED***",
    license="Adobe",
    url="***REMOVED***",
    description="Utilities to normalize working with different Version Control Systems",
    long_description="Utilities to normalize working with different Version Control Systems",

    packages=find_packages(),
    scripts=[
        'bin/vcsinfo',
    ],
    install_requires=[
        'GitPython==2.1.8',
    ],

    # override the default egg_info class to enable setting the tag_build
    cmdclass={
        'egg_info': vcsinfo.VCSInfoEggInfo,
    },
)
