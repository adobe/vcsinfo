"""
Copyright (C) 2014 Adobe
"""
from setuptools import setup, find_packages
import vcsinfo
import os


VERSION='0.1'
BUILD_NR = os.getenv('VCSINFO_NUMBER')
if not BUILD_NR:
    try:
        VCS = vcsinfo.detect_vcs(os.path.dirname(__file__))
        if VCS and VCS.number:
            BUILD_NR = VCS.number
    except vcsinfo.VCSUnsupported:
        pass
if BUILD_NR:
    VERSION = '{}.{}'.format(VERSION, BUILD_NR)


#pylint: disable=C0301
setup(
    name='vcsinfo',
    version=VERSION,
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
        'GitPython==2.1.15',
        'mercurial',
    ],

    # override the default egg_info class to enable setting the tag_build
    cmdclass={
        'egg_info': vcsinfo.VCSInfoEggInfo,
    },
)
