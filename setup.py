"""
Copyright (C) 2014-2020 Adobe
"""
from __future__ import print_function

from setuptools import setup, find_packages
import vcsinfo
import os
import sys


VERSION='0.1'
THIS_DIR = os.path.dirname(__file__)
BUILD_NR = None
try:
    VCS = None
    # Only use py_egg if git or something else is not available.
    for _vcs in vcsinfo.detect_vcss(THIS_DIR):
        if _vcs.vcs == 'py_egg':
            VCS = _vcs
            # keep looking for a real VCS
        else:
            VCS = _vcs
            break
    print('setup: VCS={}'.format(VCS), file=sys.stderr)
    if VCS and VCS.number:
        BUILD_NR = VCS.number
except vcsinfo.VCSUnsupported:
    pass

if BUILD_NR:
    VERSION = '{}.{}'.format(VERSION, BUILD_NR)
else:
    pipath = os.path.join(THIS_DIR, 'PKG-INFO')
    try:
        with open(pipath, 'r') as pi_obj:
            for line in pi_obj.readlines():
                key, value = line.strip().split(':', 1)
                if key == 'Version':
                    VERSION = value.strip()
                    break
    except IOError:
        pass


REQ_FILE = 'requirements.txt'
REQUIRES = []
try:
    with open(os.path.join(THIS_DIR, REQ_FILE)) as robj:
        for line in robj.readlines():
            _line = line.strip()
            if _line and _line[0].isalpha():
                REQUIRES.append(_line)
except IOError as err:
    sys.stderr.write('Python build requirements must be specified in "{0}": {1}\n'.format(REQ_FILE, err))
    os.exit(err.errno)


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
    install_requires=REQUIRES,

    # override the default egg_info class to enable setting the tag_build
    cmdclass={
        'egg_info': vcsinfo.VCSInfoEggInfo,
    },
)
