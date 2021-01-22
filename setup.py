"""
Copyright (C) 2014-2020 Adobe
"""

import os
import sys
from setuptools import setup, find_packages
import vcsinfo

VERSION = '0.2'
THIS_DIR = os.path.dirname(__file__)
BUILD_NR = None
try:
    VCS = None
    # Only use py_info if git or something else is not available.
    for _vcs in vcsinfo.detect_vcss(THIS_DIR):
        if _vcs.vcs == 'pyinfo':
            VCS = _vcs
            # keep looking for a real VCS
        else:
            VCS = _vcs
            break
    if VCS and VCS.number:
        BUILD_NR = VCS.number
        if VCS.modified:
            BUILD_NR = f'{BUILD_NR}.dev{VCS.modified}'
except vcsinfo.VCSUnsupported:
    pass

if BUILD_NR:
    VERSION = f'{VERSION}.{BUILD_NR}'

REQ_FILE = 'requirements.txt'
REQUIRES = []
try:
    with open(os.path.join(THIS_DIR, REQ_FILE)) as robj:
        for line in robj.readlines():
            _line = line.strip()
            if _line and _line[0].isalpha():
                REQUIRES.append(_line)
except IOError as err:
    # pylint: disable=C0301
    sys.stderr.write(f'Python build requirements must be specified in "{REQ_FILE}": {err}\n')
    sys.exit(err.errno)

# pylint: disable=C0301
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
)
